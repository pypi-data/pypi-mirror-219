import json

import yaml

from .builder import from_json


def make_branch(node: dict, nodes: list[dict]) -> dict:
    """`Recursive function that adds `nodes` to a position in the subtree
    represented by `node`.

    It presumes the result of a specific format (see `build_branch()`). If the first `node`
    passed is `{}` (an empty dict), this is considered the 'trunk' of
    the subtree which will be populated by `nodes` having the _raw_ hierarchical format of:

    ```yaml title="The variable is expressed in yaml to make the hierarchy readable."
    - id: 1.
    - id: 1.1.
    - id: 1.1.1.
      units:
      - id: 1.1.1.1.
    ```

    The reason it has this format is because of an sqlite json1 union of two queries:

    1. one that retrieves ascendant nodes of a target (1.1.1.) as a list; and
    2. one that retrieves descendants of the same target (1.1.1.) but retaining the hierarchy

    After running `branch` on this _raw_ hierarchical format, the expected structure is a subtree:

    ```yaml title="The variable is expressed in yaml to make the hierarchy readable."
    - id: 1.
      units:
      - id: 1.1.
        units:
        - id: 1.1.1.
          units:
          - id: 1.1.1.1.
    ```

    After the initial run, `node` can be returned to the invoking function and it
    will be populated by a 'units' key containing the list of `nodes`.

    Examples:
        >>> trunk = {}
        >>> nodes = [{'id': '1.1.', 'content': 'starts here'}, {'id': '1.1.1.', 'content': 'should be contained in 1.1.', 'units': [{'id': '1.1.1.1.'}]} ]
        >>> make_branch({}, nodes)
        {'units': [{'id': '1.1.', 'content': 'starts here', 'units': [{'id': '1.1.1.', 'content': 'should be contained in 1.1.', 'units': [{'id': '1.1.1.1.'}]}]}]}

    Args:
        node (dict): The most recent node via recursion
        nodes (list[dict]): Expects

    Returns:
        dict: The original node
    """  # noqa
    while True:
        try:
            if units := nodes.pop(0):
                node["units"] = [units]
                new_target_node = node["units"][0]
                make_branch(new_target_node, nodes)
        except IndexError:
            break

    return node


def make_branch_json_array(raw_nodes: list[dict] | str | None) -> str | None:
    """A wrapper around the `make_branch()` function which expects a sequence of
    `units` keyed nodes and returns a tree structure.

    Args:
        raw_nodes (list[dict] | str | None): base set of rows (a sequence). This is usually received from an sqlite query using json_array.

    Returns:
        str | None: Stringified sqlite usable `json_array`.
    """  # noqa: E501
    if not raw_nodes:
        return None

    node_list = from_json(raw_nodes)
    if not node_list:
        return None

    br = make_branch({}, node_list)
    content = br["units"][0]
    branch_json_string = json.dumps(content)
    return branch_json_string


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
