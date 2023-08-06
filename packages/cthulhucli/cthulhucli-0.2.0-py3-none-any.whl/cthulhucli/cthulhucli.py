#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from json import loads
from operator import itemgetter, eq, ne, gt, ge, lt, le
from os.path import join, dirname
from re import compile as re_compile, IGNORECASE
from string import capwords
from sys import argv


from click import (
    Choice,
    ClickException,
    ParamType,
    argument,
    command,
    echo,
    option,
    pass_context,
    secho,
    style,
)


__version__ = "0.2.0"


CARD_TYPES = ["Character", "Conspiracy", "Event", "Story", "Support"]
CARD_TYPES_UNIQUE = ["Character", "Support"]
FACTIONS = {
    "The Agency": {"alias": ["Agency"]},
    "Cthulhu": {},
    "Hastur": {},
    "Miskatonic University": {},
    "Neutral": {},
    "Shub-Niggurath": {},
    "Silver Twilight": {"alias": ["Lodge"]},
    "Syndicate": {},
    "Yog-Sothoth": {},
}
FACTION_ALIASES = {
    alias: faction
    for faction, data in FACTIONS.items()
    for alias in [faction] + data.get("alias", [])
}
KEYWORDS = [
    "Dormant",
    "Fast",
    "Fated",
    "Heroic",
    "Invulnerability",
    "Loyal",
    "Resilient",
    "Steadfast",
    "Toughness",
    "Transient",
    "Villainous",
    "Willpower",
]
SORT_KEYS = [
    "arcane",
    "combat",
    "cost",
    "faction",
    "investigation",
    "name",
    "set",
    "skill",
    "terror",
    "type",
]
COUNT_KEYS = [
    "arcane",
    "combat",
    "cost",
    "era",
    "faction",
    "icons",
    "investigation",
    "keyword",
    "name",
    "restricted",
    "set",
    "skill",
    "subtypes",
    "terror",
    "type",
    "unique",
]
REGEX_KEYS = [
    "name",
    "subtype",
    "subtype_isnt",
    "text",
    "text_isnt",
]
TYPE_KEYS = {
    "arcane": {"Character"},
    "combat": {"Character"},
    "faction": {"Character", "Conspiracy", "Event", "Support"},
    "icons": {"Character"},
    "investigation": {"Character"},
    "skill": {"Character"},
    "terror": {"Character"},
    "unique": {"Character", "Support"},
}
DB_KEY_MAPPING = {"set": "setname"}
FIELD_NAME_MAPPING = {v: k for k, v in DB_KEY_MAPPING.items()}
TEST_FALSE = []
FIELDS = [
    ("Unique", "unique", 0, ["Character", "Support"], True),
    ("Faction", "faction", 0, ["Character", "Support", "Event", "Conspiracy"], False),
    ("Type", "type", 0, None, True),
    ("Cost", "cost", 0, ["Character", "Support", "Event", "Conspiracy"], True),
    (
        "Transient",
        "transient",
        2,
        ["Character", "Support", "Event", "Conspiracy"],
        True,
    ),
    (
        "Steadfast",
        "steadfast",
        2,
        ["Character", "Support", "Event", "Conspiracy"],
        True,
    ),
    ("Skill", "skill", 0, ["Character"], True),
    ("Icons", "icons", 0, ["Character"], True),
    ("Era", "era", 2, None, False),
    ("Set", "setname", 2, None, False),
    ("Card #", "id", 2, None, False),
    ("Illustrator", "illustrator", 2, None, False),
    ("Restricted", "restricted", 2, None, True),
    ("Banned", "banned", 2, None, True),
]


