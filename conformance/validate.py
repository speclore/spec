#!/usr/bin/env python3
"""Read-only core snapshot checks. Not a serializer, repair tool or agent runtime."""

import argparse
from collections import defaultdict
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from markdown_it import MarkdownIt
from markdown_it.rules_block.table import escapedSplit
from referencing import Registry, Resource

PROFILE = "0.1.0-core"
REPO = Path(__file__).resolve().parents[1]
MARKER = "<!-- speclore:versions -->"
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
MD = MarkdownIt("commonmark", {"html": True, "linkify": True}).enable(
    ["table", "strikethrough", "linkify"]
)
FORMATS = FormatChecker()
if "date-time" not in FORMATS.checkers:
    raise RuntimeError("Install conformance/requirements.txt: RFC 3339 checking is required")
SCHEMAS = {}
for schema_path in sorted((REPO / "schemas/core").glob("*.json")):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    SCHEMAS[schema_path.stem.removesuffix(".schema")] = schema
REGISTRY = Registry().with_resources(
    (schema["$id"], Resource.from_contents(schema)) for schema in SCHEMAS.values()
)


class CoreLoader(yaml.SafeLoader):
    """YAML block mappings with JSON scalar resolution, no implicit dates."""


CoreLoader.yaml_implicit_resolvers = {}
for tag, pattern in [
    ("null", r"^null$"),
    ("bool", r"^(?:true|false)$"),
    ("int", r"^-?(?:0|[1-9][0-9]*)$"),
    ("float", r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)$"),
]:
    CoreLoader.add_implicit_resolver("tag:yaml.org,2002:" + tag, re.compile(pattern), None)


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key == "<<" or key in result:
            raise ValueError("frontmatter keys must be unique strings; merge keys are forbidden")
        result[key] = loader.construct_object(value_node)
    return result


CoreLoader.add_constructor("tag:yaml.org,2002:map", unique_mapping)


def json_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number: " + value)


def parse_document(raw):
    text = raw.decode("utf-8")
    if not text.startswith("---\n") or "\r" in text or not text.endswith("\n"):
        raise ValueError("expected UTF-8/LF document, leading YAML delimiter and final LF")
    lines = text.splitlines(keepends=True)
    end = next((i for i in range(1, len(lines)) if lines[i] == "---\n"), None)
    if end is None:
        raise ValueError("missing closing YAML delimiter")
    front = "".join(lines[1:end])
    for token in yaml.scan(front):
        if isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken, yaml.tokens.TagToken)):
            raise ValueError("YAML tags, anchors and aliases are forbidden")
    node = yaml.compose(front, Loader=CoreLoader)
    if not isinstance(node, yaml.MappingNode) or node.flow_style:
        raise ValueError("frontmatter must be a block YAML mapping")
    meta = yaml.load(front, Loader=CoreLoader)
    json.dumps(meta, allow_nan=False)
    return meta, "".join(lines[end + 1:]), end + 1


def schema_errors(name, value):
    return list(Draft202012Validator(
        SCHEMAS[name], registry=REGISTRY, format_checker=FORMATS
    ).iter_errors(value))


def app_path(path):
    return any(part.startswith("_") for part in PurePosixPath(path).parts[:-1])


def directories(files):
    result = {""}
    for path in files:
        for parent in PurePosixPath(path).parents:
            result.add("" if str(parent) == "." else str(parent))
    return result


def parent_path(path):
    parent = str(PurePosixPath(path).parent)
    return "" if parent == "." else parent


