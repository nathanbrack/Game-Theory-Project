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
        return 'gray', 'Uniform random'
    elif agent == "Fixed_absolute_markovian":
        return 'gray', 'Fixed Absolute Markovian'
    elif agent == "Fixed_relative_markovian":
        return 'gray', 'Fixed Relative Markovian'
    elif agent == "MW_absolute_markovian_eps0.5":
        return 'darkgreen', 'Absolute Markovian Agent with epsilon = 0.5'
    elif agent == "MW_relative_markovian_eps0.5":
        return 'darkred', 'Relative Markovian Agent with epsilon = 0.5'
    elif agent == "MW_absolute_eps0.3":
        return 'green', 'Absolute Markovian Agent with epsilon = 0.3'
    elif agent == "MW_relative_eps0.3":
        return 'red', 'Relative Markovian Agent with epsilon = 0.3'


if __name__ == "__main__":
    # get game names from log-file
    logfile = open("log.txt", "r")
    logs = logfile.read()
    games = logs.split(";")[:-1]
    logfile.close()

    # plot "confidence interval" grey area
    M = 500  # number of simulations
    N = 100  # number of rounds played each simulation
    eps = 0.5  # tuning parameter: exploration (small eps) vs. exploitation (big eps)

    for i in range(M):
        p1 = Uniform_random(3)
        p2 = Uniform_random(3)
        game = RPSGame(p1, p2)

        for j in range(N):
            game.play_round()

        print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")
        plt.plot(game.win_loss_ratio, 'lightgray')

    plt.ylim((0, 3))
    plt.xlabel('Number of Rounds')
    plt.ylabel('Win-Loss-ratio')
    plt.suptitle('Simulation of Rock Paper Scissors: MW Markovian vs. fixed Markovian')


    agents = []
    for i in range(len(games)):
        fp = games[i]
        agent = fp.split("--")[-1]
        agents.append(agent)
        if agent.find("MW_a") >= 0: # plot only MW-based agents
            game = pkl_read(f"./games/{fp}.pkl")
            col, lab = color(agent)
            plt.plot(game.win_loss_ratio, col, label=lab)


    plt.plot([0, 100], [1, 1], 'blue')  # plot horizontal line
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    plt.show()