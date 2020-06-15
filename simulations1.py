from agents import *
from rock_paper_scissors import *

# self play
p1 = MW_markovian(3, 3, 0.05)
p2 = MW_markovian(3, 3, 0.05)

game = RPSGame(p1, p2)

for i in range(100):
    game.play_round()

print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")
print(p1.weights)
print(p2.weights)

# play against non markovian learner
p1 = MW_markovian(3, 3, 0.05)
p2 = MW(3, 0.05)

game = RPSGame(p1, p2)

for i in range(100):
    game.play_round()

print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")
print(p1.weights)
print(p2.weights)

# play against optimal random

p1 = MW_markovian(3, 3, 0.05)
p2 = Uniform_random(3)

game = RPSGame(p1, p2)

for i in range(100):
    game.play_round()

print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")
print(p1.weights)


# play against biased markovian that prefers to play the last action

p1 = MW_markovian(3, 3, 0.05)
p2 = Markovian_fixed(3,np.array(([0.5,0.25,0.25], [0.25,0.5,0.25], [0.25,0.25,0.5])))

game = RPSGame(p1, p2)

for i in range(1000):
    game.play_round()

print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")
print(p1.weights)
