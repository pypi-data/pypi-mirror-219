import json
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from .components import TREE_FILTERS

tree_env = Environment(
    loader=PackageLoader("statute_utils"),
    autoescape=select_autoescape(),
)
tree_env.filters |= TREE_FILTERS


def render_units(filename: str, v: Any):
    if isinstance(v, str):
        v = json.loads(v)

    if isinstance(v, list):
        return tree_env.get_template(filename).render(units=v).strip()

    raise Exception("Improper value used to render units.")


def html_crumbs_from_hierarchy(v):
    """Expects raw json / json from sqlite-json1 to format into html that
    is suitable for inserting into a DOM. See tree.css which shows the styling
    that can be employed for the result generated: `<span.crumbs>result</span>`
    """
    return render_units("crumbs.html", v)


def html_tree_from_hierarchy(v):
    """Expects raw json / json from sqlite-json1 to format into html that
    is suitable for inserting into a DOM. See tree.css which shows the styling
    that can be employed for the result generated under a recursive `<ul><li>`
    structure.

    For instance, `statute.py` will use this function to create an html
    representation of the `*.yml` file (consisting of units). This makes
    a large dynamically generated tree into a single field for sqlite
    to store. Without this, it would be necessary to reconstruct the tree
    and this takes a substantial amount of time.

    This same mechanism can dynamically create subtrees, given a specific
    set of units in `v`.
    """
    return render_units("subtree.html", v)


def html_paragraph_from_hierarchy(v):
    """Expects raw json / json from sqlite-json1 to format into html that
    is suitable for converting into rtf or Microsoft's ooxml."""
    return render_units("paragraph.html", v)
