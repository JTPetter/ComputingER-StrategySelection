import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import path

from environment import Stimulus, AgentStatus, EmotionEnv
from agent import QTableAgent


random.seed(123)
np.random.seed(123)

N_RUNS = 10000
N_STIMULI = 2000

# p_recurrence does not do anything at the moment
stimuli_list = [Stimulus(id=1, emo_intensity=8, p_recurrence=1),
                Stimulus(id=2, emo_intensity=3, p_recurrence=.5),
                Stimulus(id=3, emo_intensity=5, p_recurrence=1),
                Stimulus(id=4, emo_intensity=7, p_recurrence=.8)]

agent_status = AgentStatus()
# some testing
# stimuli_list[0].emo_intensity
agent_status.appraise_stimuli(stimuli_list[0])
# agent_emotion.current_id
# agent_emotion.current_emo_intensity
# agent_emotion.current_emo_intensity = 10
# agent_emotion.previous_encounter
# agent_emotion.print_list()
# agent_emotion.stimuliAppraisals[0].emo_intensity = 4

agent_status.current_emo_intensity
agent_status.stimuliAppraisals[1].emo_intensity

env = EmotionEnv(engage_delay=1,
                 engage_benefit=2,
                 disengage_benefit=5,
                 engage_adaptation=3,
                 stimuli=stimuli_list,
                 agent_status=agent_status
                 )

#env.agent_status.current_emo_intensity
env.render()
env.current_timepoint
next_state, reward, done, info = env.step(action=2)
agent_status.print_list()
env.reset()
env.current_timepoint

next_state.current_emo_intensity
next_state.stimuliAppraisals[1].emo_intensity
next_state.stimuliAppraisals[1].reappraised

for i in range(0, len(agent_status.stimuliAppraisals)):
    if agent_status.stimuliAppraisals[i].id == stimuli_list[0].id:
        print(True)
    else:
        print(False)

# #for eng_adapt in np.arange(0, .9, .1):
# if __name__ == '__main__':
#     N_RUNS = 10000
#     N_STIMULI = 2000 # Ratio of N_RUNS/N_STIMULI determines how likely agent is to re-encounter stimuli
#
#     # Create a set of stimuli which the agent will encounter
#     stimuli = [random.choice(
#         [Emotion(id=i, emo_trajectory=[.8, .8, .8], p_recurrence=1/N_STIMULI),
#          Emotion(id=i, emo_trajectory=[.3, .3, .3], p_recurrence=1/N_STIMULI)]
#     ) for i in range(N_STIMULI)]
#
#     # Here goes the appraisal function of the agent, currently 1:1 mapping
#
# #stimulus = Emotion(id=1, emo_trajectory=[.3, .3, .3], p_recurrence=1)
#     # Set parameters for environment
#     env = EmotionEnv(
#         engage_delay=1,
#         engage_benefit=0,
#         disengage_benefit=1,
#         engage_adaptation=0,
#         stimuli=stimuli
#     )
#     # Set parameters for agent
#     agent = QTableAgent(env.n_stimuli, env.N_ACTIONS, alpha=.001, gamma=.99, epsilon=.1)
#
#     state = env.current_emotion.id
#
#     # Record actions and rewards
#     action_counts = np.zeros((N_RUNS, agent.n_actions))
#     reward_counts = np.zeros((N_RUNS, agent.n_actions))
#     zero_counts = np.zeros(N_RUNS)
#
#     # Run simulation
#     for i in range(N_RUNS):
#
#         # env.render()
#         #if (i + 3) % 3 == 0:
#         action = agent.choose_action(state)
#         next_state, reward, done, info = env.step(action)
#         agent.update(state, next_state, action, reward)
#         print(f'action: {action}, reward: {reward}, step: {i}')
#         # env.render()
#         print(env.current_emotion.get_dict())
#
#         action_counts[i, action] += 1
#         reward_counts[i, action] += reward
#         # count and show how many stimuli are set to [0, 0, 0]
#         for stimulus in env.stimuli:
#             if sum(stimulus.emo_trajectory) == 0:
#                 zero_counts[i] += 1
#         print(zero_counts)
#
#
#     print(f'actions: {np.sum(action_counts, axis=0)}')
#     print(f'rewards: {np.sum(reward_counts, axis=0) / np.sum(action_counts, axis=0)}')
#
#
#     # Plot choices
#     time = np.arange(0, N_RUNS)
#     action_cumsum = np.cumsum(action_counts, axis=0)
#     #zero_cumsum = np.cumsum(zero_counts, axis=0)
#     # plt.plot(time, action_cumsum[:, 0], marker='', color='olive', linewidth=2, label='inaction')
#     # plt.plot(time, action_cumsum[:, 1], marker='', color='blue', linewidth=2, label='disengage')
#     # plt.plot(time, action_cumsum[:, 2], marker='', color='red', linewidth=2, label='engage')
#     # plt.legend()
#     # plt.show()
#
#     #set options for pandas
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.width', None)
#     pd.set_option('display.max_colwidth', None)
#
#     df = pd.DataFrame({'inaction': action_cumsum[:, 0], 'disengange': action_cumsum[:, 1], 'engange': action_cumsum[:, 2], 'zero_stimuli': zero_counts})
#     file_name='no_benefits_but_disengage' + ".csv"  #str(eng_adapt) +
#     df.to_csv(file_name)
#
