import datetime
import logging
import re
from collections import Counter
from collections.abc import Iterator
from operator import attrgetter
from typing import NamedTuple, Self

from .components import StatuteSerialCategory
from .models import NamedPattern, Rule, SerialPattern
from .models_names import STYLES_NAMED
from .models_serials import STYLES_SERIAL
from .recipes import split_digits


def create_single_pattern_styles(
    styles: list[SerialPattern] | list[NamedPattern],
) -> re.Pattern:
    """Regex strings from either a `SerialPattern` list or a `NamedPattern` list are
    combined into a single regex string so that `finditer()` can used."""  # noqa: E501
    return re.compile("|".join([style.regex for style in styles]), re.X)


SERIALS = create_single_pattern_styles(styles=STYLES_SERIAL)
"""All of the Serial Pattern objects combined into a single pattern object."""

NAMES = create_single_pattern_styles(styles=STYLES_NAMED)
"""All of the Named Pattern objects combined into a single pattern object."""


def extract_serial_rules(text: str) -> Iterator[Rule]:
    """Each `m`, a python Match object, represents a
    serial pattern category with possible ambiguous identifier found.

    So running `m.group(0)` should yield the entire text of the
    match which consists of (a) the definitive category;
    and (b) the ambiguous identifier.

    The identifier is ambiguous because it may be a compound one,
    e.g. 'Presidential Decree No. 1 and 2'. In this case, there
    should be 2 matches produced not just one.

    This function splits the identifier by commas `,` and the
    word `and` to get the individual component identifiers.
    """
    for match in SERIALS.finditer(text):
        for style in STYLES_SERIAL:
            if match.lastgroup == style.group_name:
                if candidates := style.digits_in_match.search(match.group(0)):
                    for d in split_digits(candidates.group(0)):
                        yield Rule(cat=style.cat, num=d.lower())


def extract_named_rules(
    text: str, document_date: datetime.date | None = None
) -> Iterator[Rule]:
    """Using `text`, get named rules in serial format with a special criteria when
    the `document_date` is provided.

    Args:
        text (str): The text to extract named patterns from.
        document_date (datetime.date | None, optional): When present, will use the `named.options`. Defaults to None.

    Yields:
        Iterator[Rule]: The applicable rule found
    """  # noqa: E501
    for m in NAMES.finditer(text):
        for named in STYLES_NAMED:
            if m.lastgroup == named.group_name:
                if named.options and document_date:
                    # sorts the options in descending order
                    options = sorted(
                        named.options, key=attrgetter("date"), reverse=True
                    )
                    for option in options:
                        # default to the first option that can include
                        # the document date, so if the document date
                        # is 1940 and the civil code date sorted options are
                        # [1950, 1889]
                        # this will skip the first because of the `if` conditional
                        # but include the second
                        if option.date and document_date > option.date:
                            yield option
                            break
                else:
                    yield named.rule


def is_rule_ok(
    rule: Rule,
    document_date: datetime.date | None = None,
    context: str | None = None,
) -> bool:
    """If a `document_date` is available, determine if the rule was existing
    at the time of the document's date. If rule inexistent at time of
    `document_date`, then it is likely that the document is wrongly dated and
    ought to be corrected. It is also possible for the rule to be absent
    in the database and therefore the rule date may not be available, in which case
    consider the rule valid.
    """  # noqa: E501
    if not document_date:
        return True

    if not rule.date:
        err = f"Missing date for {rule=}, rule may not be listed in db."
        logging.warning(err)
        return True

    if rule.date < document_date:
        return True
    else:
        err = (
            f"Date mismatch > {context or ''} | {document_date=} likely erroneous for"
            f" {rule=} {rule.date=}".strip()
        )
        logging.error(err)
        return False


