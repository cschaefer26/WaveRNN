import re

from num2words import num2words

_comma_number_re = re.compile(r'([0-9]+,[0-9]+)')
_decimal_number_re = re.compile(r'(\d+\.\d{1,2}[^.\d])')  # excludes those digits that have a double dot eg dates 24.03.
_date_re = re.compile(r'([0-9]{1,2}\.+)')
_number_re = re.compile(r'[0-9]+')
_time_re = re.compile(r'([0-9]{1,2}).([0-9]{1,2})(\s*Uhr)')
_decimal_thousands_re = re.compile(r'(\.000)')
_decimal_hundreds_re = re.compile(r'(\.\d\d\d)')


def _expand_comma(m):
    return m.group(1).replace(',', ' Komma ')


def _expand_decimal_point(m):
    return m.group(1).replace('.', ' Komma ')


def _expand_decimal_thousands(m):
    return m.group(1).replace('.000', 'tausend')


def _expand_decimal_hundreds(m):
    return m.group(1).replace('.', 'tausend')


def _fix_time(m):
    if int(m.group(2)):
        return m.group(1) + m.group(3) + ' ' + m.group(2)  # 9 Uhr 30
    else:
        return m.group(1) + m.group(3)


def _expand_date(m):
    num = int(m.group(0).replace('.', ''))
    if num < 20:
        return m.group(1).replace('.', 'ten')
    else:
        return m.group(1).replace('.', 'sten')


def _expand_number(m):
    num = int(m.group(0))
    return num2words(num, lang='de')


def normalize_numbers(text, sub_numbers=True):
    ends_with_dot = text.endswith('.')
    if ends_with_dot:
        text = text[:-1]
    text = re.sub(_comma_number_re, _expand_comma, text)
    text = re.sub(_time_re, _fix_time, text)
    text = re.sub(_decimal_thousands_re, _expand_decimal_thousands, text)
    text = re.sub(_decimal_hundreds_re, _expand_decimal_hundreds, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    text = re.sub(_date_re, _expand_date, text)
    if sub_numbers:
        text = re.sub(_number_re, _expand_number, text)
    if ends_with_dot:
        text += '.'
    return text


if __name__ == '__main__':
    # text = 'Schon vor zwei Jahren nutzten beispielsweise unter den kleinen und mittleren Unternehmen in Deutschland dreimal so viele Big Data wie in 2016.'
    text = 'mit 150.500 deutschen Dividendenpapieren waren es 81.600 2.06 mit 81.653 24.24. 24. 13.03.1991 asd.'
    
    text = normalize_numbers(text)
    
    print(text)
