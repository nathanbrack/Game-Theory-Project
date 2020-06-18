# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:19:52 2020

@author: Admin
"""

import numpy 
import random
rng = numpy.random.default_rng()
#np.random.default_rng()


np.ones(10)
n_actions=[1,2,3]
weights=np.ones(3)/3
rng.choice(n_actions, p=weights)


print(numpy.__version__)

getattr(numpy.random)
from numpy import random as default_rng


from numpy.random import Generator