def extract_rules(
    text: str,
    document_date: datetime.date | None = None,
    context: str | None = None,
) -> Iterator[Rule]:
    """If text contains [serialized][serial-pattern] (e.g. _Republic Act No. 386_)
    and [named][named-pattern] rules (_the Civil Code of the Philippines_),
    extract the [`Rules`][rule-model] into their canonical serial variants.

    Examples:
        >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
        >>> list(extract_rules(text)) # get all rules
        [<Rule: ra 386>, <Rule: ra 386>, <Rule: spain civil>]

    Args:
        text (str): Text to search for statute patterns.
        document_date (datetime.date | None, optional): When present, makes a naive dated extraction of _named_ ambiguous rules. Defaults to None.
        context (str | None, optional): Helps provide error message, if provided. Defaults to None.

    Yields:
        Iterator[Rule]: Serialized Rules and Named Rule patterns
    """  # noqa: E501
    for rule in extract_serial_rules(text):
        if is_rule_ok(rule, document_date, context):
            yield rule

    for rule in extract_named_rules(text, document_date):
        if is_rule_ok(rule, document_date, context):
            yield rule


def extract_rule(
    text: str, document_date: datetime.date | None = None, context: str | None = None
) -> Rule | None:
    """Thin wrapper over `extract_rules()`. Get the first matching Rule found.

    Examples:
        >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
        >>> extract_rule(text)  # get the first matching rule
        <Rule: ra 386>

    Args:
        text (str): Text to search for statute patterns.
        document_date (datetime.date | None, optional): When present, makes a naive dated extraction of _named_ ambiguous rules. Defaults to None.
        context (str | None, optional): Helps provide error message, if provided. Defaults to None.

    Returns:
        Rule | None: The first Rule found, if it exists
    """  # noqa: E501
    try:
        return next(extract_rules(text, document_date, context))
    except StopIteration:
        return None


class CountedStatute(NamedTuple):
    """Based on results from `extract_rules()`, get count of each
    unique rule found."""

    cat: StatuteSerialCategory
    num: str
    mentions: int = 1

    def __repr__(self) -> str:
        return f"{self.cat} {self.num}: {self.mentions}"

    @classmethod
    def from_source(
        cls,
        text: str,
        document_date: datetime.date | None = None,
        context: str | None = None,
    ) -> Iterator[Self]:
        """Detect counted rules from source `text`.

        Examples:
            >>> text = "The Civil Code of the Philippines, the old Spanish Civil Code; Rep Act No. 386"
            >>> results = list(CountedStatute.from_source(text))
            >>> results
            [ra 386: 2, spain civil: 1]
            >>> results[0] == CountedStatute(cat=StatuteSerialCategory('ra'),num='386', mentions=2)
            True
            >>> results[1] == CountedStatute(cat=StatuteSerialCategory('spain'),num='civil', mentions=1)
            True

        Args:
            text (str): Legalese containing statutory rules in various formats.
            document_date (datetime.date | None, optional): When present, makes a naive dated extraction of _named_ ambiguous rules. Defaults to None.
            context (str | None, optional): Helps provide error message, if provided. Defaults to None.

        Yields:
            Iterator[Self]: Each counted rule found.
        """  # noqa: E501
        rules = extract_rules(text, document_date, context)
        unique_rules = Counter(rules)
        for rule, mention_count in unique_rules.items():
            yield CountedStatute(cat=rule.cat, num=rule.num, mentions=mention_count)

    @classmethod
    def from_repr_format(cls, repr_texts: list[str]) -> Iterator[Self]:
        """Generate pythonic counterparts from `<cat> <id>: <mentions>` format.

        Examples:
            >>> repr_texts = ['ra 386: 2', 'spain civil: 1']
            >>> results = list(CountedStatute.from_repr_format(repr_texts))
            >>> results
            [ra 386: 2, spain civil: 1]
            >>> results[0].cat
            'ra'
            >>> results[0].num
            '386'
            >>> results[0].mentions
            2
            >>> str(results[0])
            'ra 386: 2'
            >>> repr(results[0])
            'ra 386: 2'


        Args:
            repr_texts (str): list of texts having `__repr__` format of a `CountedStatute`

        Yields:
            Iterator[Self]: Instances of CountedStatute
        """  # noqa: E501
        for text in repr_texts:
            counted_bits = text.split(":")
            if len(counted_bits) == 2:
                statute_bits = counted_bits[0].split()
                mentions = counted_bits[1]
                is_cat_id = len(statute_bits) == 2
                is_digit_bit = mentions.strip().isdigit()
                if is_cat_id and is_digit_bit:
                    if cat := StatuteSerialCategory(statute_bits[0]):
                        yield CountedStatute(cat=cat, num=statute_bits[1], mentions=int(mentions))  # type: ignore # noqa: E501
