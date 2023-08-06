import json
import re
from typing import Any

import markdown
from bs4 import BeautifulSoup, Tag
from markupsafe import Markup

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


def is_first_par(node: dict) -> bool:
    if is_par(node) and str(node["item"]).endswith("1"):
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


def md_to_html(value: str) -> Markup:
    """Convert markdown text to html.

    Args:
        value (str): convert value into html from

    Returns:
        Markup: Usable in template.
    """
    exts = [
        "markdown.extensions.tables",
        "markdown.extensions.footnotes",
        "markdown.extensions.md_in_html",
    ]
    return Markup(markdown.markdown(value, extensions=exts))


def paragrapher(obj: dict[str, Any]) -> str:
    """A node `obj`, as part of a hierarchical structure` will consist of well-defined keys: `item`, `caption` and `content`.
    Instead of rendering the `obj` as part of a json object, format the same so that it becomes suitable for rendering as
    semantic html.

    Examples:
        >>> hidden_item = {"item": "Paragraph 1", "caption": "Short Table.", "content": "a | b\\n--:|:--\\nhello|world" }
        >>> html = paragrapher(hidden_item)
        >>> soup = BeautifulSoup(html, "lxml")
        >>> soup('strong')[0].text
        'Short Table'
        >>> soup('table')[0]
        <table>
        <thead>
        <tr>
        <th style="text-align: right;">a</th>
        <th style="text-align: left;">b</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td style="text-align: right;">hello</td>
        <td style="text-align: left;">world</td>
        </tr>
        </tbody>
        </table>
        >>> item_with_caption = {"item": "Article 1", "caption": "Short Table."}
        >>> paragrapher(item_with_caption)
        '<strong>Article 1</strong> (<em>Short Table</em>).'
        >>> complete_display = {"item": "Article 1", "caption": "Short Title.", "content": "Hello World!"}
        >>> paragrapher(complete_display)
        '<p><strong>Article 1</strong> (<em>Short Title</em>). Hello World!</p>'
        >>> just_body = {"content":"**Hello World**"}
        >>> paragrapher(just_body)
        '<p><strong>Hello World</strong></p>'
        >>> caption_with_content = {"caption": "Permutation", "content":"**Hello World**"}
        >>> paragrapher(caption_with_content)
        '<p><strong>Permutation</strong>. <strong>Hello World</strong></p>'

    Args:
        node (dict[str, Any]): a json object with item, caption, content fields

    Returns:
        str | None: A contextualized html markup string
    """  # noqa: E501

    def paragraph_node(obj):
        return isinstance(obj, Tag) and (obj.name == "p")

    def simple_caption(caption: str) -> str:
        return f"<strong>{caption.removesuffix('.')}</strong>."

    def limited_item_caption(item: str, caption: str) -> str:
        return f"<strong>{item}</strong> (<em>{caption.removesuffix('.')}</em>)."

    def label_provision(value: str, prelim: Tag, soup: BeautifulSoup):
        tag = soup.new_tag("strong")
        tag.string = value.removesuffix(".")
        prelim.insert(0, tag) if paragraph_node(prelim) else prelim.insert_before(tag)
        return tag

    def supplement_label(value: str, anchor: Tag, soup: BeautifulSoup):
        cap = soup.new_tag("em")
        cap.string = value.removesuffix(".")
        anchor.insert_after(cap)
        cap.insert_after(soup.new_string("). "))
        cap.insert_before(soup.new_string(" ("))

    def set_labelled_content(soup: BeautifulSoup, text: str) -> str:
        body = soup("body")[0]
        added_tag = label_provision(text, body.contents[0], soup)
        added_tag.insert_after(soup.new_string(". "))
        return body.decode_contents()

    def full_labelled_content(soup: BeautifulSoup, item: str, caption: str) -> str:
        body = soup("body")[0]
        added_tag = label_provision(item, body.contents[0], soup)
        supplement_label(caption, added_tag, soup)
        return body.decode_contents()

    _item, caption, _content = (obj.get("item"), obj.get("caption"), obj.get("content"))
    item = _item and str(_item)  # converts integer
    content = BeautifulSoup(md_to_html(_content), "lxml") if _content else None

    if item:
        if is_hidden(item):  # Paragraph 1
            if content and caption:  # <p>Hello World</p> + Short Title
                return set_labelled_content(content, caption)
            elif caption:  # Short Title
                return simple_caption(caption)
            elif content:  # <p>Hello World</p>
                return content("body")[0].decode_contents()
        else:  # Article 1
            if content and caption:  # <p>Hello World</p> + Short Title
                return full_labelled_content(content, item, caption)
            elif caption:  # Short Title
                return limited_item_caption(item, caption)
            elif content:  # <p>Hello World</p>
                return set_labelled_content(content, item)
    else:  # Not present
        if content and caption:  # <p>Hello World</p> + Short Title
            return set_labelled_content(content, caption)
        elif caption:  # Short Title
            return simple_caption(caption)
        elif content:  # <p>Hello World</p>
            return content("body")[0].decode_contents()
    return ""


def crumb(node) -> Markup:
    """A series of breadcrumbs can be created based on the depth of a tree node.
    This is a template helper to get the value needed for a particular node. Such value
    depends on the values found in `item` and `caption`."""
    item = node.get("item", "Container")
    caption = node.get("caption")
    if is_excluded(item) and caption:
        return Markup(caption)
    short = try_short(item)
    if caption:
        return Markup(f"{short}&nbsp;<em>({caption})</em>")
    return Markup(f"{short}")


TREE_FILTERS = {
    "crumb": crumb,
    "md_to_html": md_to_html,
    "is_par": is_par,
    "is_first_par": is_first_par,
    "set_mp_slug": set_mp_slug,
    "try_short": try_short,
    "from_mp": from_mp,
    "is_excluded": is_excluded,
    "is_hidden": is_hidden,
    "from_json": from_json,
    "paragrapher": paragrapher,
}
"""A collection of statute utility filters for use in Jinja templates"""
