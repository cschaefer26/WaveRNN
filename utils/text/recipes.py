from utils.files import get_files
from pathlib import Path
from typing import Union

from utils.text.cleaners import basic_cleaners


def ljspeech(path: Union[str, Path]):
    csv_file = get_files(path, extension='.csv')

    assert len(csv_file ) == 1

    text_dict = {}

    with open(csv_file[0], encoding='utf-8') as f :
        for i, line in enumerate(f):
            split = line.split('|')
            key = split[0].split('_')[0]
            text = split[1]
            print(f'{i} {text}')
            text = basic_cleaners(text)
            print(f'{i} {text}')
            text_dict[key] = text

    return text_dict