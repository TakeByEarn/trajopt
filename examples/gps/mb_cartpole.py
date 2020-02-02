import autograd.numpy as np

import gym

from trajopt.gps import MBGPS

import warnings
warnings.filterwarnings("ignore")


# cartpole env
env = gym.make('Cartpole-TO-v0')
env._max_episode_steps = 10000
env.unwrapped._dt = 0.01

dm_state = env.observation_space.shape[0]
dm_act = env.action_space.shape[0]

horizon, nb_steps = 50, 500

state = np.zeros((dm_state, nb_steps + 1))
action = np.zeros((dm_act, nb_steps))

state[:, 0] = env.reset()
for t in range(nb_steps):
    solver = MBGPS(env, init_state=tuple([state[:, t], 1e-16 * np.eye(dm_state)]),
                   init_action_sigma=5., nb_steps=horizon, kl_bound=0.1)
    trace = solver.run(nb_iter=10, verbose=False)

    _nominal_action = solver.udist.mu

    action[:, t] = _nominal_action[:, 0]
    state[:, t + 1], _, _, _ = env.step(action[:, t])

    print('Time Step:', t, 'Cost:', trace[-1])


import matplotlib.pyplot as plt

plt.figure()

plt.subplot(65, 1, 1)
plt.plot(state[0, :], '-b')
plt.subplot(5, 1, 2)
plt.plot(state[1, :], '-b')

plt.subplot(5, 1, 3)
plt.plot(state[2, :], '-r')
plt.subplot(5, 1, 4)
plt.plot(state[3, :], '-r')

plt.subplot(5, 1, 5)
plt.plot(action[0, :], '-g')

plt.show()
