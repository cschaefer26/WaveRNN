from num2words import num2words

import re

from utils.text.numbers import normalize_numbers

if __name__ == '__main__':

    text = 'Der 10. april.'
    text = normalize_numbers(text)
    print(text)