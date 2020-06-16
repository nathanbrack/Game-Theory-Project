import numpy as np


def RPS_cost(adversary_action):
    """returns cost vector for Rock Paper Scissors
    adversary_action=[0:rock 1:paper 2:scissors]"""
    if adversary_action == 0:
        return np.array([0, -1, 1])
    if adversary_action == 1:
        return np.array([1, 0, -1])
    if adversary_action == 2:
        return np.array([-1, 1, 0])


def RPS_winner(a1, a2):
    if a1 == a2:  # tie
        return 0
    if (a1 + 1) % 3 != a2:  # a1 wins
        return 1
    return -1


class RPSGame():
    def __init__(self, strategy1, strategy2):
        self.strategy1 = strategy1
        self.strategy2 = strategy2

        self.game_history = []
        self.win_loss_ratio = []

        self.ties = 0
        self.wins1 = 0
        self.losses1 = 0

    def play_round(self):
        a1 = self.strategy1.get_action()
        a2 = self.strategy2.get_action()

        c1 = RPS_cost(a2)
        c2 = RPS_cost(a1)

        outcome = RPS_winner(a1, a2)

        self.strategy1.update(c1, own_action=a1, adv_action=a2, game_outcome=outcome)
        self.strategy2.update(c2, own_action=a2, adv_action=a1, game_outcome=-1*outcome)

        if outcome == 1:
            self.wins1 += 1
        elif outcome == -1:
            self.losses1 += 1
        else:
            self.ties += 1

        self.game_history.append((a1, a2))
        if self.losses1 > 0:
            self.win_loss_ratio.append(self.wins1 / self.losses1)
        else:
            self.win_loss_ratio.append(None)

        return outcome