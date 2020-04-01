from num2words import num2words

import re

_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_date_re = re.compile(r'([0-9]+\.+)')
_number_re = re.compile(r'[0-9]+')


def _expand_comma(m):
  return m.group(1).replace(',', ' Komma ')

def _expand_decimal_point(m):
  return m.group(1).replace('.', ' Komma ')

def _expand_date(m):
  num = int(m.group(0).replace('.', ''))
  if num < 20:
    return m.group(1).replace('.', 'ten')
  else:
    return m.group(1).replace('.', 'sten')


def _expand_number(m):
  num = int(m.group(0))
  return num2words(num, lang='de')

def normalize_numbers(text):
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_date_re, _expand_date, text)
  text = re.sub(_number_re, _expand_number, text)
  return text

if __name__ == '__main__':

  text = 'Bis zum 10. April'

  text = normalize_numbers(text)

  print(text)