class IntComparison(ParamType):
    name = "NUMBER COMPARISON"
    operators = {"==": eq, "!=": ne, "<": lt, "<=": le, ">": gt, ">=": ge}
    parser = re_compile(r"^(==|!=|<|<=|>|>=)?\s*(\d+|[xX])$")

    def convert(self, value, param=None, ctx=None):
        """
        Return a function that implements the integer comparison formulated by
        `value`.

        Examples:
            >>> comparer = IntComparison()
            >>> comparer.convert("10")(10)
            True
            >>> comparer.convert("!=10")(10)
            False
            >>> comparer.convert("<10")(10)
            False
            >>> comparer.convert("<10")(0)
            True
            >>> comparer.convert("<=10")(10)
            True
            >>> comparer.convert(">10")(-1)
            False
            >>> try:
            ...     comparer.convert("foo")(0)
            ... except Exception as e:
            ...     print(str(e))
            Invalid integer comparison: foo
        """
        match = self.parser.match(value.strip())
        if not match:
            self.fail("Invalid integer comparison: {}".format(value))
        operator, number = match.groups()
        func = eq if operator is None else self.operators[operator]
        number = int(number) if number not in ("x", "X") else None

        def compare(x):
            try:
                return func(x, number)
            except TypeError:
                return False

        return compare


INT_COMPARISON = IntComparison()


