from agents import *
from rock_paper_scissors import *
import pandas as pd
from datetime import datetime
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl

#%%

M = 10 # number of simulations
N = 2000 # number of rounds played each simulation
eps = 0.5 # tuning parameter: exploration (small eps) vs. exploitation (big eps)

for i in range(M):
    p1 = MW_absolute_markovian(3, 3, eps)
    p2 = Uniform_random(3)
    #p2 = MW_absolute(3,eps)
    #p2 = Fixed_absolute_markovian(3, np.array(([0.5, 0.25, 0.25], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5])))
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


for i in range(5):
    print("round:",i+1)
    print(game.game_history[i])
    print(game.cost1_history[i])
    print(game.cost2_history[i])


actual_cost = actual_cum_cost(game.game_history,game.cost1_history,game.cost2_history)
best_cost = best_cost_in_hindsight(game.cost1_history,game.cost2_history)
regret1 = regret(actual_cost[0],best_cost[0],N)
regret2 = regret(actual_cost[1],best_cost[1],N)

def map_costs(c):
    if c == -1:
        c = 0
    elif c == 0:
        c= 0.5
    return c


def test_actual_cum_cost(game_history,cost1_history,cost2_history):
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


actual_cost = test_actual_cum_cost(game.game_history,game.cost1_history,game.cost2_history)
best_cost = best_cost_in_hindsight(game.cost1_history,game.cost2_history)
regret1 = regret(actual_cost[0],best_cost[0],N)
regret2 = regret(actual_cost[1],best_cost[1],N)


"""
c_types = [(0,-1,1),(1,0,-1),(-1,1,0)]
    cost1_history = tuple(map(tuple, cost1_history)) # convert np.array entry to tuples
    cost2_history = tuple(map(tuple, cost2_history)) # convert np.array entry to tuples
    # returns counts of each cost vector type   
    counts1 = np.array([cost1_history.count(c_types[0]),cost1_history.count(c_types[1]),cost1_history.count(c_types[2])])
    counts2 = np.array([cost2_history.count(c_types[0]),cost2_history.count(c_types[1]),cost2_history.count(c_types[2])])
    # returns argmin of the cost vector type with least counts
    min_counts1=np.argmin(counts1)
    min_counts2=np.argmin(counts2)
    # returns the argmax of the minimal counts cost vector, i.e the best action in hindsight
    best_a1=np.argmax(c_types[min_counts1])
    best_a2=np.argmax(c_types[min_counts2])
"""
# Charlotte
#%%
########## Anna
def game_sims(p1,p2,no_sims,no_rounds_per_sim):

    # initialize dictionary we will save data in
    dic = {}
    stats_dict = {}
    
    for j in range(no_sims):
        game = RPSGame(p1, p2)
        
        col = ['game no','player 1','player 2','outcome (pl1)','w/l']
        df = pd.DataFrame(np.zeros((no_rounds_per_sim,5)) ,columns=col)
        
        for i in range(no_rounds_per_sim): 
            game.play_round()
            df.iloc[i,0] = i
            df.iloc[i,1] = game.game_history[i][0]
            df.iloc[i,2] = game.game_history[i][1]
            df.iloc[i,3] = game.costs[i]
            df.iloc[i,4] = game.win_loss_ratio[i]
        
        dic[j] = df
        
        # collect stats after each simulation
        game.losses1    
        game.wins1
        game.ties
        actual_cost = actual_cum_cost(game.game_history,game.cost1_history,game.cost2_history)
        best_cost = best_cost_in_hindsight(game.cost1_history,game.cost2_history)
        regret1 = regret(actual_cost[0],best_cost[0],no_rounds_per_sim)
        regret2 = regret(actual_cost[1],best_cost[1],no_rounds_per_sim)
        
        # save stats in pd.Series
        index = ['wins1','losses1','ties','actual_costs','best_costs','regret1','regret2']
        data = [game.wins1,game.losses1 ,game.ties,actual_cost,best_cost,regret1,regret2]
        stats = pd.Series(data, index=index)
        
        stats_dict[j] = stats
        
    return dic, stats_dict
#########
#%%

# tuning parameter which we need to decide about 
eps = 0.5
adj_mat = np.array(([0.5, 0.25, 0.25], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5]))

# define the different agents 
p1 = Uniform_random(3)
p2 = MW_absolute(3,eps)
p3 = MW_relative(3,eps)
p4 = MW_absolute_markovian(3,3,eps)
p5 = MW_relative_markovian(3,3,eps)
p6 = Fixed_absolute_markovian(3,adj_mat)
p7 = Fixed_relative_markovian(3,adj_mat)
 

#%%
test1,test2 = game_sims(p4,p6,3,8)
game_sims(p1,p3,3,8)
game_sims(p1,p4,3,8)
game_sims(p2,p5,3,8)
game_sims(p6,p3,3,8)

"""
def pkl_save(fp, obj_history, obj_stats):
    with open(fp, 'wb') as f:
        pkl.dump(obj_history,obj_stats, f)
        
timestr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
fp = f"./{timestr}.pkl"
    
pkl_save(fp, test1,test2)
"""
#%%
# example Nathan 
p1 = MW_absolute_markovian(3, 3, eps)
p2 = Fixed_absolute_markovian(3, np.array(([0.5, 0.25, 0.25], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5])))

game_sims(p1,p2,3,8)

#%%
N = 200 # number of rounds played each simulation
eps = 0.5 # tuning parameter: exploration (small eps) vs. exploitation (big eps)


p1 = MW_absolute_markovian(3, 3, eps)
p2 = Fixed_absolute_markovian(3, np.array(([0.5, 0.25, 0.25], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5])))
game = RPSGame(p1, p2)

for j in range(N):
    game.play_round()
    
# collect stats
game.losses1    
game.wins1
game.ties
actual_cost = actual_cost(game.game_history,game.cost1_history,game.cost2_history)
best_cost = best_cost_in_hindsight(game.cost1_history,game.cost2_history)
regret1 = regret(actual_cost[0],best_cost[0],N)
regret2 = regret(actual_cost[1],best_cost[1],N)

# save stats in pd.Series
index = ['wins1','losses1','ties','actual_costs','best_costs','regret1','regret2']
data = [game.wins1,game.losses1 ,game.ties,actual_cost,best_cost,regret1,regret2]
stats = pd.Series(data, index=index)


        
        for i in range(no_rounds_per_sim): 
            game.play_round()
            df.iloc[i,0] = i
            df.iloc[i,1] = game.game_history[i][0]
            df.iloc[i,2] = game.game_history[i][1]
            df.iloc[i,3] = game.costs[i]
            df.iloc[i,4] = game.win_loss_ratio[i]


#    print(f"Wins:{game.wins1}\tLosses:{game.losses1}\tTies:{game.ties}")

