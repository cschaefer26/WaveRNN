import glob
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

    # Parse Arguments
    parser = argparse.ArgumentParser(description='TTS Generator')
    parser.add_argument('--input_text', '-i', type=str, help='[string] Type in something here and TTS will generate it!')
    parser.add_argument('--tts_weights', type=str, help='[string/path] Load in different Tacotron weights')
    parser.add_argument('--save_attention', '-a', dest='save_attn', action='store_true', help='Save Attention Plots')
    parser.add_argument('--force_cpu', '-c', action='store_true', help='Forces CPU-only training, even when in CUDA capable environment')
    parser.add_argument('--hp_file', metavar='FILE', default='hparams.py', help='The file to use for the hyperparameters')

    parser.set_defaults(input_text=None)
    parser.set_defaults(weights_path=None)
    args = parser.parse_args()

    hp.configure(args.hp_file)  # Load hparams from file

    sr = 22050
    bits = 6
    path = '/Users/cschaefe/Downloads/04059.npy'
    m = np.load(path)
    m = (m + 4) / 8
    np.clip(m, 0, 1, out=m)

    wav = reconstruct_waveform(m, n_iter=32)
    save_wav(wav, '/tmp/sample_test.wav')