from datetime import date, datetime
from typing import Any
from django.http import QueryDict


def post_rich(
    post: QueryDict,
    model: dict[str, Any],
) -> QueryDict:
    for key, value in model.items():
        if key not in list(post.keys()):
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")

            elif isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")

            post.update({key: value})

    return post
