from triad import Schema
import pyarrow as pa


def is_vec_col(schema: Schema, name: str) -> bool:
    """Check if a column is a vector column. A vector column must be a list
    of numeric values

    :param schema: the schema of the dataframe
    :param name: the column name
    :return: whether it is a vector column
    """
    tp = schema[name].type
    if not pa.types.is_list(tp):
        return False
    return pa.types.is_integer(tp.value_type) or pa.types.is_floating(tp.value_type)