@command()
@argument("search", nargs=-1)
@option("--brief", is_flag=True, default=False, help="Show brief card data.")
@option("--case", is_flag=True, default=False, help="Use case sensitive matching.")
@option(
    "--cost",
    type=INT_COMPARISON,
    multiple=True,
    help="Find cards whose cost matches the expression (inclusive).",
)
@option(
    "--count",
    multiple=True,
    help=(
        "Show card count breakdown for given field. Increase verbosity to "
        "also show individual cards. Possible fields are: {}."
    ).format(", ".join(COUNT_KEYS)),
)
@option("--exact", is_flag=True, default=False, help="Use exact matching.")
@option(
    "--faction",
    "-f",
    multiple=True,
    help="Find cards with given faction (inclusive). Possible factions are: {}.".format(
        ", ".join(sorted(FACTION_ALIASES.keys()))
    ),
)
@option(
    "--faction-isnt",
    multiple=True,
    help="Find cards with other than given faction (exclusive).",
)
@option(
    "--group",
    multiple=True,
    help=(
        "Sort resulting cards by the given field and print group headers. "
        "Possible fields are: {}."
    ).format(", ".join(COUNT_KEYS)),
)
@option(
    "--inclusive",
    is_flag=True,
    default=False,
    help=(
        "Treat multiple options of the same type as inclusive rather than exclusive. "
        "(Or-logic instead of and-logic.)"
    ),
)
@option(
    "--name",
    multiple=True,
    help="Find cards with matching name. (This is the default search.)",
)
@option("--non-unique", is_flag=True, help="Find non-unique cards.")
@option("--regex", "-r", is_flag=True, help="Use regular expression matching.")
@option(
    "--set",
    multiple=True,
    help="Find cards from matching expansion sets (inclusive).",
)
@option(
    "--show",
    multiple=True,
    help="Show only given fields in non-verbose mode. Possible fields are: {}.".format(
        ", ".join(COUNT_KEYS)
    ),
)
@option(
    "--sort",
    multiple=True,
    help="Sort resulting cards by the given field. Possible fields are: {}.".format(
        ", ".join(SORT_KEYS)
    ),
)
@option(
    "--skill",
    type=INT_COMPARISON,
    multiple=True,
    help="Find cards whose Skill matches the expression (inclusive).",
)
@option(
    "--terror",
    type=INT_COMPARISON,
    multiple=True,
    help="Find cards whose Terror matches the expression (inclusive).",
)
@option(
    "--combat",
    type=INT_COMPARISON,
    multiple=True,
    help="Find cards whose Combat matches the expression (inclusive).",
)
@option(
    "--arcane",
    type=INT_COMPARISON,
    multiple=True,
    help="Find cards whose Arcane matches the expression (inclusive).",
)
@option(
    "--investigation",
    type=INT_COMPARISON,
    multiple=True,
    help="Find cards whose Investigation matches the expression (inclusive).",
)
@option("--text", multiple=True, help="Find cards with matching text (exclusive).")
@option(
    "--text-isnt", multiple=True, help="Find cards without matching text (exclusive)."
)
@option(
    "--subtype", multiple=True, help="Find cards with matching subtype (exclusive)."
)
@option(
    "--subtype-isnt",
    multiple=True,
    help="Find cards without matching subtype (exclusive).",
)
@option(
    "--keyword",
    multiple=True,
    help=(
        "Find cards with matching keyword (exclusive). Possible fields are: {}.".format(
            ", ".join(KEYWORDS)
        )
    ),
)
@option(
    "--keyword-isnt",
    multiple=True,
    help=(
        "Find cards without matching keyword (exclusive). "
        "Possible fields are: {}.".format(", ".join(KEYWORDS))
    ),
)
@option(
    "--type",
    "-t",
    multiple=True,
    help=(
        "Find cards with matching card type (inclusive). "
        "Possible types are: {}.".format(", ".join(CARD_TYPES))
    ),
)
@option("--unique", is_flag=True, help="Find unique cards.")
@option(
    "--verbose",
    "-v",
    count=True,
    help="Show more card data.",
)
@option(
    "--era",
    type=Choice(["All", "CCG", "LCG"], case_sensitive=False),
    default="LCG",
    show_default=True,
    help="Specify which era of cards to search.",
)
@option(
    "--version",
    is_flag=True,
    default=False,
    help="Show the cthulhucli version: {}.".format(__version__),
)
@pass_context
def main(ctx, search, **options):
    """
    A command line interface for Call of Cthulhu LCG and CCG.

    The default SEARCH arguments matches cards against their name. See below
    for more options.

    Options marked with inclusive or exclusive can be repeated to further
    include or exclude cards, respectively.

    For help and bug reports visit the project on GitHub:
    https://github.com/jimorie/cthulhucli
    """
    preprocess_options(search, options)
    if options["version"]:
        echo(__version__)
        return
    if len(argv) == 1:
        echo(ctx.get_usage())
        return
    for opt, types in TYPE_KEYS.items():
        if (
            options.get(opt)
            or opt in options["count"]
            or opt in options["group"]
            or opt in options["sort"]
        ):
            if options["type"]:
                options["type"] &= types
            else:
                options["type"] = types
    cards = load_cards(options)
    cards = filter_cards(cards, options)
    cards = sort_cards(cards, options)
    counts, total = count_cards(cards, options)
    if options["count"]:
        options["verbose"] -= 1
    elif total == 1 and options["brief"] is False:
        options["verbose"] += 1
    if options["show"]:
        options["verbose"] = 0
        options["brief"] = False
    prevgroup = None
    groupkey = sortkey(*options["group"]) if options["group"] else None
    for card in cards:
        if options["verbose"] >= 0:
            if groupkey:
                thisgroup = groupkey(card)
                if thisgroup != prevgroup:
                    if prevgroup is not None and options["verbose"] < 1:
                        echo("")
                    secho(
                        "[ {} ]".format(
                            " | ".join(
                                format_card_field(card, group, color=False)
                                for group in options["group"]
                            )
                        ),
                        fg="yellow",
                        bold=True,
                    )
                    echo("")
                    prevgroup = thisgroup
            print_card(card, options)
    print_counts(counts, options, total)


def preprocess_options(search, options):
    """Preprocess all options."""
    preprocess_search(options, search)
    preprocess_regex(options)
    preprocess_case(options)
    preprocess_faction(options)
    preprocess_sort(options)
    preprocess_count(options)
    preprocess_type(options)
    preprocess_keyword(options)


def preprocess_search(options, search):
    """Treat non-option args as one string."""
    if search:
        options["name"] = [" ".join(search), *options["name"]]


