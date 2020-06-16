import pickle
from rock_paper_scissors import *
from agents import *
from human_play import *


def pkl_read(fp):
    with open(fp, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    fp = f"./games/2020-06-16-10-29-29-Uniform_random.pkl"
    my_game = pkl_read(fp)
    print(my_game.win_loss_ratio)