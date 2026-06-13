from django import template

register = template.Library()

# Список нежелательных слов
BAD_WORDS = [
    'редиска',
    'дурак',
    'идиот',
    'ежиками', # Из примера: "поедания кактусов ёжиками"
    'кактусов'
]

@register.filter()
def censor(value):
    """
    Фильтр цензурирования. Заменяет буквы нежелательных слов на '*',
    оставляя только первую букву. Проверка регистра независимая.

    ВНИМАНИЕ: Применяется только к строкам. Если передано не строка,
    выбрасывается исключение ValueError.
    """
    if not isinstance(value, str):
        raise ValueError("Фильтр censor можно применять только к строкам")

    import re
    result = value
    for bad_word in BAD_WORDS:
        # Ищем слово целиком, игнорируя регистр
        pattern = re.compile(rf'\b{re.escape(bad_word)}\b', re.IGNORECASE)
        # Заменяем слово: первая буква остается, остальные меняются на '*'
        result = pattern.sub(lambda match: match.group(0)[0] + '*' * (len(match.group(0)) - 1), result)

    return result
