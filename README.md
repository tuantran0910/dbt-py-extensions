# dbt-py-extensions 🧬

A collection of Python extensions for dbt that can be used in Jinja templates via [dbt-py](https://github.com/billwallis/dbt-py).

## Installation ⬇️

Install both `dbt-py-wrap` and this package in your dbt environment:

```bash
uv pip install dbt-py-wrap
uv pip install git+https://github.com/tuantran0910/dbt-py-extensions@v0.0.1
```

## Configuration 📝

Add the following configuration to your dbt project's `pyproject.toml` file:

```toml
[tool.setuptools]
py-modules = [
    "json_schema",
]

[tool.dbt-py]
packages = [
    {name = "json_schema"},
]
```

## Usage 📖

Once configured, you can use the extension functions in your dbt models via the `modules` object in Jinja templates.

### Example: Inferring Flattened Columns from JSON

```sql
{%- set flattened_columns = modules.json_schema.infer_flattened_columns([{"id": 1, "payload": {"a": 1, "b": {"c": 3}}}], "payload") %}

select
    *,
    {%- for column in flattened_columns %}
        {{ column }} as {{ column }},
    {%- endfor %}
from {{ ref('my_first_dbt_model') }}
where id = 1
```

This will dynamically create columns based on the JSON schema inference:

- `a`
- `b__c`

## Available Functions 🔧

### `infer_flattened_columns(rows, json_column, *, sep="__")`

Infer flattened column names from JSON data in a specified column.

**Parameters:**

- `rows`: List of dictionaries representing table rows
- `json_column`: Name of the column containing JSON data
- `sep`: Separator for nested keys (default: `"__"`)

**Returns:** List of flattened column names as strings

**Example:**

```python
# Input data
rows = [
    {"id": 1, "payload": {"user": {"name": "John", "age": 30}, "active": True}},
    {"id": 2, "payload": {"user": {"name": "Jane", "city": "NYC"}, "active": False}}
]

# Usage
columns = modules.json_schema.infer_flattened_columns(rows, "payload")
# Returns: ["user__name", "user__age", "user__city", "active"]
```

## Running dbt 🏃

Instead of using the regular `dbt` command, use `dbt-py`:

```bash
dbt-py clean
dbt-py build
dbt-py run --select my_model
```

## Dependencies 📦

- [genson](https://pypi.org/project/genson/) - For JSON schema generation
- [dbt-py-wrap](https://pypi.org/project/dbt-py-wrap/) - For extending dbt with Python (required at runtime)

## Development 🚀

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Build package
uv build
```

## License 📄

MIT License - see [LICENSE](LICENSE) file for details.
