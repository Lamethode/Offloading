import numpy as np
import tensorflow as tf
from tensorflow.keras import optimizers as opt
import random
import time
import json
import os
import sys
sys.path.append("../src")
from config import *
from env import *
from memory import *
from agent import *

class SuperAgent_serv:
    def __init__(self,vehicle_serv,serv_memory,state,price_base,liste_dir,path_save=PATH_SAVE_MODEL, path_load=PATH_LOAD_FOLDER):
        self.path_save = path_save
        vehicle_serv,serv_memory,state,price_base,liste_dir=vehicle_serv,serv_memory,state,price_base,liste_dir
        self.path_load = path_load
        self.replay_buffer = serv_memory
        self.agents = [[Agent_serv(vehicle_serv,j,state,price_base) for j in range(liste_dir[p])] for p in range(len(liste_dir))]
        
    def get_actions(self, agents_states):
        list_actions = [self.agents[index].get_actions(agents_states[index]) for index in range(self.n_agents)]
        return list_actions
    
    def save(self):
        date_now = time.strftime("%Y%m%d%H%M")
        full_path = f"{self.path_save}/save_agent_{date_now}"
        if not os.path.isdir(full_path):
            os.makedirs(full_path)
        
        for agent in self.agents:
            agent.save(full_path)
            
        self.replay_buffer.save(full_path)
    
    def load(self):
        full_path = self.path_load
        for agent in self.agents:
            agent.load(full_path)
            
        self.replay_buffer.load(full_path)