import numpy as np
import random
import copy

import gym
from gym.spaces import Discrete, Tuple, Box, Dict

class Stimulus:

    def __init__(self, id: int, emo_intensity: int, p_recurrence: float):
        self.id = id
        self.emo_intensity = emo_intensity
        self.p_recurrence = p_recurrence
        self.reappraised = False

    def get_intensity(self):
        return self.emo_intensity

    def get_dict(self):
        return {'id': self.id, 'emo_intensity': self.emo_intensity, "p_recurrence": self.p_recurrence}


class AgentStatus:

    def __init__(self):
        self.stimuliAppraisals = list()
        self.current_id = None
        self.current_emo_intensity = None
        self.expected_p_recurrence = None
        self.previous_encounter = None

    def print_list(self):
        for i in range(len(self.stimuliAppraisals)):
            print(self.stimuliAppraisals[i].get_dict())

    def appraise_stimuli(self, stimulus: Stimulus):  # currently the appraisal function is 1:1, so just a copy
        self._check_for_previous_encounter(stimulus)
        if not self.previous_encounter:
            self.stimuliAppraisals.append(copy.deepcopy(stimulus))
        self._update_emotional_state(stimulus)

    def _check_for_previous_encounter(self, stimulus):
        for i in range(0, len(self.stimuliAppraisals)):
            if self.stimuliAppraisals[i].id == stimulus.id:
                self.previous_encounter = True
            else:
                self.previous_encounter = False

    def _update_emotional_state(self, stimulus):
        for i in range(0, len(self.stimuliAppraisals)):
            if self.stimuliAppraisals[i].id == stimulus.id:
                self.current_emo_intensity = self.stimuliAppraisals[i].emo_intensity
                self.expected_p_recurrence = self.stimuliAppraisals[i].p_recurrence
                self.current_id = self.stimuliAppraisals[i].id






class EmotionEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    N_ACTIONS = 3

    # Actions
    INACTION = 0
    DISENGAGE = 1
    ENGAGE = 2

    def __init__(self,
                 engage_delay: float,
                 engage_benefit: float,
                 disengage_benefit: float,
                 engage_adaptation: float,
                 current_timepoint: float,
                 stimuli: list,
                 agent_status: AgentStatus
                 ):

        super(EmotionEnv, self).__init__()

        self.action_space = Discrete(self.N_ACTIONS)
        self.observation_space = Dict({'stimulus_id': Discrete(len(stimuli)),
        'emo_intensity': Box(low=0, high=10, shape=(1,), dtype=np.float32),
        'emo_step:': Box(low=0, high=2, shape=(1,), dtype=np.int8)})

        self.stimuli = stimuli
        self.n_stimuli = len(stimuli)
        self.engage_delay = engage_delay
        self.engage_benefit = engage_benefit
        self.engage_adaptation = engage_adaptation
        self.disengage_benefit = disengage_benefit
        self.current_timepoint = current_timepoint
        self.agent_status = agent_status

        self.reset()

    def step(self, action: int) -> tuple:
        '''
        Execute one timestep in environment
        :param action: which action to take
        :return: state, reward, done, info
        '''
        # Take action
        if action == self.DISENGAGE:
            self._disengage()
        elif action == self.ENGAGE:
            self._engage()
        elif action == self.INACTION:
            self._inaction()
        else:
            raise ValueError(f'Received invalid action {action} which is not part of the action space')

        info = None
        self.current_timepoint += 1

        if self._get_doneness():
            done = 1
            self.reset()
        else:
            done = 0

        return self.agent_status, self._get_reward(), done, info

    def _inaction(self):
        return self.agent_status

    def _disengage(self):
        self.agent_status.current_emo_intensity -= self.disengage_benefit
        return self.agent_status

    def _engage(self):
        if self.current_timepoint < self.engage_delay:
            self.agent_status.current_emo_intensity -= self.engage_benefit
        else:
            for i in range(0, len(self.agent_status.stimuliAppraisals)):
                if self.agent_status.stimuliAppraisals[i].id == self.agent_status.current_id:
                    if not self.agent_status.stimuliAppraisals[i].reappraised:
                        self.agent_status.stimuliAppraisals[i].emo_intensity -= self.engage_adaptation
                        self.agent_status.current_emo_intensity -= self.engage_adaptation
                        self.agent_status.stimuliAppraisals[i].reappraised = True
                    else:
                        self.agent_status.current_emo_intensity -= self.engage_benefit

        return self.agent_status

    def _get_reward(self):
        reward = -1 * self.agent_status.current_emo_intensity
        return reward

    def _get_doneness(self):
        return True if self.current_timepoint == 2 else False
#
#     def reset(self):
#         if self.current_emotion is not None:
#             # TODO: not sure if this is necessary, is this pointing to same object when random choices are made?
#             self.current_emotion.reset()
#         self.current_emotion = random.choice(self.stimuli)
#
#     def render(self, mode='human'):
#         '''
#
#         :param mode:
#         :return:
#         '''
#         if mode != 'human':
#             raise NotImplementedError()
#         print(f'{self.current_emotion.get_dict()}')
