import json

import markdown
from jinja2 import Environment, PackageLoader, select_autoescape
from markupsafe import Markup

from .components import (
    StatuteSerialCategory,
    from_json,
    from_mp,
    is_excluded,
    is_hidden,
    is_par,
    set_mp_slug,
    try_short,
)

tree_env = Environment(
    loader=PackageLoader("statute_utils"), autoescape=select_autoescape()
)


def subtree(node: dict, nodes: list[dict]) -> dict:
    """Recursive function that adds `nodes` as deeply nested _units_
    key of the `node`. It presumes the result of a specific format, e.g.
    if the first `node` passed is `{}` (an empty dict), this will will be populated
    with a `units` key containing the content of the `nodes`:

    Examples:
        >>> subtree({}, [{'id': '1.1.', 'content': 'starts here'}, {'id': '1.2.', 'content': 'should be contained in 1.1.', 'units': [{'id': '1.2.1.'}]} ])
        {'units': [{'id': '1.1.', 'content': 'starts here', 'units': [{'id': '1.2.', 'content': 'should be contained in 1.1.', 'units': [{'id': '1.2.1.'}]}]}]}

    Args:
        node (dict): The most recent node via recursion
        nodes (list[dict]): The updated nodes

    Returns:
        dict: The original node
    """  # noqa
    while True:
        try:
            if units := nodes.pop(0):
                node["units"] = [units]
                new_target_node = node["units"][0]
                subtree(new_target_node, nodes)
        except IndexError:
            break

    return node


def build_branch(raw_nodes: list[dict] | str | None) -> str | None:
    """Create a partial tree based on ascendant and a base set of rows (a sequence).
    This is usually received from an sqlite query using json_array. It
    returns another json_array but now containing a tree structure rather
    than the original raw_nodes which was a sequence.
    """  # noqa: E501
    if not raw_nodes:
        return None

    node_list = from_json(raw_nodes)
    if not node_list:
        return None

    branch = subtree({}, node_list)
    content = branch["units"][0]
    branch_json_string = json.dumps(content)
    return branch_json_string


def make_statute_string(cat: str, num: str) -> str | None:
    """Wrapper over `StatuteSerialCategory(cat).cite(num)`.

    Args:
        cat (str): The lowercased code of the statute category
        num (str): The serial instance to associate with the category

    Returns:
        str | None: Readable text identifying the statute, if found.
    """
    return StatuteSerialCategory(cat.lower()).cite(num)


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


tree_helpers = {
    "crumb": crumb,
    "md_to_html": md_to_html,
    "is_par": is_par,
    "set_mp_slug": set_mp_slug,
    "try_short": try_short,
    "from_mp": from_mp,
    "is_excluded": is_excluded,
    "is_hidden": is_hidden,
    "from_json": from_json,
}
tree_env.filters |= tree_helpers


def create_html_tree(units: list[dict]) -> str:
    template = tree_env.get_template("branch.html")
    result = template.render(units=units)
    return str(result).strip()
