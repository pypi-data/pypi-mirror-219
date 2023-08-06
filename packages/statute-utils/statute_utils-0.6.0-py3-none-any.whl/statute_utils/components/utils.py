import re
from collections.abc import Iterator


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
