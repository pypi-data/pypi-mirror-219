import re
from collections.abc import Iterator

import yaml


def shorten_provision(text: str | int):
    text = str(text).removesuffix(".")
    if "Paragraph" in text:
        return re.sub(r"Paragraph", "Par.", text)
    if "Article" in text:
        return re.sub(r"Article", "Art.", text)
    if "Section" in text:
        return re.sub(r"Section", "Sec.", text)
    if "Book" in text:
        return re.sub(r"Book", "Bk.", text)
    if "Chapter" in text:
        return re.sub(r"Chapter", "Ch.", text)
    if "Sub-Container" in text:
        return re.sub(r"Sub-Container(\s+\d+)?", "", text)
    if "Container" in text:
        return re.sub(r"Container(\s+\d+)?", "", text)
    return text


def adjust_caption(text: str | int):
    return str(text).removesuffix(".")


def adjust_heading(text: str, heading: str):
    return f"{text}, {heading}".strip(" ,")


def create_unit_heading(unit: dict, heading: str) -> str:
    """When a search is made for a specific material path, it should be able
    to display a heading. This function consolidates a parent heading
    with the present heading to form the displayed heading."""
    item = unit.get("item")
    caption = unit.get("caption")
    if item and caption:
        text = f"{shorten_provision(item)} ({adjust_caption(caption)})"
        return adjust_heading(text, heading)
    elif item:
        return adjust_heading(shorten_provision(item), heading)
    elif caption:
        return adjust_heading(adjust_caption(caption), heading)
    return heading


def create_fts_snippet_column(unit: dict) -> str | None:
    """An sqlite fts5 function has an auxiliary snippet function
    that takes as a parameter a single column. Since content is
    generally identified by the caption and content, need to
    combine these into a single unit; otherwise, use any of the
    caption / content fields as the searchable / snippetable column text."""
    caption = unit.get("caption")
    content = unit.get("content")
    if caption and content:
        return f"({caption}) {content}"
    elif caption:
        return caption
    elif content:
        return content
    return None


def set_node_ids(
    nodes: list[dict],
    parent_id: str = "1.",
    child_key: str = "units",
):
    """Recursive function updates nodes in place since list/dicts are mutable.
    Assumes that the nodes reprsent a deeply nested json, e.g.

    For each node in the `nodes` list, it will add a new `id` key and will
    increment according to its place in the tree structure.

    If node id "1.1." has child nodes, the first child node will be "1.1.1.".

    A trailing period is necessary for materialized paths. Otherwise a string
    with  `value like '%'` where the value is 1.1 will also match 1.11

    The root of the tree will always be "1.", unless the `parent_id` is
    set to a different string.

    The child key of the tree will always be "units", unless the `child_key`
    is set to a different string.

    Args:
        nodes (list[dict]): The list of dicts that
        parent_id (str, optional): The root node id. Defaults to "1.".
        child_key (str, optional): The node which represents a list of children nodes.
            Defaults to "units".
    """
    if isinstance(nodes, list):
        for counter, node in enumerate(nodes, start=1):
            node["id"] = f"{parent_id}{str(counter)}."
            if node.get(child_key, None):
                set_node_ids(node[child_key], node["id"], child_key)


class literal(str):
    pass


def literal_presenter(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=">")


yaml.add_representer(literal, literal_presenter)


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode("tag:yaml.org,2002:map", value)


yaml.add_representer(dict, represent_ordereddict)


def walk(nodes: list[dict]):
    """Converts raw nodes into a suitably formatted object for `yaml.dump()`.
    Without this, there would be no formatting of content and the ordering
    of the key-value pairs would not be in sync with the intended design.
    """
    if isinstance(nodes, list):
        revised_nodes = []
        for node in nodes:
            data = []
            if node.get("item"):
                candidate = node["item"]
                if candidate := str(node["item"]).strip():
                    if candidate.isdigit():
                        candidate = int(candidate)
                data.append(("item", candidate))
            if node.get("caption"):
                data.append(("caption", node["caption"].strip()))
            if node.get("content"):
                formatted_content = literal(node["content"].strip())
                data.append(("content", formatted_content))
            if node.get("units", None):
                walked_units = walk(node["units"])
                data.append(("units", walked_units))
            revised_nodes.append(dict(data))
    return revised_nodes


def make_regex_readable(regex_text: str):
    """Remove indention of raw regex strings. This makes regex more readable when using
    rich.Syntax(<target_regex_string>, "python")"""
    return rf"""
{regex_text}
"""


def ltr(*args) -> str:
    """
    Most statutes are referred to in the following way:
    RA 8424, P.D. 1606, EO. 1008, etc. with spatial errors like
    B.  P.   22; some statutes are acronyms: "C.P.R."
    (code of professional responsibility)
    """
    joined = r"\.?\s*".join(args)
    return rf"(?:\b{joined}\.?)"


def add_num(prefix: str) -> str:
    num = r"(\s+No\.?s?\.?)?"
    return rf"{prefix}{num}"


def add_blg(prefix: str) -> str:
    blg = r"(\s+Blg\.?)?"
    return rf"{prefix}{blg}"


def get_regexes(regexes: list[str], negate: bool = False) -> Iterator[str]:
    for x in regexes:
        if negate:
            yield rf"""(?<!{x}\s)
                """
        else:
            yield x


def not_prefixed_by_any(regex: str, lookbehinds: list[str]) -> str:
    """Add a list of "negative lookbehinds" (of fixed character lengths) to a
    target `regex` string."""
    return rf"""{''.join(get_regexes(lookbehinds, negate=True))}({regex})
    """


NON_ACT_INDICATORS = [
    r"An",  # "An act to ..."
    r"AN",  # "AN ACT ..."
    r"Republic",  # "Republic Act"
    r"Rep",
    r"Rep\.",
    r"REPUBLIC",
    r"Commonwealth",
    r"COMMONWEALTH",
]
"""If the word act is preceded by these phrases, do not consider the same to be a
legacy act of congress."""
limited_acts = not_prefixed_by_any(rf"{add_num(r'Acts?')}", NON_ACT_INDICATORS)
