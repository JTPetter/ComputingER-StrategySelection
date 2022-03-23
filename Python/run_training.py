import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import path

from environment import Stimulus, AgentStatus, EmotionEnv
from agent import QTableAgent

random.seed(123)
np.random.seed(123)

#for seed in np.arange(1, 9, 1):

N_RUNS = 10000
N_STIMULI = 2000

engage_delay = 1
engage_benefit = 0
disengage_benefit = 2
engage_adaptation = 4

# p_recurrence does not do anything at the moment
stimuli_list = [random.choice(
    [Stimulus(id=i, emo_intensity=8, p_recurrence=1),
     Stimulus(id=i, emo_intensity=3, p_recurrence=.5),
     Stimulus(id=i, emo_intensity=5, p_recurrence=1),
     Stimulus(id=i, emo_intensity=7, p_recurrence=.8)]
) for i in range(N_STIMULI)]

#     stimuli = [random.choice(
#         [Emotion(id=i, emo_trajectory=[.8, .8, .8], p_recurrence=1/N_STIMULI),
#          Emotion(id=i, emo_trajectory=[.3, .3, .3], p_recurrence=1/N_STIMULI)]
#     ) for i in range(N_STIMULI)]

agent_status = AgentStatus()

env = EmotionEnv(engage_delay=engage_delay,
                 engage_benefit=engage_benefit,
                 disengage_benefit=disengage_benefit,
                 engage_adaptation=engage_adaptation,
                 stimuli=stimuli_list,
                 agent_status=agent_status
                 )
n_actions = 3
alpha = .001
gamma = .99
epsilon = .1


agent = QTableAgent(env.n_stimuli, n_actions=3, alpha=alpha, gamma=gamma, epsilon=epsilon)

state = agent_status.current_id
action = agent.choose_action(state)

# Record actions and rewards
action_counts = np.zeros((N_RUNS, agent.n_actions))
reward_counts = np.zeros((N_RUNS, agent.n_actions))
zero_counts = np.zeros(N_RUNS)

# Run simulation
for i in range(N_RUNS):
    env.render()
    next_state, reward, done, info = env.step(action)
    agent.update(state, next_state, action, reward)
    print(f'action: {action}, reward: {reward}, step: {i}')
    env.render()
    action_counts[i, action] += 1
    reward_counts[i, action] += reward
    if done:
        env.reset()
        action = agent.choose_action(state)


# Plot choices
time = np.arange(0, N_RUNS)
action_cumsum = np.cumsum(action_counts, axis=0)
plt.plot(time, action_cumsum[:, 0], marker='', color='olive', linewidth=2, label='inaction')
plt.plot(time, action_cumsum[:, 1], marker='', color='blue', linewidth=2, label='disengage')
plt.plot(time, action_cumsum[:, 2], marker='', color='red', linewidth=2, label='engage')
plt.legend()
plt.show()

# plot rewards
inaction_timeline = np.cumsum(reward_counts[:, 0] != 0) + 1
disengage_timeline = np.cumsum(reward_counts[:, 1] != 0) + 1
engage_timeline = np.cumsum(reward_counts[:, 2] != 0) + 1
reward_cumsum = np.cumsum(reward_counts, axis=0)
reward_cumsum[:, 0] / np.arange(1, N_RUNS + 1, 1)
plt.plot(time, reward_cumsum[:, 0]/inaction_timeline, marker='', color='olive', linewidth=2, label='inaction')
plt.plot(time, reward_cumsum[:, 1]/disengage_timeline, marker='', color='blue', linewidth=2, label='disengage')
plt.plot(time, reward_cumsum[:, 2]/engage_timeline, marker='', color='red', linewidth=2, label='engage')
plt.legend()
plt.show()



# set options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df1 = pd.DataFrame({'inaction': action_cumsum[:, 0], 'disengange': action_cumsum[:, 1], 'engange': action_cumsum[:, 2]})
file_name1='no_engage_benefit_high_adapt_actions' + ".csv"  #+ str(seed)
df1.to_csv(file_name1)

df2 = pd.DataFrame({'inaction': reward_cumsum[:, 0]/inaction_timeline, 'disengange': reward_cumsum[:, 1]/disengage_timeline,
                    'engange': reward_cumsum[:, 2]/engage_timeline})
file_name2='no_engage_benefit_high_adapt_rewards' + ".csv"  #+ str(seed)
df2.to_csv(file_name2)