def preprocess_regex(options):
    """Compile regex patterns for relevant options."""
    flags = IGNORECASE if not options["case"] else 0
    if options["regex"]:
        for opt in REGEX_KEYS:
            if options[opt]:
                options[opt] = tuple(
                    re_compile(value, flags=flags) for value in options[opt]
                )


def preprocess_case(options):
    """Preprocess relevant options for case comparison."""
    # These options are always case insensitive
    opts = ("set", "keyword", "keyword_isnt")
    if not options["case"] and not options["regex"]:
        # These options respect the case and regex options
        opts += tuple(REGEX_KEYS)
    for opt in opts:
        options[opt] = tuple(value.lower() for value in options[opt])


def preprocess_faction(options):
    """Preprocess faction arguments to valid options."""

    def postprocess_faction_value(value):
        return FACTION_ALIASES[value]

    aliases = FACTION_ALIASES.keys()
    preprocess_field(
        options, "faction", aliases, postprocess_value=postprocess_faction_value
    )
    preprocess_field(
        options, "faction_isnt", aliases, postprocess_value=postprocess_faction_value
    )


def preprocess_sort(options):
    """Preprocess sortable arguments to valid options."""
    preprocess_field(options, "group", COUNT_KEYS, postprocess_value=get_field_db_key)
    preprocess_field(options, "sort", SORT_KEYS, postprocess_value=get_field_db_key)
    preprocess_field(options, "show", COUNT_KEYS, postprocess_value=get_field_db_key)


def preprocess_count(options):
    """Preprocess count arguments to valid options."""
    preprocess_field(options, "count", COUNT_KEYS, postprocess_value=get_field_db_key)


def preprocess_type(options):
    """Preprocess type arguments to valid options."""
    preprocess_field(options, "type", CARD_TYPES)
    options["type"] = set(options["type"])


def preprocess_keyword(options):
    """Preprocess keyword arguments to valid options."""
    preprocess_field(options, "keyword", KEYWORDS)
    preprocess_field(options, "keyword_isnt", KEYWORDS)


def preprocess_field(options, field, candidates, postprocess_value=None):
    """
    Preprocess value of `field` in `options` to the best match in `candidates`.
    """
    if options[field]:
        values = list(options[field])
        for i, value in enumerate(values):
            value = value.lower()
            value = get_single_match(value, candidates)
            if value is None:
                raise ClickException(
                    "no such --{} argument: {}.  (Possible arguments: {})".format(
                        get_field_name(field), values[i], ", ".join(candidates)
                    )
                )
            if postprocess_value:
                value = postprocess_value(value)
            values[i] = value
        options[field] = tuple(values)


def get_single_match(value, candidates):
    """
    Return the single member in `candidates` that starts with `value`, else
    `None`.

    Examples:
        >>> get_single_match("foo", ["foobar", "barfoo"])
        'foobar'
        >>> get_single_match("foo", ["foobar", "barfoo", "foobarfoo"]) is None
        True
        >>> get_single_match("foo", ["barfoo"]) is None
        True
        >>> get_single_match("foo", []) is None
        True
        >>> get_single_match("", []) is None
        True
        >>> get_single_match("", ["foobar"])
        'foobar'
        >>> get_single_match("", ["foobar", "barfoo"]) is None
        True
    """
    found = None
    for candidate in candidates:
        if candidate.lower().startswith(value):
            if found:
                return None
            found = candidate
    return found


def get_field_name(field):
    """Return `field` without negating suffix."""
    return field[: -len("_isnt")] if field.endswith("_isnt") else field


def get_field_db_key(field):
    """Return the corresponding database field for `field`."""
    return DB_KEY_MAPPING.get(field, field)


def get_faction_name(faction_code):
    """Return a human friendly faction name for `faction_code`."""
    return FACTIONS[faction_code].get("name", faction_code)


def load_cards(options):
    """Load card data from file."""
    paths = []
    if options["era"] in ("CCG", "All"):
        paths.append(join(dirname(__file__), "coc-ccg.data"))
    if options["era"] in ("LCG", "All"):
        paths.append(join(dirname(__file__), "coc-lcg.data"))
    for filepath in paths:
        with open(filepath, "r") as f:
            for line in f:
                yield loads(line)


