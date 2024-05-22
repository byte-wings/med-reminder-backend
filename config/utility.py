import re

phone_regex = re.compile(r"^998([378]{2}|(9[013-57-9]))\d{7}$")


def check_phone(phone_number: str) -> bool:
    return bool(phone_regex.match(phone_number))

