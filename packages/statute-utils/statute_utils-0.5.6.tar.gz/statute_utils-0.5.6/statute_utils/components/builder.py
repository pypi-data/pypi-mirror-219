import json
import re
from typing import Any

named_clause = re.compile(r"(First|Second|Third|Fourth|Fifth|Whereas|Enacting)\sClause")
special_starts = (
    "whereas clause",
    "paragraph",
    "sub-paragraph",
    "container",
    "sub-container",
    "proviso",
    "sub-proviso",
    "clause",
)
excludeables = ("container", "sub-container")
shorteables = (
    ("Chapter", "Ch."),
    ("Book", "Bk."),
    ("Article", "Art."),
    ("Section", "Sec."),
    ("Paragraph", "Par."),
)


def is_par(node: dict) -> bool:
    if item := node.get("item"):
        if str(item).startswith("Paragraph"):
            return True
    return False


def try_short(text: str):
    for short in shorteables:
        text = str(text)
        if text.startswith(short[0]):
            text = text.removeprefix(short[0])
            return f"{short[1]} {text}"
    return text


def is_excluded(text: str) -> bool:
    return any(
        [str(text).strip().lower().startswith(excluded) for excluded in excludeables]
    )


def is_special(text: str) -> bool:
    return any(
        [str(text).strip().lower().startswith(special) for special in special_starts]
    )


def is_hidden(text: str | None = None) -> bool:
    """Helper function of set_headline() template tag.
    Used on the node['item'] key of the node being evaluated.

    Args:
        text (str): This generally describes location of the node within
            the tree, e.g. Section 1, Paragraph 1, etc.

    Returns:
        bool: Determine whether it should be hidden or not.
    """
    if not text:
        return False
    if named_clause.search(str(text)):
        return True
    return is_special(text)


def from_json(v: Any) -> list[dict]:
    if v and isinstance(v, str):
        return json.loads(v)
    return v


def set_mp_slug(v: str):
    return v.replace(".", "-").removesuffix("-")


def set_mp(v: str):
    return v.replace("-", ".") + "."


def from_mp(v: str):
    mark = "xxx"
    if mark in v:
        bits = v.split(mark)
        if len(bits) == 2:
            return {"id": bits[0], "mp": set_mp(bits[1])}
    return None