def filter_cards(cards, options):
    """Yield all members in `cards` that match the given `options`."""
    for card in cards:
        if test_card(card, options):
            yield card


def test_card(card, options):
    """Return `True` if `card` match the given `options`, else `False`."""
    for option_name, value in options.items():
        test = CardFilters.get_test(option_name)
        if test and (value or type(value) is int or option_name in TEST_FALSE):
            if not test(card, value, options):
                return False
    return True


class CardFilters(object):
    @classmethod
    def get_test(cls, option):
        try:
            return getattr(cls, "test_" + option)
        except AttributeError:
            return None

    @staticmethod
    def match_value(value, card_value, options):
        """
        Test if the requested `value` matches the `card_value`. Where `value`
        can be both a string or a regex object.

        Examples:
            >>> CardFilters.match_value("foo", "foo", defaultdict(bool))
            True
            >>> CardFilters.match_value("foo", "bar", defaultdict(bool))
            False
            >>> CardFilters.match_value("foo", "Foo", defaultdict(bool))
            True
            >>> CardFilters.match_value("foo", "Foo", defaultdict(bool, case=True))
            False
            >>> CardFilters.match_value("foo", "foofoo", defaultdict(bool))
            True
            >>> CardFilters.match_value("foo", "foofoo", defaultdict(bool, exact=True))
            False
            >>> CardFilters.match_value(re_compile("f[oaeu]+"), "foofoo", defaultdict(bool))
            True
            >>> CardFilters.match_value(re_compile("f[oaeu]+"), "boo", defaultdict(bool))
            False
            >>> CardFilters.match_value(re_compile("f[oaeu]+"), "foofoo", defaultdict(bool, exact=True))
            False
        """
        if card_value is None:
            return False
        if hasattr(value, "search"):
            match = value.search(card_value)
            if options["exact"]:
                return (
                    match is not None
                    and match.start() == 0
                    and match.end() == len(card_value)
                )
            else:
                return match is not None
        else:
            if not options["case"]:
                card_value = card_value.lower()
            return value == card_value if options["exact"] else value in card_value

    @staticmethod
    def test_cost(card, tests, options):
        return any(test(card["cost"]) for test in tests)

    @staticmethod
    def test_skill(card, tests, options):
        return any(test(card["skill"]) for test in tests)

    @staticmethod
    def test_terror(card, tests, options):
        return any(test(card["terror"]) for test in tests)

    @staticmethod
    def test_combat(card, tests, options):
        return any(test(card["combat"]) for test in tests)

    @staticmethod
    def test_arcane(card, tests, options):
        return any(test(card["arcane"]) for test in tests)

    @staticmethod
    def test_investigation(card, tests, options):
        return any(test(card["investigation"]) for test in tests)

    @staticmethod
    def test_faction(card, values, options):
        return any(card["faction"] == value for value in values)

    @staticmethod
    def test_faction_isnt(card, values, options):
        return all(card["faction"] != value for value in values)

    @staticmethod
    def test_name(card, value, options):
        return any(
            CardFilters.match_value(name, card["name"], options) for name in value
        )

    @staticmethod
    def test_unique(card, values, options):
        return card["type"] in CARD_TYPES_UNIQUE and card["unique"] is True

    @staticmethod
    def test_non_unique(card, values, options):
        return card["type"] in CARD_TYPES_UNIQUE and card["unique"] is False

    @staticmethod
    def test_set(card, values, options):
        return any(
            CardFilters.match_value(value, card["setname"], options) for value in values
        ) or any(
            CardFilters.match_value(value, card["setname"], options) for value in values
        )

    @staticmethod
    def test_text(card, values, options):
        any_or_all = any if options["inclusive"] else all
        return any_or_all(
            CardFilters.match_value(value, card["text"], options) for value in values
        )

    @staticmethod
    def test_text_isnt(card, values, options):
        any_or_all = any if options["inclusive"] else all
        return any_or_all(
            not CardFilters.match_value(value, card["text"], options)
            for value in values
        )

    @staticmethod
    def test_subtype(card, values, options):
        subtypes = [subtype.strip() for subtype in card["subtypes"].split(".")]
        any_or_all = any if options["inclusive"] else all
        return any_or_all(
            any(
                CardFilters.match_value(value, subtype, options) for subtype in subtypes
            )
            for value in values
        )

    @classmethod
    def test_subtype_isnt(cls, card, values, options):
        return not cls.test_subtype(card, values, options)

    @staticmethod
    def test_keyword(card, values, options):
        keywords = parse_keywords(card["text"])
        any_or_all = any if options["inclusive"] else all
        return any_or_all(
            any(keyword in value for keyword in keywords) for value in values
        )

    @classmethod
    def test_keyword_isnt(cls, card, values, options):
        return not cls.test_keyword(card, values, options)

    @staticmethod
    def test_type(card, values, options):
        return any(card["type"].startswith(value) for value in values)


