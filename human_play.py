import random
import tkinter
from rock_paper_scissors import *
from agents import *
import pickle
from datetime import datetime

"""
inspired by https://code.sololearn.com/c2I4XIiO36yH/#py
"""

def pkl_save(fp, obj):
    with open(fp,'wb') as f:
        pickle.dump(obj, f)

class RPS_human_game():
    def __init__(self, opponent):
        self.strategy2 = opponent

        self.game_history = []
        self.cost2s = []

        self.ties = 0
        self.wins1 = 0
        self.losses1 = 0

    def play_round(self, a1):
        a2 = self.strategy2.get_action()
        c2 = RPS_cost(a1)

        outcome = RPS_winner(a1, a2)

        self.strategy2.update(c2, own_action=a2, adv_action=a1, game_outcome=-1*outcome)
        self.cost2s.append(c2)

        if outcome == 1:
            self.wins1 += 1
        elif outcome == -1:
            self.losses1 += 1
        else:
            self.ties += 1

        self.game_history.append((a1, a2))

        return a1, a2, outcome


def random_opponent():
    x = np.random.default_rng().choice(7)

    if x == 0:
        return Uniform_random(3), "Uniform_random"

    elif x == 1:
        return Fixed_absolute_markovian(3, np.array(([0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]))), "Fixed_absolute_markovian"

    elif x == 2:
        return Fixed_relative_markovian(3, np.array(([1/3, 1/3, 1/3], [1/3, 1/3, 1/3], [0.1, 0.1, .8]))), "Fixed_relative_markovian"

    elif x == 3:
        return MW_absolute_markovian(3, 3, 0.5), "MW_absolute_markovian_eps0.5"
        
    elif x == 4:
        return MW_relative_markovian(3, 3, 0.5), "MW_relative_markovian_eps0.5"

    elif x == 5:
        return MW_relative(3, 0.3), "MW_relative_eps0.3"
        
    elif x == 6:
        return MW_absolute(3, 0.3), "MW_absolute_eps0.3"
        



if __name__ == "__main__":
    n_rounds = 100
    eps = 0.5 # tuning parameter: exploration (small eps) vs. exploitation (big eps)
    opponent, name = random_opponent()

    timestr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fp = f"./games/{timestr}-{name}.pkl"

    game = RPS_human_game(opponent)

    window = tkinter.Tk()
    window.geometry("600x400")
    round = 0

    def update_window(a1, a2, outcome):
        global round
        global n_rounds
        if round >= n_rounds: # n_rounds have been played
            global window
            window.destroy()
            return

        round += 1
        actions = {0: "Rock", 1: "Paper", 2: "Scissors"}

        global output
        global stats

        if outcome == 1:
            ret = "You win!"
            output.config(text=f"{actions[a1]} vs. {actions[a2]}\n{ret}\n", fg="green")
        elif outcome == -1:
            ret = "You Loose!"
            output.config(text=f"{actions[a1]} vs. {actions[a2]}\n{ret}\n", fg="red")
        else:
            ret = "Tie!"
            output.config(text=f"{actions[a1]} vs. {actions[a2]}\n{ret}\n", fg="black")

        
        
        

        stats.config(text=f"Total: {round}/{n_rounds}\nWins: {game.wins1}\nLosses:{game.losses1}\nTies:{game.ties}\n")

        pkl_save(fp, game)
    
    def play_r():
        a1, a2, outcome = game.play_round(0)
        update_window(a1, a2, outcome)

    def play_p():
        a1, a2, outcome = game.play_round(1)
        update_window(a1, a2, outcome)

    def play_s():
        a1, a2, outcome = game.play_round(2)
        update_window(a1, a2, outcome)

    
    rock = tkinter.Button(window, text = "Rock", bg = "#80ff80", padx=10, pady=25, command=play_r, width=20)
    paper = tkinter.Button(window, text = "Paper", bg = "#3399ff", padx=10, pady=25, command=play_p, width=20)
    scissors = tkinter.Button(window, text = "Scissors", bg = "#ff9999", padx=10, pady=25, command=play_s, width=20)
    global output
    global stats
    output = tkinter.Label(window, width=20, fg = "red", text="What's your call?",font=("Courier", 30,"bold") )
    stats = tkinter.Label(window, width=20, fg = "black", text="",font=("Helvetica", 20) )

    
    rock.grid(column=0,row=2)
    paper.grid(column=1,row=2)
    scissors.grid(column=2,row=2)
    output.grid(column=0,row=4, columnspan=3)
    stats.grid(column=0,row=5, columnspan=3)
    window.mainloop()