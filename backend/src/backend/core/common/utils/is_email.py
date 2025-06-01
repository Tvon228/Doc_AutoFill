import re


def is_email(string: str) -> bool:
    email_pattern: str = r"[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern=email_pattern, string=string))
