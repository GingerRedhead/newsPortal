# Создать новую страницу с адресом /news/, на которой должен выводиться список всех новостей.
#
# Написать собственный фильтр censor, который заменяет буквы нежелательных слов в заголовках и текстах
# статей на символ «*».
#
# Все новые страницы должны использовать шаблон default.html как основу.


from django import template

register = template.Library()

reject_values = {
    'редиска'
}


@register.filter()
def censor(value):
    # Todo: Сделать фильр на слово "Редиска". Предусмотреть Строчные и прописные буквы

    # Todo: Сделать флильтр-Цензор на базе регулярных выражений
    # Todo: Сделать фильтр-Цензор на базе словоформ  и векторов при помощи Pandas

    """
    value: Текст выборки
    return: Итоговое значение после цензурирования
    """
    words = value.strip().split(' ')
    value_final = []

    for word in words:
        if word.lower() in reject_values:
            word_final = []
            first = True
            for letter in word:
                if first:
                    first = False
                    word_final.append(letter)
                else:
                    word_final.append('*')
            value_final.append(''.join(word_final))
        else:
            word_final = word
            value_final.append(word_final)

    return ' '.join(value_final)


@register.filter()
def use_time(value, format_string='%d %b %Y'):
    return value.strftime(format_string)