def validate(files, dirs=None):
    """Validate a mapping of root-relative POSIX file paths to bytes, without writing."""
    diagnostics = []

    def error(code, path, message, line=None):
        entry = {"code": code, "severity": "error", "path": path, "message": message}
        if line is not None:
            entry["line"] = line
        diagnostics.append(entry)

    dirs = directories(files) if dirs is None else dirs | directories(files)
    docs, entities, folders, body_links = {}, {}, {}, []
    for path, raw in sorted(files.items()):
        if app_path(path):
            continue
        if any(p.startswith(".") or "\\" in p or any(ord(c) < 32 or ord(c) == 127 for c in p) for p in PurePosixPath(path).parts):
            error("C05", path, "hidden or backslash-containing authored path")
        if not path.endswith(".md"):
            continue
        try:
            meta, body, _ = parse_document(raw)
        except (ValueError, UnicodeError, yaml.YAMLError, TypeError) as exc:
            error("C02", path, str(exc))
            continue
        schema_name = "folder" if meta.get("type") == "folder" else "document"
        issues = schema_errors(schema_name, meta)
        for issue in issues:
            error("C02", path, issue.message)
        if issues:
            continue
        docs[path] = meta
        entity_path = str(PurePosixPath(path).parent) if schema_name == "folder" else path
        if entity_path == ".":
            entity_path = ""
        if schema_name == "folder":
            if PurePosixPath(path).name != "README.md":
                error("C05", path, "folder descriptors must be named README.md")
            folders[entity_path] = meta
            if entity_path and ("speclore" in meta or "relation-types" in meta):
                error("C01", path, "profile and relation catalog belong only to the root")
        if meta["guid"] in entities:
            error("C06", path, "duplicate entity GUID")
        else:
            entities[meta["guid"]] = (entity_path, meta)
        tokens = MD.parse(body)
        titles = [t for t in tokens if t.type == "heading_open" and t.tag == "h1" and t.level == 0]
        if schema_name == "document" and len(titles) != 1:
            error("C03", path, "document requires exactly one top-level H1")
        markers = [i for i, t in enumerate(tokens) if t.type == "html_block"
                   and t.content.strip() == MARKER and t.level == 0]
        if len(markers) > 1:
            error("C04", path, "duplicate versions block")
        allowed_header_end = 0
        for i in markers:
            token = tokens[i]
            if i != 0 or (titles and token.map[0] >= titles[0].map[0]):
                error("C04", path, "versions block must start the body before the title")
            if i + 1 >= len(tokens) or tokens[i + 1].type != "table_open":
                error("C04", path, "versions marker requires a table")
                continue
            table = tokens[i + 1]
            if table.map[0] != token.map[1] + 1:
                error("C04", path, "versions marker requires exactly one blank line before its table")
            j = i + 2
            cells, rows = [], []
            while j < len(tokens) and tokens[j].type != "table_close":
                t = tokens[j]
                if t.type == "tr_open":
                    cells = []
                elif t.type == "inline":
                    cells.append(t.content)
                    if any(child.type not in ("text",) for child in (t.children or [])):
                        error("C04", path, "versions cells must be plain text")
                elif t.type == "tr_close":
                    rows.append(cells)
                j += 1
            if not rows or rows[0] != ["version", "author", "date", "comment"]:
                error("C04", path, "incorrect versions columns")
            for row in rows[1:]:
                if len(row) != 4 or not row[0].strip() or not row[1].strip() or not FORMATS.conforms(row[2], "date-time"):
                    error("C04", path, "invalid versions row")
            # GFM pads/truncates row cells. Require authored rows to have four actual cells.
            for source_line in body.splitlines()[table.map[0]:table.map[1]]:
                split = escapedSplit(source_line.strip())
                if split and split[0] == "":
                    split.pop(0)
                if split and split[-1] == "":
                    split.pop()
                if len(split) != 4:
                    error("C04", path, "versions row must author exactly four cells")
            allowed_header_end = j + 1
        if schema_name == "document" and len(titles) == 1:
            title_index = tokens.index(titles[0])
            if title_index != allowed_header_end:
                error("C03", path, "content before document title")
        for token in tokens:
            if token.type != "inline":
                continue
            for child in token.children or []:
                if child.type in ("link_open", "image"):
                    target = child.attrGet("href" if child.type == "link_open" else "src")
                    body_links.append((path, meta["guid"], target, child.type == "image"))

    root = folders.get("")
    if not root or root.get("speclore") != PROFILE or root.get("usage") != "project" or root.get("kind") != "composite":
        error("C01", "README.md", "root requires folder/project/composite descriptor and exact profile")

    authored_dirs = {d for d in dirs if not any(p.startswith("_") for p in PurePosixPath(d).parts)}
    for directory in sorted(authored_dirs):
        children = [d for d in authored_dirs if d and parent_path(d) == directory]
        if any(p.startswith(".") or "\\" in p or any(ord(c) < 32 or ord(c) == 127 for c in p) for p in PurePosixPath(directory).parts):
            error("C05", directory, "invalid authored folder name")
        if len(children) > 255:
            error("C05", directory, "more than 255 authored child folders")
        if directory in folders:
            prefix = directory + "/" if directory else ""
            direct_files = [p for p in files if str(PurePosixPath(p).parent) == (directory or ".")]
            if direct_files != [prefix + "README.md"]:
                error("C05", directory, "structural root may contain only README.md")
            for child in children:
                if (child in folders) != (folders[directory]["kind"] == "composite"):
                    error("C05", child, "child function disagrees with parent kind")
            if "index" in folders[directory]:
                reserved = set()
                for child in children:
                    numeric = re.match(r"^(\d+)-", PurePosixPath(child).name)
                    if numeric:
                        number = int(numeric[1])
                        if number < 1 or number in reserved or number > folders[directory]["index"]:
                            error("C05", child, "numeric child ID must be unique and within 1..index")
                        reserved.add(number)
        elif directory:
            parent = str(PurePosixPath(directory).parent)
            if parent == ".":
                parent = ""
            if parent not in folders and children:
                error("C05", directory, "thematic folder cannot contain authored subfolders")
            if any(child in folders for child in children):
                error("C05", directory, "notional folder cannot contain structural children")

    expected = {guid: {"guid": guid, "path": path, "refs": {}} for guid, (path, _) in entities.items()}

    def backlink(target, name, source):
        if target not in expected:
            return
        expected[target]["refs"].setdefault(name, set()).add(source)

    entity_paths = {p for p, _ in entities.values()} | {p for p, m in docs.items() if m["type"] == "folder"}
    for path, source, target, is_image in body_links:
        if target.startswith("ref://"):
            guid = target[6:]
            if is_image or not re.fullmatch(UUID, guid) or guid not in entities:
                error("C06", path, "invalid or unresolved entity link: " + target)
            else:
                backlink(guid, "links", source)
            continue
        try:
            parsed = urlsplit(target)
        except ValueError:
            error("C06", path, "malformed URL: " + target)
            continue
        if parsed.scheme in ("http", "https", "mailto"):
            if (parsed.scheme in ("http", "https") and not parsed.netloc) or (parsed.scheme == "mailto" and not parsed.path):
                error("C06", path, "external URL lacks its destination: " + target)
            continue
        if not is_image and target.startswith("#"):
            continue
        decoded = unquote(parsed.path)
        if parsed.scheme or parsed.netloc or not decoded or decoded.startswith("/") or "\\" in decoded:
            error("C06", path, "unsupported link: " + target)
            continue
        parts = list(PurePosixPath(path).parent.parts)
        escaped = False
        for part in decoded.split("/"):
            if part == "..":
                if not parts:
                    escaped = True
                else:
                    parts.pop()
            elif part not in ("", "."):
                parts.append(part)
        resolved = "/".join(parts)
        if escaped or resolved in entity_paths or resolved not in files or app_path(resolved):
            error("C06", path, "local link must target an existing non-entity asset: " + target)

    catalog, used_names = {}, set()
    for relation in (root or {}).get("relation-types", []):
        name, inverse = relation["name"], relation["inverse"]
        if name in used_names or inverse in used_names or "links" in (name, inverse) or (name == inverse and relation["cardinality"] != "N:N"):
            error("C07", "README.md", "conflicting/reserved relation names")
        used_names.update((name, inverse))
        catalog[name] = relation
    incoming = defaultdict(set)
    symmetric = set()
    for source, (path, meta) in entities.items():
        for name, values in meta.get("relations", {}).items():
            definition = catalog.get(name)
            if definition is None:
                error("C07", path, "undeclared relation: " + name)
                continue
            scalar = isinstance(values, str)
            if scalar != (definition["cardinality"] == "1:1"):
                error("C07", path, "relation value shape disagrees with cardinality")
            for value in [values] if scalar else values:
                target = value[6:]
                if target not in entities or source == target:
                    error("C07", path, "dangling or self relation")
                    continue
                incoming[(name, target)].add(source)
                if definition["cardinality"] != "N:N" and len(incoming[(name, target)]) > 1:
                    error("C07", path, "incoming cardinality exceeded")
                if name == definition["inverse"]:
                    edge = (name, *sorted((source, target)))
                    if edge in symmetric:
                        error("C07", path, "symmetric edge authored twice")
                    symmetric.add(edge)
                backlink(target, definition["inverse"], source)
    expected_files = {}
    for guid, record in expected.items():
        record["refs"] = {key: sorted(values) for key, values in record["refs"].items()}
        expected_files[f"_refs/{guid[:2]}/{guid[2:4]}/{guid}.json"] = record
    actual_files = {p for p in files if p.startswith("_refs/")}
    for path in sorted(actual_files | expected_files.keys()):
        if path not in actual_files:
            error("C08", path, "missing reference record")
            continue
        if path not in expected_files:
            error("C08", path, "unexpected/stale/mis-sharded reference record")
            continue
        try:
            raw = files[path].decode("utf-8")
            if "\r" in raw or not raw.endswith("\n"):
                raise ValueError("JSON record requires LF and final LF")
            value = json.loads(raw, object_pairs_hook=json_pairs, parse_constant=reject_constant)
            if schema_errors("refs", value) or value != expected_files[path]:
                raise ValueError("reference record disagrees with schema or authored graph")
        except (ValueError, UnicodeError) as exc:
            error("C08", path, str(exc))
    if "_refs" not in dirs:
        error("C08", "_refs", "missing reference store")
    return {"profile": PROFILE, "valid": not diagnostics, "diagnostics": diagnostics}


def read_snapshot(root):
    files, dirs, links = {}, {""}, []

    def walk(directory):
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(root).as_posix()
            if relative in (".git", ".gitignore"):
                continue
            if path.is_symlink():
                links.append(relative)
            elif path.is_dir():
                dirs.add(relative)
                # Runtime stores are opaque except for the core reference index.
                if not path.name.startswith("_") or relative == "_refs" or relative.startswith("_refs/"):
                    walk(path)
            elif path.is_file():
                files[relative] = path.read_bytes()
    walk(root)
    return files, dirs, links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    try:
        files, dirs, links = read_snapshot(args.project.resolve())
        report = validate(files, dirs)
        for path in links:
            report["diagnostics"].append({"code": "C05", "severity": "error", "path": path, "message": "symlink is not a core artifact"})
        report["valid"] = not report["diagnostics"]
        assert not schema_errors("diagnostic", report)
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