def sortkey(*sortfields):
    def _sortkey(card):
        sortkey = []
        for field in sortfields:
            if field == "subtypes":
                sortkey.append(len(card["subtypes"].split(".")))
            elif field not in card:
                sortkey.append(format_card_field(card, field, color=False))
            elif card[field] is None:
                sortkey.append(-2)
            else:
                sortkey.append(-1 if card[field] == "X" else card[field])
        return sortkey

    return _sortkey


def sort_cards(cards, options):
    if options["sort"] or options["group"]:
        sortfields = options["group"] + options["sort"]
        return sorted(cards, key=sortkey(*sortfields))
    return list(cards)


def count_cards(cards, options):
    counts = defaultdict(lambda: defaultdict(int))
    total = 0
    for card in cards:
        total += 1
        if options["count"]:
            for count_field in options["count"]:
                if count_field == "subtypes":
                    for subtype in card["subtypes"].split("."):
                        if subtype:
                            counts[count_field][subtype.strip()] += 1
                elif count_field == "keyword":
                    for keyword in parse_keywords(card["text"]):
                        counts[count_field][keyword] += 1
                elif count_field == "unique":
                    if card[count_field]:
                        counts[count_field][format_field_name(count_field)] += 1
                    else:
                        counts[count_field][
                            "Non-" + format_field_name(count_field)
                        ] += 1
                elif count_field == "icons":
                    counts[count_field][format_icons(card, False)] += 1
                elif card[count_field] or type(card[count_field]) is int:
                    counts[count_field][card[count_field]] += 1
    return counts, total


def print_card(card, options):
    if options["verbose"]:
        print_verbose_card(card, options)
    elif options["brief"]:
        secho(card["name"], fg="cyan", bold=True)
    elif options["show"]:
        print_brief_card(card, options, options["show"])
    else:
        print_brief_card(card, options)


def print_verbose_card(card, options):
    secho(card["name"], fg="cyan", bold=True)
    if card["descriptor"]:
        secho(card["descriptor"], fg="cyan", bold=False)
    if card["subtypes"]:
        secho(card["subtypes"], fg="magenta", bold=True)
    if card["text"]:
        echo(card["text"])
    fields = [
        (label, key)
        for label, key, verbosity, types, default in FIELDS
        if options["verbose"] >= verbosity
        and (types is None or card["type"] in types)
        and (default or card[key])
    ]
    print_verbose_fields(card, fields)
    echo("")


def print_verbose_fields(card, fields):
    for name, field in fields:
        value = card.get(field)
        secho("{}: ".format(name), bold=True, nl=False)
        if field == "faction":
            echo(get_faction_name(value) if value else "No Faction")
        elif field == "icons":
            echo(format_icons(card))
        elif field == "steadfast":
            echo(format_steadfast(card))
        elif value is None:
            echo("X")
        elif type(value) is bool:
            echo("Yes" if value else "No")
        elif field in ["type"]:
            echo(value)
        elif type(value) is int:
            echo(str(value))
        else:
            echo(value)


