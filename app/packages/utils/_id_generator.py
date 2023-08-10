import random
import string


def id_generator(
    size=4,
    letter: bool = True,
    digits: bool = True,
):
    if letter is False and digits is False:
        raise ValueError("without chars for to generate")

    chars: str = ""
    if letter is True:
        chars += string.ascii_lowercase

    if digits is True:
        chars += string.digits

    return "".join(random.choice(chars) for _ in range(size))
