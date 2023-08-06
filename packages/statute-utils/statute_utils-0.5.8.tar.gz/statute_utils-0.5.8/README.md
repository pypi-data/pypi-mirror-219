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

are found in `statute_utils/templates/statute.html`.

The present module has a directory for `statute_utils/templates/`:

It contains:

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

It becomes possible to use custom functions and filters found in `tree.py` likeso:

```py title="datasette/plugins/tree.py"
from datasette import hookimpl
from statute_utils.display import from_json, is_hidden, is_excluded, from_mp, try_short, set_mp_slug, is_par, md_to_html, build_branch, crumb, tree_helpers

@hookimpl
def prepare_jinja2_environment(env): # custom filters can be used in datasette pages
  env.filters["from_json"] = from_json
  env.filters["is_hidden"] = is_hidden
  env.filters["is_excluded"] = is_excluded
  env.filters["from_mp"] = from_mp
  env.filters["try_short"] = try_short
  env.filters["set_mp_slug"] = set_mp_slug
  env.filters["is_par"] = is_par
  env.filters["md_to_html"] = md_to_html
  env.filters["crumb"] = crumb

@hookimpl
def prepare_connection(conn): # custom function can be used in sqlite
    conn.create_function("build_branch", 1, build_branch)
```
