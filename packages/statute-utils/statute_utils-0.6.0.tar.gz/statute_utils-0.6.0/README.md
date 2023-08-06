# statute-utils

![Github CI](https://github.com/justmars/statute-utils/actions/workflows/main.yml/badge.svg)

Philippine statutory law pattern matching and unit retrieval; utilized in [LawSQL dataset](https://lawsql.com).

## Documentation

See [documentation](https://justmars.github.io/statute-utils).

## Development

Checkout code, create a new virtual environment:

```sh
poetry add statute-utils # python -m pip install statute-utils
poetry update # install dependencies
poetry shell
```

## Some unit patterns

```json title="Convention used when desiring to exclude appropriation laws."
{
  "units": [
    {
        "item": "Container 1",
        "content": "Appropriation laws are excluded.",
    }
  ]
}
```

```json title="Convention used when no content found."
UNITS_NONE = [
    {
        "item": "Container 1",
        "content": "Individual provisions not detected.",
    }
]
```

## Use in Datasette

### Add units to a database from a pre-made file

Consider an example `db.sqlite`:

```py title="Assumes path-to-file.yml exists"
>>> from sqlite_utils import Database
>>> from statute_utils import Statute
>>> f = Path().joinpath(path-to-file.yml)
>>> db = Database('db.sqlite')
>>> db["statutes"].insert(Statute.from_file(f).make_row())
# this will contain an 'html' column containing a semantic tree structure that can be styled via css
```

### Copy html/css files

1. `tree.html` - Tree-building macros (which can be used for creating an html tree to represent the statute)
2. `tree.css` - Sample css rulesets to use for the tree generated with the macros

Copy files to the Jinja environment where these can be reused:

```text
- /app
--|
  |--/static
      |--tree.css # copy it here
  |--/templates
      |--tree.html # copy it here
  |--db.sqlite
```

When datasette is served with:

```jinja
datasette serve db.sqlite --template-dir=app/templates/ --static static:app/static
```

It becomes possible to import the macros file into a future files:

```jinja title="app/templates/future.html"
{% from 'tree.html' import create_branches %}
{{ create_branches(units|from_json) }} {# note that from_json is custom filter added in the Datasette environment as a one-off plugin}
```

### Add filters / custom functions

Create a file in the plugins directory:

```text
- /app
- /app
--|
  |--/static
      |--tree.css
  |--/templates
      |--tree.html
  |--/plugins
      |--tree.py # new
  |--db.sqlite
```

When datasette is served with:

```jinja
datasette serve db.sqlite --plugins-dir=app/plugins/ {# plus the other arguments #}...
```

It becomes possible to use custom functions and filters found in `tree.py`.
