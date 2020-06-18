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

########### Anna
""" 
Cumulative Costs and Regret Calculations:
Assume regret to be nonnegative. Hence map costvector from {-1,0,1} to {0,0.5,1}
"""
def map_costs(c):
    if c == -1:
        c = 0
    elif c == 0:
        c = 1
    elif c == 1:
        c = 2
    return c


def actual_cum_cost(game_history,cost1_history,cost2_history):
    """return the actual cumulative costs for player 1 and player 2"""
    cum_c1 = 0
    cum_c2 = 0
    for i in range(len(game_history)):
        a1_t = game_history[i][0] # action of player1 in round t
        c1_t = map_costs(cost1_history[i][a1_t]) # costs of action a1_t
        cum_c1 += c1_t # sum up costs of player1's actions over all rounds
        print(cum_c1)
        # analogous for player2
        a2_t = game_history[i][1]
        c2_t = map_costs(cost2_history[i][a2_t]) # costvector of player1 is the complment of player2's cost vector
        cum_c2 += c2_t
        print(cum_c2)
    return cum_c1, cum_c2

def best_cost_in_hindsight(cost1_history,cost2_history):
    # return costs of best action in hindsight
    c11_t = 0
    c12_t = 0
    c13_t = 0
    c21_t = 0
    c22_t = 0
    c23_t = 0
    for i in range(len(cost1_history)):
        c11_t += map_costs(cost1_history[i][0])
        c12_t += map_costs(cost1_history[i][1])
        c13_t += map_costs(cost1_history[i][2])
        c21_t += map_costs(cost2_history[i][0])
        c22_t += map_costs(cost2_history[i][1])
        c23_t += map_costs(cost2_history[i][2])
    best_cum_c1 = min(c11_t,c12_t,c13_t)
    best_cum_c2 = min(c21_t,c22_t,c23_t)
    return best_cum_c1, best_cum_c2

def regret(cum_cost,best_cum_cost,T):
    return 1/T*(cum_cost-best_cum_cost)


#######

class RPSGame():
    def __init__(self, strategy1, strategy2):
        self.strategy1 = strategy1
        self.strategy2 = strategy2

        self.game_history = []
        self.win_loss_ratio = []
        self.costs = []
        self.cost1_history = []
        self.cost2_history = []

        self.ties = 0
        self.wins1 = 0
        self.losses1 = 0

    def play_round(self):
        a1 = self.strategy1.get_action()
        a2 = self.strategy2.get_action()

        c1 = RPS_cost(a2)
        c2 = RPS_cost(a1)
        self.cost1_history.append(c1)
        self.cost2_history.append(c2)

        outcome = RPS_winner(a1, a2)

        self.strategy1.update(c1, own_action=a1, adv_action=a2, game_outcome=outcome)
        self.strategy2.update(c2, own_action=a2, adv_action=a1, game_outcome=-1*outcome)

        if outcome == 1:
            self.wins1 += 1
        elif outcome == -1:
            self.losses1 += 1
        else:
            self.ties += 1

        self.costs.append(outcome)
        self.game_history.append((a1, a2))
        if self.losses1 > 0:
            self.win_loss_ratio.append(self.wins1 / self.losses1)
        else:
            self.win_loss_ratio.append(None)

        return outcome