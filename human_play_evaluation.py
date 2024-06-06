import pickle
import matplotlib as plt
plt.use("pgf")
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
plt.rcParams['text.usetex'] = True

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
        return 'blue', 'Absolute Markovian Agent'
    elif agent == "MW_relative_markovian_eps0.5":
        return 'blue', 'Relative Markovian Agent'
    elif agent == "MW_absolute_eps0.3":
        return 'green', 'Basic Absolute Agent'
    elif agent == "MW_relative_eps0.3":
        return 'green', 'Basic Relative Agent'


if __name__ == "__main__":
    type = input("Do you want to evaluate the Absolute or the Relative Markovian Agent? Type 'a' or 'r'.\n")

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

        plt.pyplot.plot(game.win_loss_ratio, 'lightgray')

    plt.pyplot.ylim((0, 3))
    plt.pyplot.xlabel('Number of Rounds')
    plt.pyplot.ylabel('Win-Loss-ratio')
    #plt.pyplot.suptitle('Humans performance against Markovian Agents')


    agents = []
    for i in range(len(games)):
        fp = games[i]
        agent = fp.split("--")[-1]
        agents.append(agent)
        if agent.find(f'MW_{type}') >= 0: # plot only MW-based agents
            game = pkl_read(f"./games/{fp}.pkl")
            col, lab = color(agent)
            plt.pyplot.plot(game.win_loss_ratio, col, label=lab)


    plt.pyplot.plot([0, 100], [1, 1], 'red')  # plot horizontal line
    handles, labels = plt.pyplot.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.pyplot.legend(by_label.values(), by_label.keys(), loc='upper right')
    plt.pyplot.savefig('Humans_vs_Agents.pgf')
    plt.pyplot.savefig('demo.png', bbox_inches='tight')
    print("See demo.png for the evaluation plot.")