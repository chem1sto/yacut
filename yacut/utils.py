from re import sub


def get_invalid_symbols(pattern, string):
    """Функция для проверки введённых символов."""
    return set(sub(pattern, '', string))
