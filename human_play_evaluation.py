import pickle
import matplotlib.pyplot as plt
from rock_paper_scissors import *
from agents import *
from human_play import *


def pkl_read(fp):
    with open(fp, 'rb') as f:
        return pickle.load(f)


def color(agent):
    if agent == "Uniform_random":
        return 'gray'
    elif agent == "Fixed_absolute_markovian":
        return 'red'
    elif agent == "Fixed_relative_markovian":
        return 'pink'
    elif agent == "MW_absolute_markovian_eps0.5":
        return 'green'
    elif agent == "MW_relative_markovian_eps0.5":
        return 'blue'
    elif agent == "MW_absolute_eps0.3":
        return 'lightgreen'
    elif agent == "MW_relative_eps0.3":
        return 'lightblue'


if __name__ == "__main__":
    # get game names from log-file
    logfile = open("log.txt", "r")
    logs = logfile.read()
    games = logs.split(";")[:-1]
    logfile.close()

    agents = []
    # for i in range(len(games)):
    if True:
        i = len(games)-1
        fp = games[i]
        agent = fp.split("--")[-1]
        agents.append(agent)
        game = pkl_read(f"./games/{fp}.pkl")
        col = color(agent)
        plt.plot(game.win_loss_ratio, col, label=agent)

    plt.ylim((0, 3))
    plt.xlabel('Number of Rounds')
    plt.ylabel('Win-Loss-ratio')
    plt.plot([0, 100], [1, 1], 'black')  # plot horizontal line
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    plt.show()