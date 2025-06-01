import re


def try_parse_phone_number(phone_string: str) -> int | None:
    """ Пытается извлечь номер телефона из строки """
    if not phone_string:
        return None

    # Удаляем все нецифровые символы
    digits = re.sub(r"[^\d]", "", phone_string)

    # Проверяем минимальную длину номера
    if not digits or len(digits) < 10:
        return None

    try:
        return int(digits)
    except ValueError:
        return None