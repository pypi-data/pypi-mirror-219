import datetime
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import yaml

from .components import (
    StatuteSerialCategory,
    StatuteTitle,
    create_fts_snippet_column,
    create_unit_heading,
    set_node_ids,
    walk,
)
from .models import STATUTE_DIR, Rule
from .templater import html_tree_from_hierarchy


class Statute(NamedTuple):
    """A instance is dependent on a statute path from a fixed
    `STATUTE_DIR`. The shape of the Python object will be different
    from the shape of the dumpable `.yml` export."""

    titles: list[StatuteTitle]
    rule: Rule
    variant: int
    date: datetime.date
    units: list[dict]

    def __str__(self) -> str:
        return f"{self.rule.__str__()}, {self.date.strftime('%b %d, %Y')}"

    def __repr__(self) -> str:
        return "/".join(
            [
                self.rule.cat.value,
                self.rule.num,
                self.date.isoformat(),
                f"{str(self.variant)}.yml",
            ]
        )

    @property
    def slug(self):
        return self.__repr__().removesuffix(".yml").replace("/", "-")

    def make_title_rows(self) -> Iterator[dict[str, str]]:
        for counter, title in enumerate(self.titles, start=1):
            yield {
                "id": f"{self.slug}-{counter}",
                "statute_id": self.slug,
                "cat": title.category.name.lower(),
                "text": title.text,
            }

    def make_row(self) -> dict:
        """All nodes in the tree are marked by a material path.

        The units key is manipulated to add a root node. This is
        useful for repeals and other changes since affecting the root node, affects all nodes.

        The root node for every key should be `1.`

        A special `html` field exists for the purpose of performance. Since some units
        are overly large, this creates an unstyled html blob that semantically represents
        the tree object. The helper functions that were used to create the tree object
        can be re-used using the same function via filters.
        ```
        """  # noqa: E501
        set_node_ids(self.units)
        units = [{"id": "1.", "units": self.units}]
        return {
            "id": self.slug,
            "cat": self.rule.cat.value,
            "num": self.rule.num,
            "date": self.date,
            "variant": self.variant,
            "units": units,
            "html": html_tree_from_hierarchy(units),
        }

    @classmethod
    def flatten_units(
        cls, statute_id: str, units: list[dict[str, Any]], heading: str = ""
    ) -> Iterator[dict[str, str | None]]:
        """Recursive flattening of tree structure where each material path
        gets its own item, caption, and content fields with extracted heading / snippetable
        columns from such fields. Use cases:

        1. Material path with individual fields reconstructs subtrees
        2. Snippetable column becomes a searchable FTS summary of caption + content
        3. Heading column makes identifable the subtree involved with item + caption

        """  # noqa: E501
        for unit in units:
            present_heading = create_unit_heading(unit, heading)
            yield {
                "statute_id": statute_id,
                "material_path": unit["id"],  # enable subtree
                "heading": present_heading,  # identify subtree
                "item": unit.get("item"),
                "caption": unit.get("caption"),
                "content": unit.get("content"),
                "snippetable": create_fts_snippet_column(unit),  # enable searchability
            }
            if subunits := unit.get("units"):
                yield from cls.flatten_units(statute_id, subunits, present_heading)

    def to_file(self) -> Path:
        """Orders different key, value pairs for a yaml dump operation.
        Ensures each node in the tree is properly (rather than alphabetically) ordered.
        """
        f = STATUTE_DIR.joinpath(self.__repr__())
        f.parent.mkdir(parents=True, exist_ok=True)
        data: dict = self._asdict()
        data["units"] = walk(data["units"])
        text = yaml.dump(data, width=60)  # see representer added in walk
        f.write_text(text)
        return f

    @classmethod
    def from_file(cls, file: Path):
        """Assumes strict path routing structure: `cat` / `num` / `date` / `variant`.yml,
        e.g. `ra/386/1946-06-18/1.yml` where each file contains the following metadata, the
        mandatory ones being "title" and "units". See example:

        ```yaml
        title: An Act to Ordain and Institute the Civil Code of the Philippines
        aliases:
        - New Civil Code
        - Civil Code of 1950
        short: Civil Code of the Philippines
        units:
        - item: Container 1
          caption: Preliminary Title
          units:
            - item: Chapter 1
              caption: Effect and Application of Laws
              units:
                - item: Article 1
                  content: >-
                    This Act shall be known as the "Civil Code of the Philippines."
                    (n)
                - item: Article 2
                  content: >-
                    Laws shall take effect after fifteen days following the
                    completion of their publication either in the Official
                    Gazette or in a newspaper of general circulation in the
                    Philippines, unless it is otherwise provided. (1a)
        ```
        """  # noqa: E501
        cat, num, date, variant = file.parts[-4:]
        _date = [int(i) for i in date.split("-") if i]

        data = yaml.safe_load(file.read_bytes())
        official = data.get("title")
        if not official:
            return None

        category = StatuteSerialCategory(cat)
        if not category:
            return None

        serial = category.serialize(num)
        if not serial:
            return None

        return cls(
            rule=Rule(cat=category, num=num),
            variant=int(variant.removesuffix(".yml")),
            date=datetime.date(year=_date[0], month=_date[1], day=_date[2]),
            units=data.get("units"),
            titles=list(
                StatuteTitle.generate(
                    official=official,
                    serial=serial,
                    short=data.get("short"),
                    aliases=data.get("aliases"),
                )
            ),
        )
