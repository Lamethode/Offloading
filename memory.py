import tensorflow as tf
import numpy as np
import os
import json


class ReplayBuffer_Serv():
    def __init__(self,buffer_capacity, batch_size,n_agents,states,actions):
        #liste_dir,liste_dir_task=liste_dir,liste_dir_task
        self.n_agents=n_agents
        states=states
        actions=actions
        self.buffer_capacity = buffer_capacity
        self.batch_size = batch_size
        self.buffer_counter = 0
        self.n_games = 0
        self.list_actors_dimension=[states[index].shape[0] for index in range(len(self.n_agents))]
        self.critic_dimension=sum(self.list_actors_dimension)
        self.list_actor_n_actions=[actions[index].ndim for index in range(len(self.n_agents))]
        
        self.states = np.zeros((self.buffer_capacity, self.critic_dimension))
        self.rewards = np.zeros((self.buffer_capacity, len(self.n_agents)))
        self.next_states = np.zeros((self.buffer_capacity, self.critic_dimension))
        
        self.list_actors_states = []
        self.list_actors_next_states = []
        self.list_actors_actions = []
        
        for n in range(len(self.n_agents)):
            self.list_actors_states.append(np.zeros((self.buffer_capacity, self.list_actors_dimension[n])))
            self.list_actors_next_states.append(np.zeros((self.buffer_capacity, self.list_actors_dimension[n])))
            self.list_actors_actions.append(np.zeros((self.buffer_capacity, self.list_actor_n_actions[n])))

        


    def __len__(self):
        return self.buffer_counter
        
    def check_buffer_size(self):
        return self.buffer_counter >= self.batch_size 
    
    def update_n_games(self):
        self.n_games += 1
          
    def add_record(self, actor_states, actor_next_states, actions, state, next_state, reward):
        
        index = self.buffer_counter % self.buffer_capacity
        
        for agent_index in range(len(self.n_agents)):
            self.list_actors_states[agent_index][index] = actor_states[agent_index]
            self.list_actors_next_states[agent_index][index] = actor_next_states[agent_index]
            self.list_actors_actions[agent_index][index] = actions[agent_index]
        
        self.states[index] = state
        self.next_states[index] = next_state
        self.rewards[index] = reward
            
        self.buffer_counter += 1


    def get_minibatch(self):
        # If the counter is less than the capacity we don't want to take zeros records, 
        # if the cunter is higher we don't access the record using the counter 
        # because older records are deleted to make space for new one
        buffer_range = min(self.buffer_counter, self.buffer_capacity)

        batch_index = np.random.choice(buffer_range, self.batch_size, replace=False)

        # Take indices
        state = self.states[batch_index]
        reward = self.rewards[batch_index]
        next_state = self.next_states[batch_index]
        done = self.dones[batch_index]
            
        actors_state = [self.list_actors_states[index][batch_index] for index in range(self.n_agents)]
        actors_next_state = [self.list_actors_next_states[index][batch_index] for index in range(self.n_agents)]
        actors_action = [self.list_actors_actions[index][batch_index] for index in range(self.n_agents)]

        return state, reward, next_state, actors_state, actors_next_state, actors_action
    
    def save(self, folder_path):
        """
        Save the replay buffer
        """
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
        np.save(folder_path + '/states.npy', self.states)
        np.save(folder_path + '/rewards.npy', self.rewards)
        np.save(folder_path + '/next_states.npy', self.next_states)
        
        for index in range(self.n_agents):
            np.save(folder_path + '/states_actor_{}.npy'.format(index), self.list_actors_states[index])
            np.save(folder_path + '/next_states_actor_{}.npy'.format(index), self.list_actors_next_states[index])
            np.save(folder_path + '/actions_actor_{}.npy'.format(index), self.list_actors_actions[index])
            
        dict_info = {"buffer_counter": self.buffer_counter, "n_games": self.n_games}
        
        with open(folder_path + '/dict_info.json', 'w') as f:
            json.dump(dict_info, f)
            
    def load(self, folder_path):
        self.states = np.load(folder_path + '/states.npy')
        self.rewards = np.load(folder_path + '/rewards.npy')
        self.next_states = np.load(folder_path + '/next_states.npy')

        
        self.list_actors_states = [np.load(folder_path + '/states_actor_{}.npy'.format(index)) for index in range(self.n_agents)]
        self.list_actors_next_states = [np.load(folder_path + '/next_states_actor_{}.npy'.format(index)) for index in range(self.n_agents)]
        self.list_actors_actions = [np.load(folder_path + '/actions_actor_{}.npy'.format(index)) for index in range(self.n_agents)]
        
        with open(folder_path + '/dict_info.json', 'r') as f:
            dict_info = json.load(f)
        self.buffer_counter = dict_info["buffer_counter"]
        self.n_games = dict_info["n_games"]


