from ._default_charecteres import default_charecteres


def capitalize(value: str) -> str:
    value = default_charecteres(value=value)

    # capitalize
    col_split = value.split('_')
    value = col_split[0]
    col_split = col_split[1:]

    for char in col_split:
        value += char.capitalize()

    # result example: fieldNameData
    return value
