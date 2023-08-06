import logging
import pathlib
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, TypeVar, cast

import attr
import yaml
from jsonschema import RefResolver

from psqlgml import types, typings
from psqlgml.types import DictionarySchema

__all__ = [
    "Association",
    "Dictionary",
    "from_object",
]

logger = logging.getLogger(__name__)

DEFAULT_META_SCHEMA: typings.Final[str] = "metaschema.yaml"
DEFAULT_DEFINITIONS: FrozenSet[str] = frozenset(
    ["_definitions.yaml", "_terms.yaml", "_terms_enum.yaml", "_settings.yaml"]
)

T = TypeVar("T")
RESOLVERS: Dict[str, "Resolver"] = {}


@attr.s(auto_attribs=True)
class Resolver:
    name: str
    schema: Dict[str, Any]

    @property
    def ref(self) -> RefResolver:
        return RefResolver(f"{self.name}#", self.schema)

    def resolve(self, reference: str) -> Any:
        base, _ = reference.split("#", 1)
        resolver = RESOLVERS[base] if base else self
        ref = resolver.ref
        _, resolution = ref.resolve(reference)
        return resolve_schema(resolution, resolver)

    def repr(self) -> str:
        return f"{self.__class__.__name__}<{self.name}>"


@attr.s(auto_attribs=True, frozen=True)
class Association:
    """An edge between two node types

    Fields:
        src: label for source node type
        dst: label for destination node type
        label: label for this edge, eg member_of
        name: A unique name for the edge
        is_reference: True if it is a backref
    """

    src: str
    dst: str
    label: str
    name: str
    backref: Optional[str] = None
    is_reference: bool = False


def extract_association(src: str, link: types.SubGroupedLink) -> Set[Association]:
    associations = set()
    links: List[types.SubGroupedLink] = [link]

    while links:
        current = links.pop()
        if "name" in current:
            dst = current["target_type"]
            label = current["label"]
            name = current["name"]
            backref = current["backref"]
            associations.add(Association(src, dst, label, name, backref=backref))
            associations.add(Association(dst, src, "", backref, is_reference=True))
        if "subgroup" in current:
            for sub in current["subgroup"]:
                links.append(cast(types.SubGroupedLink, sub))

    return associations


@attr.s(auto_attribs=True, frozen=True, hash=True)
class Dictionary:
    """Data Dictionary instance representation

    Fields:
        name: name or label of the dictionary
        version: version number of the dictionary
        schema: node label, schema collection/mapping
        url: location of the dictionary
    """

    name: str
    version: str
    schema: Dict[str, DictionarySchema] = attr.ib(hash=False)
    url: Optional[str] = None

    @property
    def links(self) -> Set[str]:
        all_links: Set[str] = set()
        for label in self.schema:
            associations = self.associations(label)
            all_links.update([assoc.name for assoc in associations])
        return all_links

    @lru_cache()
    def associations(self, label: str) -> Set[Association]:
        return {a for a in self.all_associations() if a.src == label}

    @lru_cache()
    def all_associations(self) -> Set[Association]:
        associations: Set[Association] = set()
        for label, label_schema in self.schema.items():
            for link in label_schema.links:
                associations.update(extract_association(label, link))
        return associations


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_not_yaml_file_extension(file_name: str) -> bool:
    extension = pathlib.Path(file_name).suffix
    return extension.lower() not in [".yml", ".yaml"]


def load_schemas(
    schema_path: str,
    meta_schema: str = DEFAULT_META_SCHEMA,
    definitions: FrozenSet[str] = DEFAULT_DEFINITIONS,
) -> Dict[str, DictionarySchema]:
    excludes: FrozenSet[str] = frozenset([meta_schema] + list(definitions))
    raw_schemas: List[types.DictionarySchemaDict] = []

    definitions_paths = Path(schema_path)
    for definition in definitions_paths.iterdir():
        # skip non yaml files and directories
        if (
            definition.is_dir()
            or definition.name == "README.md"
            or is_not_yaml_file_extension(definition.name)
        ):
            continue

        path = definition.name
        schema = load_yaml(definition)
        RESOLVERS[path] = Resolver(name=path, schema=schema)
        if path not in excludes:
            raw_schemas.append(cast(types.DictionarySchemaDict, schema))

    return _load_schema(raw_schemas)


def resolve_schema(entry: T, resolver: Optional[Resolver] = None) -> T:
    # unit entries
    if not isinstance(entry, (list, dict)):
        return entry

    # handle list
    if isinstance(entry, list):
        return cast(T, [resolve_schema(e, resolver) for e in entry])

    resolved: Dict[str, Any] = {}
    for k, v in entry.items():
        if k == "$ref":
            refs = v
            if not isinstance(refs, list):
                refs = [v]

            for ref in refs:
                resolution = resolve_ref(ref, resolver)
                resolved.update(resolution)
        else:
            resolved[k] = resolve_schema(v, resolver)
    return cast(T, resolved)


def resolve_ref(reference: str, resolver: Optional[Resolver] = None) -> Any:
    logger.debug(f"Resolving reference: {reference} with resolver: {resolver}")

    base, _ = reference.split("#", 1)
    if not resolver or (base and resolver.name != base):
        resolver = RESOLVERS[base]
    return resolver.resolve(reference)


def _load_schema(schemas: List[types.DictionarySchemaDict]) -> Dict[str, DictionarySchema]:
    loaded: Dict[str, DictionarySchema] = {}
    for schema in schemas:
        if "id" not in schema:
            logger.info("Skipping definition without an id entry")
            continue

        logger.debug(f"Resolving dictionary schema with id: {schema['id']}")

        raw: types.DictionarySchemaDict = resolve_schema(schema)
        loaded[schema["id"]] = DictionarySchema(raw=raw)

        logger.debug(f"Schema resolution complete for schema id: {schema['id']}")
    return loaded


def from_object(
    schema: Dict[str, types.DictionarySchemaDict], name: str, version: str
) -> Dictionary:
    """Loads a dictionary from a traditional dictionary object loaded using a compliant gdcdictionary

    Args:
        schema: gdcdictionary compliant schema
        name: unique name/label used to identify this dictionary
        version: appropriate version number for the dictionary
    Returns:
        A Dictionary instance
    """
    revised_schema: Dict[str, DictionarySchema] = {}

    for label, s in schema.items():
        revised_schema[label] = DictionarySchema(raw=s)
    return Dictionary(schema=revised_schema, name=name, version=version)
