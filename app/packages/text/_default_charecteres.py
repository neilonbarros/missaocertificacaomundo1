import unidecode


def default_charecteres(
    value: str,
    space_for_underline: bool,
) -> str:
    # lower
    value = value.lower()

    # unidecode
    value = unidecode.unidecode(value)

    # _
    chars: str = ""
    if space_for_underline is True:
        chars += " "

    chars += "/-?!(){}[]<>.:,*&^%$#@+=\"'"
    for char in chars:
        value = value.replace(char, "_")

    # __
    while "__" in value:
        value = value.replace("__", "_")

    # a
    chars = "ãàáâ"
    for char in chars:
        value = value.replace(char, "a")

    # c
    chars = "ç"
    for char in chars:
        value = value.replace(char, "c")

    # e
    chars = "ẽèéê"
    for char in chars:
        value = value.replace(char, "e")

    # i
    chars = "ĩìíî"
    for char in chars:
        value = value.replace(char, "i")

    # o
    chars = "õòóô"
    for char in chars:
        value = value.replace(char, "o")

    # u
    chars = "ũùúû"
    for char in chars:
        value = value.replace(char, "u")

    return value
