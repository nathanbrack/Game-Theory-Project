import numpy as np


class MW():
    def __init__(self, n_actions, eps):
        self.eps = eps
        self.n_actions = n_actions
        self.weights = np.ones(n_actions) / n_actions
        self.rng = np.random.default_rng()

    def get_action(self):
        return self.rng.choice(self.n_actions, p=self.weights)

    def update(self, cost, *args):
        factor = np.power((1 - self.eps), cost)
        self.weights *= factor

        self.weights /= self.weights.sum()


class MW_markovian():
    def __init__(self, n_actions, n_states, eps):
        self.eps = eps
        self.n_actions = n_actions
        self.n_states = n_states
        self.weights = np.ones((n_states, n_actions)) / n_actions
        self.rng = np.random.default_rng()

        # start with unifrom probability in any action
        self.state = None

    def get_action(self):
        if self.state is not None:
            a = self.rng.choice(self.n_actions, p=self.weights[self.state])
        else:
            a = self.rng.choice(self.n_states)
        return a

    def update(self, cost, adv_action):
        factor = np.power((1 - self.eps), cost)
        if self.state is not None:
            self.weights[self.state] *= factor

            self.weights[self.state] /= self.weights[self.state].sum()

        self.state = adv_action


class Uniform_random():
    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.rng = np.random.default_rng()

    def get_action(self):
        return self.rng.choice(self.n_actions)

    def update(self, *args):
        pass


class Markovian_fixed():
    def __init__(self, n_actions, transition_p):
        assert transition_p.shape == (n_actions, n_actions)
        self.n_actions = n_actions
        self.transition_p = transition_p
        self.rng = np.random.default_rng()

        # start with unifrom probability in any action
        self.state = self.rng.choice(self.n_actions)

    def get_action(self, update_state=True):
        a = self.rng.choice(self.n_actions, p=self.transition_p[self.state])
        if update_state:
            self.state = a
        return a

    def update(self, *args):
        pass

