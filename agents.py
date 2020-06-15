import numpy as np

class Agent():
    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.rng = np.random.default_rng()

    def get_action(self):
        return -1

    def update(self, cost, **kwargs):
        pass


class MW_absolute(Agent):
    def __init__(self, n_actions, eps):
        super().__init__(n_actions)
        self.eps = eps
        self.weights = np.ones(n_actions) / n_actions
        

    def get_action(self):
        return self.rng.choice(self.n_actions, p=self.weights)

    def update(self, cost, **kwargs):
        factor = np.power((1 - self.eps), cost)
        self.weights *= factor

        self.weights /= self.weights.sum()


class MW_relative(Agent):
    def __init__(self, n_actions, eps):
        super().__init__(n_actions)
        self.eps = eps
        self.weights = np.ones(n_actions) / n_actions

        self.last_adv_action = None
        
    def get_action(self):
        a = self.rng.choice(self.n_actions, p=self.weights)
        # make aktion relative to previous round i.e. 
        # 0: play what adv played
        # 1: play what would have won (winning strategy)
        # 2: play what would have lost (losing strategy)

        if self.last_adv_action is not None:
            a = (a + self.last_adv_action) % 3

        return a

    def update(self, cost, adv_action, **kwargs):
        if self.last_adv_action is not None:
            # make cost relative to self.last_adv_action
            cost = np.roll(cost, -1 * self.last_adv_action)
            # print(cost)

            factor = np.power((1 - self.eps), cost)
            # print(factor)
            self.weights *= factor
            self.weights /= self.weights.sum()

            # print(self.weights)

        self.last_adv_action = adv_action


class MW_absolute_markovian(Agent):
    def __init__(self, n_actions, n_states, eps):
        super().__init__(n_actions)

        self.eps = eps
        self.n_states = n_states
        self.weights = np.ones((n_states, n_actions)) / n_actions

        # start with uniform probability in any action
        self.state = None

    def get_action(self):
        if self.state is not None:
            a = self.rng.choice(self.n_actions, p=self.weights[self.state])
        else:
            a = self.rng.choice(self.n_actions)
        return a

    def update(self, cost, adv_action, **kwargs):
        if self.state is not None:
            factor = np.power((1 - self.eps), cost)
            self.weights[self.state] *= factor

            self.weights[self.state] /= self.weights[self.state].sum()

        self.state = adv_action


class MW_relative_markovian(Agent):
    # important: states are not the last adv action, but the outcome (win, loss, tie) of the previous game 
    def __init__(self, n_actions, n_states, eps):
        super().__init__(n_actions)
        self.eps = eps
        self.n_states = n_states
        self.weights = np.ones((n_states, n_actions)) / n_actions

        # start with uniform probability in any action
        self.state = None
        self.last_adv_action = None

    def get_action(self):
        if self.state is not None:
            a = self.rng.choice(self.n_actions, p=self.weights[self.state])
            # make aktion relative to previous round i.e. 
            # 0: play what adv played
            # 1: play what would have won (winning strategy)
            # 2: play what would have lost (losing strategy)
            a = (a + self.last_adv_action) % 3
        else:
            a = self.rng.choice(self.n_actions)
        return a

    def update(self, cost, adv_action, game_outcome, **kwargs):
        if self.state is not None and self.last_adv_action is not None:
            cost = np.roll(cost, -1 * self.last_adv_action)
            factor = np.power((1 - self.eps), cost)
            
            self.weights[self.state] *= factor

            self.weights[self.state] /= self.weights[self.state].sum()

        self.state = game_outcome+1
        # 0: prev game was loss
        # 1: prev game was tie
        # 2: prev game was win
        
        self.last_adv_action = adv_action

        print(kwargs)


class Uniform_random(Agent):
    def __init__(self, n_actions):
        super().__init__(n_actions)        

    def get_action(self):
        return self.rng.choice(self.n_actions)

class Fixed_absolute_markovian(Agent):
    def __init__(self, n_actions, transition_p):
        assert transition_p.shape == (n_actions, n_actions)
        super().__init__(n_actions)
        self.transition_p = transition_p

        # start with unifrom probability in any action
        self.state = None

    def get_action(self):
        if self.state is not None:
            a = self.rng.choice(self.n_actions, p=self.transition_p[self.state])
        else:
            a = self.rng.choice(self.n_actions)
            
        return a

    def update(self, cost, own_action, **kwargs):
        self.state = own_action

class Fixed_relative_markovian(Agent):
    def __init__(self, n_actions, transition_p):
        assert transition_p.shape == (n_actions, n_actions)
        super().__init__(n_actions)
        self.transition_p = transition_p

        self.state = None
        self.last_adv_action = None

    def get_action(self, update_state=True):
        if self.state is not None:
            a = self.rng.choice(self.n_actions, p=self.transition_p[self.state])
            # make aktion relative to previous round i.e. 
            # 0: play what adv played
            # 1: play what would have won (winning strategy)
            # 2: play what would have lost (losing strategy)
            a = (a + self.last_adv_action) % 3
        else:
            a = self.rng.choice(self.n_actions)

        return a

    def update(self, cost, adv_action, game_outcome, **kwargs):
        self.state = game_outcome+1
        self.last_adv_action = adv_action