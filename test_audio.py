import glob

from preprocess import convert_file
from utils.display import *
from utils.dsp import *
from utils import hparams as hp
from multiprocessing import Pool, cpu_count
from utils.paths import Paths
import pickle
import argparse
from utils.text.recipes import ljspeech
from utils.files import get_files
from pathlib import Path

if __name__ == '__main__':
    sr = 22050
    bits = 9
    path = '/Users/cschaefe/datasets/audio_data/Cutted/02628_1.1.2.Seehofer_verbietet_Reichsbürger-Gruppe_-_Razzien_in_zehn_Ländern.wav'
#    path = '/tmp/seehofer_48000.wav'
    y, _ = librosa.load(path, sr=sr)
    quant = encode_mu_law(y, mu=2**bits)
    wav = decode_mu_law(quant, mu=2**bits)
    m, x = convert_file(Path(path))
    x = decode_mu_law(x, mu=2**bits)
    librosa.output.write_wav(f'/tmp/sample_target.wav', y, sr=sr)
    librosa.output.write_wav(f'/tmp/sample_{bits}bits.wav', wav, sr=sr)
    librosa.output.write_wav(f'/tmp/sample_{bits}bits_prep.wav', x, sr=sr)