def print_brief_card(card, options, show=None):
    """Print `card` details on one line."""
    if show is None:
        show = [
            key
            for _, key, verbosity, types, default in FIELDS
            if verbosity == 0
            and (types is None or card["type"] in types)
            and (default or card[key])
        ]
    secho(card["name"] + ":", fg="cyan", bold=True, nl=False)
    for field in show:
        tmp = format_card_field(card, field, show_negation=False)
        if tmp:
            if tmp.endswith("."):
                secho(" {}".format(tmp), nl=False)
            else:
                secho(" {}.".format(tmp), nl=False)
    secho("")


def print_counts(counts, options, total):
    """Print a human friendly summary of the `counts` and `total`."""
    if options["verbose"] == 0:
        echo("")
    for count_field, count_data in counts.items():
        items = list(count_data.items())
        items.sort(key=itemgetter(1), reverse=True)
        secho(
            "[ {} counts ]".format(format_field_name(count_field)),
            fg="green",
            bold=True,
        )
        echo("")
        fill = 0
        for i in range(len(items)):
            items[i] = (format_field(count_field, items[i][0]), items[i][1])
            fill = max(fill, len(items[i][0]))
        for count_key, count_val in items:
            secho(count_key, bold=True, nl=False)
            echo(": ", nl=False)
            echo(" " * (fill - len(count_key)), nl=False)
            echo(str(count_val))
        echo("")
    secho("Total count: ", fg="green", bold=True, nl=False)
    echo(str(total))


def format_field_name(field):
    """Format a `field` name for human friendly output."""
    field = FIELD_NAME_MAPPING.get(field, field)
    return capwords(field)


def format_field(field, value, show_negation=True):
    """Format a basic `field` and `value` for human friendly output."""
    if field == "faction":
        return get_faction_name(value) if value else "No Faction"
    if value is None:
        return "X {}".format(format_field_name(field))
    if type(value) is int or value == "X":
        return "{} {}".format(value, format_field_name(field))
    if type(value) is bool:
        if show_negation or value:
            return "{}{}".format("" if value else "Non-", format_field_name(field))
        return None
    return str(value)


def format_card_field(card, field, color=True, show_negation=True):
    """Format the value of `field` on `card` for human friendly output."""
    if field == "keyword":
        keywords = parse_keywords(card["text"])
        if keywords:
            return " ".join(capwords(kw) + "." for kw in keywords)
    if field == "icons":
        return format_icons(card)
    db_key = get_field_db_key(field)
    return format_field(field, card.get(db_key), show_negation=show_negation)


def format_icons(card, color=True):
    """Format the card icons."""
    icons = ""
    for field, char in (
        ("terror", style("(T)", fg="green") if color else "(T)"),
        ("combat", style("(C)", fg="blue") if color else "(C)"),
        ("arcane", style("(A)", fg="magenta") if color else "(A)"),
        ("investigation", style("(I)", fg="yellow") if color else "(I)"),
    ):
        icons += char * card[field]
    return icons if icons else "No Icons"


def format_steadfast(card):
    """Format steadfast."""
    if card["steadfast"]:
        return ", ".join(
            f"{faction} x {amount}" for faction, amount in card["steadfast"]
        )
    return "No"


def parse_keywords(text):
    """Return the list of valid keywords found at the start of `text`."""
    text = text.lstrip()
    keywords = []
    while True:
        for keyword in KEYWORDS:
            if text.startswith(keyword):
                keywords.append(keyword)
                if "." in text:
                    text = text[text.find(".") + 1 :].lstrip()
                else:
                    text = ""
                break
        else:
            break
    return keywords


if __name__ == "__main__":
    main()