class ReplayBuffer_Task():
    def __init__(self,buffer_capacity, batch_size,n_agents,liste_dir_task,liste_dir,env_task,data_rate_liste_v,data_rate_liste_i,liste_tu,price_task_u,ressource):
        self.buffer_capacity = buffer_capacity
        liste_dir,env_task,data_rate_liste_v,data_rate_liste_i,liste_tu,price_task_u=liste_dir,env_task,data_rate_liste_v,data_rate_liste_i,liste_tu,price_task_u
        liste_dir_task=liste_dir_task
        ressource=ressource
        self.batch_size = batch_size
        self.buffer_counter = 0
        self.n_games = 0
        self.n_agents =n_agents
        self.list_actors_dimension=[0 for p in range(len(liste_dir_task))]
        self.critic_dimension=[0 for p in range(len(liste_dir_task))]
        self.list_actor_n_actions=[0 for p in range(len(liste_dir_task))]
        
        self.list_actors_states=[[] for p in range(len(liste_dir_task))]
        self.list_actors_next_states=[[] for p in range(len(liste_dir_task))]
        self.list_actors_actions=[[] for p in range(len(liste_dir_task))]
        for p in range(len(liste_dir_task)):
            self.list_actors_dimension[p] = [len(n_agents[0].state_space(n_agents,env_task,data_rate_liste_v,data_rate_liste_i,liste_dir,liste_dir_task,liste_tu,price_task_u)[p][index]) for index in range(liste_dir_task[p])]
            #[len(state_space()[1][i]) for i in range(liste_dir_task[1])]
            self.critic_dimension[p] = sum(self.list_actors_dimension[p])        
            self.list_actor_n_actions[p] = [len(n_agents[0].action_space(ressource)[p][index]) for index in range(liste_dir_task[p])]

            self.states = np.zeros((int(self.buffer_capacity/4), self.critic_dimension[p]))
            self.rewards = np.zeros((int(self.buffer_capacity/4), liste_dir_task[p]))
            self.next_states = np.zeros((int(self.buffer_capacity/4), self.critic_dimension[p]))
            #self.dones = np.zeros((self.buffer_capacity, self.n_agents), dtype=bool)

            #self.list_actors_states[p]
            #self.list_actors_next_states[p]
            #self.list_actors_actions[p]

        for p in range(len(liste_dir_task)):
          for n in range(liste_dir_task[p]):
                  self.list_actors_states[p].append(np.zeros((int(self.buffer_capacity/4), self.list_actors_dimension[p][n])))
                  self.list_actors_next_states[p].append(np.zeros((int(self.buffer_capacity/4), self.list_actors_dimension[p][n])))
                  self.list_actors_actions[p].append(np.zeros((int(self.buffer_capacity/4), self.list_actor_n_actions[p][n])))


    def __len__(self):
        return self.buffer_counter
        
    def check_buffer_size(self):
        return self.buffer_counter >= self.batch_size 
    
    def update_n_games(self):
        self.n_games += 1
          
    def add_record(self, actor_states, actor_next_states, actions, state, next_state, reward):
        
        index = self.buffer_counter % self.buffer_capacity
        self.rewards=0
        for agent_index in range(self.n_agents):
            self.list_actors_states[agent_index][index] = actor_states[agent_index]
            self.list_actors_next_states[agent_index][index] = actor_next_states[agent_index]
            self.list_actors_actions[agent_index][index] = actions[agent_index]
        
            self.states[index] = state[index]
            self.next_states[index] = next_state[index]
        self.rewards += reward
            
        self.buffer_counter += 1


    def get_minibatch(self):
        # If the counter is less than the capacity we don't want to take zeros records, 
        # if the cunter is higher we don't access the record using the counter 
        # because older records are deleted to make space for new one
        buffer_range = min(self.buffer_counter, self.buffer_capacity)

        batch_index = np.random.choice(buffer_range, self.batch_size, replace=False)

        # Take indices
        state = self.states[batch_index]
        reward = self.rewards[batch_index]
        next_state = self.next_states[batch_index]
        done = self.dones[batch_index]
            
        actors_state = [self.list_actors_states[index][batch_index] for index in range(self.n_agents)]
        actors_next_state = [self.list_actors_next_states[index][batch_index] for index in range(self.n_agents)]
        actors_action = [self.list_actors_actions[index][batch_index] for index in range(self.n_agents)]

        return state, reward, next_state, actors_state, actors_next_state, actors_action
    
    def save(self, folder_path):
        """
        Save the replay buffer
        """
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
        np.save(folder_path + '/states.npy', self.states)
        np.save(folder_path + '/rewards.npy', self.rewards)
        np.save(folder_path + '/next_states.npy', self.next_states)
        
        for index in range(self.n_agents):
            np.save(folder_path + '/states_actor_{}.npy'.format(index), self.list_actors_states[index])
            np.save(folder_path + '/next_states_actor_{}.npy'.format(index), self.list_actors_next_states[index])
            np.save(folder_path + '/actions_actor_{}.npy'.format(index), self.list_actors_actions[index])
            
        dict_info = {"buffer_counter": self.buffer_counter, "n_games": self.n_games}
        
        with open(folder_path + '/dict_info.json', 'w') as f:
            json.dump(dict_info, f)
            
    def load(self, folder_path):
        self.states = np.load(folder_path + '/states.npy')
        self.rewards = np.load(folder_path + '/rewards.npy')
        self.next_states = np.load(folder_path + '/next_states.npy')

        
        self.list_actors_states = [np.load(folder_path + '/states_actor_{}.npy'.format(index)) for index in range(self.n_agents)]
        self.list_actors_next_states = [np.load(folder_path + '/next_states_actor_{}.npy'.format(index)) for index in range(self.n_agents)]
        self.list_actors_actions = [np.load(folder_path + '/actions_actor_{}.npy'.format(index)) for index in range(self.n_agents)]
        
        with open(folder_path + '/dict_info.json', 'r') as f:
            dict_info = json.load(f)
        self.buffer_counter = dict_info["buffer_counter"]
        self.n_games = dict_info["n_games"]