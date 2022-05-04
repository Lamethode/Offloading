import os

#******************************
#******** Enviroment **********
#******************************

ENV_NAME = 'simple_tag'


PATH_SAVE_MODEL = "../model/{}/".format(ENV_NAME)
PATH_LOAD_FOLDER = "../model/simple_tag/save_agent_202105031925/"


BUFFER_CAPACITY = 500
BATCH_SIZE = 10
MIN_SIZE_BUFFER = 25

CRITIC_HIDDEN_0 = 256
CRITIC_HIDDEN_1 = 128
ACTOR_HIDDEN_0 = 256 
ACTOR_HIDDEN_1 = 128
ACTOR_HIDDEN_2 = 128 
CRITIC_HIDDEN_2 = 128

ACTOR_LR = 0.01
CRITIC_LR = 0.01
GAMMA = 0.95
TAU = 0.01

MAX_GAMES = 20
MAX_STEPS = 60
EVALUATION_FREQUENCY = 500
SAVE_FREQUENCY = 25000