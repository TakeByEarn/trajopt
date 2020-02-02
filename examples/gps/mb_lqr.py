import autograd.numpy as np

import gym

from trajopt.gps import MBGPS
from trajopt.gps.objects import Gaussian, LinearGaussianControl

import warnings
warnings.filterwarnings("ignore")


# lqr task
env = gym.make('LQR-TO-v0')
env._max_episode_steps = 100000

dm_state = env.observation_space.shape[0]
dm_act = env.action_space.shape[0]

horizon, nb_steps = 25, 100

state = np.zeros((dm_state, nb_steps + 1))
action = np.zeros((dm_act, nb_steps))
init_action = LinearGaussianControl(dm_state, dm_act, horizon, 5.)

state[:, 0] = env.reset()
for t in range(nb_steps):
    solver = MBGPS(env, init_state=tuple([state[:, t], 1e-16 * np.eye(dm_state)]),
                   init_action_sigma=5., nb_steps=horizon, kl_bound=1.)
    trace = solver.run(nb_iter=25, verbose=False)

    _nominal_action = solver.udist.mu

    action[:, t] = _nominal_action[:, 0]
    state[:, t + 1], _, _, _ = env.step(action[:, t])

    print('Time Step:', t, 'Cost:', trace[-1])


import matplotlib.pyplot as plt

plt.figure()

plt.subplot(3, 1, 1)
plt.plot(state[0, :], '-b')
plt.subplot(3, 1, 2)
plt.plot(state[1, :], '-b')

plt.subplot(3, 1, 3)
plt.plot(action[0, :], '-g')

plt.show()
