from genson import SchemaBuilder


def infer_schema(rows, json_column: str) -> dict:
    builder = SchemaBuilder()

    for row in rows:
        value = row.get(json_column)
        if value is not None:
            builder.add_object(value)

    return builder.to_schema()


def extract_flattened_columns(
    schema: dict, parent: str = "", *, sep: str = "__"
) -> list[str]:
    schema_type = schema.get("type")

    if schema_type == "object":
        columns = []
        for key, subschema in schema.get("properties", {}).items():
            path = f"{parent}{sep}{key}" if parent else key
            columns.extend(extract_flattened_columns(subschema, path, sep=sep))
        return columns

    if schema_type == "array":
        # treat arrays as atomic columns
        return [parent]

    # primitive
    return [parent]


def infer_flattened_columns(rows, json_column: str, *, sep: str = "__") -> list[str]:
    """
    Infer flattened column names from a JSON column.
    """
    schema = infer_schema(rows, json_column)
    return extract_flattened_columns(schema, sep=sep)
