""" from https://github.com/keithito/tacotron """
from utils.text.symbols import approved_symbols, punctuation
from phonemizer.phonemize import phonemize

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from .numbers import normalize_numbers

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('mrs', 'misess'),
    ('mr', 'mister'),
    ('dr', 'doctor'),
    ('st', 'saint'),
    ('co', 'company'),
    ('jr', 'junior'),
    ('maj', 'major'),
    ('gen', 'general'),
    ('drs', 'doctors'),
    ('rev', 'reverend'),
    ('lt', 'lieutenant'),
    ('hon', 'honorable'),
    ('sgt', 'sergeant'),
    ('capt', 'captain'),
    ('esq', 'esquire'),
    ('ltd', 'limited'),
    ('col', 'colonel'),
    ('ft', 'fort'),
]]


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def expand_numbers(text):
    return normalize_numbers(text)


def lowercase(text):
    return text.lower()


def collapse_whitespace(text):
    return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
    return unidecode(text)


def normalize_text(text):
    text = ''.join([c for c in text if c in approved_symbols])
    return text


def basic_cleaners(text):
    '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
    # text = lowercase(text)
    text = normalize_text(text)
    text = normalize_numbers(text)
    # text = expand_numbers(text)
    text = to_phonemes(text)
    text = collapse_whitespace(text)
    return text


def basic_cleaners_prod(text, hints):
    '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
    # text = lowercase(text)
    text = normalize_text(text)
    text = normalize_numbers(text)
    # text = expand_numbers(text)
    text = to_phonemes_prod(text, hints)
    text = collapse_whitespace(text)
    return text


def transliteration_cleaners(text):
    '''Pipeline for non-English text that transliterates to ASCII.'''
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def english_cleaners(text):
    '''Pipeline for English text, including number and abbreviation expansion.'''
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_numbers(text)
    text = expand_abbreviations(text)
    text = collapse_whitespace(text)
    return text


def to_phonemes_prod(text, hints):
    words = text.split(' ')
    phonemes = []
    for word in words:
        word, replaced = apply_hints(word, hints)
        if not replaced:
            text = text.replace('-', '—')
            word = phonemize(word,
                             language='de',
                             backend='espeak',
                             strip=True,
                             preserve_punctuation=True,
                             with_stress=False,
                             njobs=1,
                             punctuation_marks=';:,.!?¡¿—…"«»“”()',
                             language_switch='remove-flags')
            word = word.replace('—', '-')
        phonemes.append(word)
    phonemes = ' '.join(phonemes)
    return phonemes


def apply_hints(word, hints):
    last_char = word[-1]
    replaced = False
    stripped = last_char in punctuation and len(word) > 1
    if stripped:
        word = word[:-1]
    if word in hints:
        word = hints[word]
        replaced = True
    if stripped:
        word += last_char
    return word, replaced


def to_phonemes(text):
    text = text.replace('-', '—')
    phonemes = phonemize(text,
                         language='de',
                         backend='espeak',
                         strip=True,
                         preserve_punctuation=True,
                         with_stress=False,
                         njobs=1,
                         punctuation_marks=';:,.!?¡¿—…"«»“”()',
                         language_switch='remove-flags')
    phonemes = phonemes.replace('—', '-')
    return phonemes
