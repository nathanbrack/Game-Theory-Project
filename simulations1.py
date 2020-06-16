from agents import *
from rock_paper_scissors import *

import matplotlib.pyplot as plt


M = 10 # number of simulations
N = 2000 # number of rounds played each simulation
eps = 0.5 # tuning parameter: exploration (small eps) vs. exploitation (big eps)

for i in range(M):
    p1 = MW_absolute_markovian(3, 3, eps)
    p2 = Fixed_absolute_markovian(3, np.array(([0.5, 0.25, 0.25], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5])))
    game = RPSGame(p1, p2)

    for j in range(N):
        game.play_round()

    print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")
    plt.plot(game.win_loss_ratio, 'lightgray')

plt.ylim((0,3))
plt.xlabel('Number of Rounds')
plt.ylabel('Win-Loss-ratio')
plt.suptitle('Simulation of Rock Paper Scissors: MW Markovian vs. fixed Markovian')
plt.plot([0,N], [1,1], 'black') # plot horizontal line
plt.show()

