import argparse
import os
from typing import Any, Dict

import fasttext

import matplotlib.pyplot as plt

import numpy as np


LOG_PATH = 'semantic_learning/training_experiments/temp'
TRAINING_PATH = 'semantic_learning/training_experiments/unsupervised'
TRAINING_LOG_FILE_NAME = 'training.log'
EXPERIMENTAL_MODEL_NAME = 'unsupervised_model.bin'
FINAL_MODEL_NAME = 'semantic_model.bin'


def train_unsupervised(
    train_file: str,
    params: Dict[str, Any],
    experiment_mode: bool,
    output_path: str,
):
    model = fasttext.train_unsupervised(
        input=train_file,
        model='skipgram',
        lr=params['lr'],
        dim=params['dim'],
        ws=5,
        epoch=params['epoch'],
        minCount=5,
        minn=0,
        maxn=0,
        neg=5,
        wordNgrams=params['n_grams'],
        loss=params['loss'],
        bucket=2000000,
        thread=6,
        lrUpdateRate=100,
        t=0.0001,
        verbose=2,
    )
    if experiment_mode:
        experiment_name = f'fasttext_dim-{params["dim"]}_epoch-{params["epoch"]}_loss-{params["loss"]}_lr-{params["lr"]}_ngrams-{params["n_grams"]}'
        training_path = os.path.join(TRAINING_PATH, experiment_name)
        os.makedirs(training_path, exist_ok=True)
        model.save_model(os.path.join(training_path, EXPERIMENTAL_MODEL_NAME))
        with open(os.path.join(LOG_PATH, TRAINING_LOG_FILE_NAME)) as fp:
            loss = [float(line.split()[7]) for line in fp.readlines() if line.startswith('Progress:')]
        plt.figure(figsize=(16, 4))
        plt.plot(loss)
        ticks = np.linspace(0, len(loss) - 1, params['epoch'], dtype=int)
        plt.xticks(ticks, range(params['epoch']))
        plt.grid()
        plt.savefig(os.path.join(training_path, 'progress.png'))
        plt.close()
    else:
        model.save_model(os.path.join(output_path, FINAL_MODEL_NAME))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_file', type=str, default='data/corpus_unsupervised.txt')
    parser.add_argument('--dim', type=int, default=100)
    parser.add_argument('--epoch', type=int, default=7)
    parser.add_argument('--loss', type=str, default='hs')
    parser.add_argument('--lr', type=float, default=0.05)
    parser.add_argument('--n_grams', type=int, default=1)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--experiment_mode', action='store_true', default=False)
    group.add_argument('--output_path', type=str, default='binaries')

    args = parser.parse_args()
    params = {
        'dim': args.dim,
        'epoch': args.epoch,
        'loss': args.loss,
        'lr': args.lr,
        'n_grams': args.n_grams,
    }
    train_unsupervised(args.train_file, params, args.experiment_mode, args.output_path)
