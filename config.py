import os

#******************************
#******** Enviroment **********
#******************************

ENV_NAME = 'Pendulum-v0'


PATH_SAVE_MODEL = "../model/{}/".format(ENV_NAME)
PATH_LOAD_FOLDER = "../model/simple_tag/save_agent_202105031925/"


BUFFER_CAPACITY = 30
BATCH_SIZE = 10
MIN_SIZE_BUFFER = 25

CRITIC_HIDDEN_0 = 256
CRITIC_HIDDEN_1 = 128
ACTOR_HIDDEN_0 = 256 
ACTOR_HIDDEN_1 = 128
ACTOR_HIDDEN_2 = 128
CRITIC_HIDDEN_2 = 128

ACTOR_LR = 0.001
CRITIC_LR = 0.001
GAMMA = 0.1
TAU = 0.001

MAX_GAMES = 20
MAX_STEPS = 60
EVALUATION_FREQUENCY = 500
SAVE_FREQUENCY = 25000