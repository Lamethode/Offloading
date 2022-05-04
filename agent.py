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
from network import *


class Agent_serv:
    
    def __init__(self,vehicule_service,i,state,price_base, actor_lr=ACTOR_LR, critic_lr=CRITIC_LR, gamma=GAMMA, tau=TAU):
       #######################SERVICE#########################################################"" 
        self.gamma = gamma
        self.tau = tau
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr
        self.i=i
        self.state=state
        self.state=np.array(state)
        self.action=np.array(price_base)
        self.actor_dims = self.state.shape[2]
        self.n_actions = self.action.shape[2]
        
        self.agent_name = "agent_number_{}".format(self.i)
        
        self.actor = Actor("actor_" + self.agent_name, self.n_actions)
        self.critic = Critic("critic_" + self.agent_name)
        self.target_actor = Actor("target_actor_" + self.agent_name, self.n_actions)
        self.target_critic = Critic("critic_" + self.agent_name)
        
        self.actor.compile(optimizer=opt.Adam(learning_rate=actor_lr))
        self.critic.compile(optimizer=opt.Adam(learning_rate=critic_lr))
        self.target_actor.compile(optimizer=opt.Adam(learning_rate=actor_lr))
        self.target_critic.compile(optimizer=opt.Adam(learning_rate=critic_lr))
        
        actor_weights = self.actor.get_weights()
        critic_weights = self.critic.get_weights()
        
        self.target_actor.set_weights(actor_weights)
        self.target_critic.set_weights(critic_weights)
        
    def update_target_networks(self, tau):
        actor_weights = self.actor.weights
        target_actor_weights = self.target_actor.weights
        for index in range(len(actor_weights)):
            target_actor_weights[index] = tau * actor_weights[index] + (1 - tau) * target_actor_weights[index]

        self.target_actor.set_weights(target_actor_weights)
        
        critic_weights = self.critic.weights
        target_critic_weights = self.target_critic.weights
    
        for index in range(len(critic_weights)):
            target_critic_weights[index] = tau * critic_weights[index] + (1 - tau) * target_critic_weights[index]

        self.target_critic.set_weights(target_critic_weights)

    def save(self, path_save):
        self.actor.save_weights(f"{path_save}/{self.actor.net_name}.h5")
        self.target_actor.save_weights(f"{path_save}/{self.target_actor.net_name}.h5")
        self.critic.save_weights(f"{path_save}/{self.critic.net_name}.h5")
        self.target_critic.save_weights(f"{path_save}/{self.target_critic.net_name}.h5")
        
    def load(self, path_load):
        self.actor.load_weights(f"{path_load}/{self.actor.net_name}.h5")
        self.target_actor.load_weights(f"{path_load}/{self.target_actor.net_name}.h5")
        self.critic.load_weights(f"{path_load}/{self.critic.net_name}.h5")
        self.target_critic.load_weights(f"{path_load}/{self.target_critic.net_name}.h5")
        
        """def get_actions(self, actor_states):
        noise = tf.random.uniform(shape=[self.n_actions])
        actions = self.actor(actor_states)
        actions = actions + noise

        return actions.numpy()[0]"""

    # définir get state

    


    def train(self):

        state, reward, next_state, actors_state, actors_next_state, actors_action = self.replay_buffer.get_minibatch()
        
        states = tf.convert_to_tensor(state, dtype=tf.float32)
        rewards = tf.convert_to_tensor(reward, dtype=tf.float32)
        next_states = tf.convert_to_tensor(next_state, dtype=tf.float32)
        
        actors_states = [tf.convert_to_tensor(s, dtype=tf.float32) for s in actors_state]
        actors_next_states = [tf.convert_to_tensor(s, dtype=tf.float32) for s in actors_next_state]
        actors_actions = [tf.convert_to_tensor(s, dtype=tf.float32) for s in actors_action]
        
        with tf.GradientTape(persistent=True) as tape:
            target_actions = [self.agents[index].target_actor(actors_next_states[index]) for index in range(self.n_agents)]
            policy_actions = [self.agents[index].actor(actors_states[index]) for index in range(self.n_agents)]
            
            concat_target_actions = tf.concat(target_actions, axis=1)
            concat_policy_actions = tf.concat(policy_actions, axis=1)
            concat_actors_action = tf.concat(actors_actions, axis=1)
            
            target_critic_values = [tf.squeeze(self.agents[index].target_critic(next_states, concat_target_actions), 1) for index in range(self.n_agents)]
            critic_values = [tf.squeeze(self.agents[index].critic(states, concat_actors_action), 1) for index in range(self.n_agents)]
            targets = [rewards[:, index] + self.agents[index].gamma * target_critic_values[index] * (1-done[:, index]) for index in range(self.n_agents)]
            critic_losses = [tf.keras.losses.MSE(targets[index], critic_values[index]) for index in range(self.n_agents)]
            
            actor_losses = [-self.agents[index].critic(states, concat_policy_actions) for index in range(self.n_agents)]
            actor_losses = [tf.math.reduce_mean(actor_losses[index]) for index in range(self.n_agents)]
        
        critic_gradients = [tape.gradient(critic_losses[index], self.agents[index].critic.trainable_variables) for index in range(self.n_agents)]
        actor_gradients = [tape.gradient(actor_losses[index], self.agents[index].actor.trainable_variables) for index in range(self.n_agents)]
        
        for index in range(self.n_agents):
            self.agents[index].critic.optimizer.apply_gradients(zip(critic_gradients[index], self.agents[index].critic.trainable_variables))
            self.agents[index].actor.optimizer.apply_gradients(zip(actor_gradients[index], self.agents[index].actor.trainable_variables))
            self.agents[index].update_target_networks(self.agents[index].tau)
     #######################SERVICE#########################################################""



class Agent_Task:
    def __init__(self, env_serv,vehicule_service ,n_agent, actor_lr=ACTOR_LR, critic_lr=CRITIC_LR, gamma=GAMMA, tau=TAU):
       #######################SERVICE#########################################################"" 
        n_agent=vehicule_tache.nombre
        self.gamma = gamma
        self.tau = tau
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr
        
        self.actor_dims = len(self.state_space[n_agent])
        self.n_actions = len(ServiceVehicle.action_space[n_agent])
        
        self.agent_name = "agent_number_{}".format(n_agent)
        
        self.actor = Actor("actor_" + self.agent_name, self.n_actions)
        self.critic = Critic("critic_" + self.agent_name)
        self.target_actor = Actor("target_actor_" + self.agent_name, self.n_actions)
        self.target_critic = Critic("critic_" + self.agent_name)
        
        self.actor.compile(optimizer=opt.Adam(learning_rate=actor_lr))
        self.critic.compile(optimizer=opt.Adam(learning_rate=critic_lr))
        self.target_actor.compile(optimizer=opt.Adam(learning_rate=actor_lr))
        self.target_critic.compile(optimizer=opt.Adam(learning_rate=critic_lr))
        
        actor_weights = self.actor.get_weights()
        critic_weights = self.critic.get_weights()
        
        self.target_actor.set_weights(actor_weights)
        self.target_critic.set_weights(critic_weights)
        
    def update_target_networks(self, tau):
        actor_weights = self.actor.weights
        target_actor_weights = self.target_actor.weights
        for index in range(len(actor_weights)):
            target_actor_weights[index] = tau * actor_weights[index] + (1 - tau) * target_actor_weights[index]

        self.target_actor.set_weights(target_actor_weights)
        
        critic_weights = self.critic.weights
        target_critic_weights = self.target_critic.weights
    
        for index in range(len(critic_weights)):
            target_critic_weights[index] = tau * critic_weights[index] + (1 - tau) * target_critic_weights[index]

        self.target_critic.set_weights(target_critic_weights)

    def save(self, path_save):
        self.actor.save_weights(f"{path_save}/{self.actor.net_name}.h5")
        self.target_actor.save_weights(f"{path_save}/{self.target_actor.net_name}.h5")
        self.critic.save_weights(f"{path_save}/{self.critic.net_name}.h5")
        self.target_critic.save_weights(f"{path_save}/{self.target_critic.net_name}.h5")
        
    def load(self, path_load):
        self.actor.load_weights(f"{path_load}/{self.actor.net_name}.h5")
        self.target_actor.load_weights(f"{path_load}/{self.target_actor.net_name}.h5")
        self.critic.load_weights(f"{path_load}/{self.critic.net_name}.h5")
        self.target_critic.load_weights(f"{path_load}/{self.target_critic.net_name}.h5")
        
        """def get_actions(self, actor_states):
        noise = tf.random.uniform(shape=[self.n_actions])
        actions = self.actor(actor_states)
        actions = actions + noise

        return actions.numpy()[0]"""

    # définir get state




    


    def train(self):

        state, reward, next_state, actors_state, actors_next_state, actors_action = self.replay_buffer.get_minibatch()
        
        states = tf.convert_to_tensor(state, dtype=tf.float32)
        rewards = tf.convert_to_tensor(reward, dtype=tf.float32)
        next_states = tf.convert_to_tensor(next_state, dtype=tf.float32)
        
        actors_states = [tf.convert_to_tensor(s, dtype=tf.float32) for s in actors_state]
        actors_next_states = [tf.convert_to_tensor(s, dtype=tf.float32) for s in actors_next_state]
        actors_actions = [tf.convert_to_tensor(s, dtype=tf.float32) for s in actors_action]
        
        with tf.GradientTape(persistent=True) as tape:
            target_actions = [self.agents[index].target_actor(actors_next_states[index]) for index in range(self.n_agents)]
            policy_actions = [self.agents[index].actor(actors_states[index]) for index in range(self.n_agents)]
            
            concat_target_actions = tf.concat(target_actions, axis=1)
            concat_policy_actions = tf.concat(policy_actions, axis=1)
            concat_actors_action = tf.concat(actors_actions, axis=1)
            
            target_critic_values = [tf.squeeze(self.agents[index].target_critic(next_states, concat_target_actions), 1) for index in range(self.n_agents)]
            critic_values = [tf.squeeze(self.agents[index].critic(states, concat_actors_action), 1) for index in range(self.n_agents)]
            targets = [rewards[:, index] + self.agents[index].gamma * target_critic_values[index] * (1-done[:, index]) for index in range(self.n_agents)]
            critic_losses = [tf.keras.losses.MSE(targets[index], critic_values[index]) for index in range(self.n_agents)]
            
            actor_losses = [-self.agents[index].critic(states, concat_policy_actions) for index in range(self.n_agents)]
            actor_losses = [tf.math.reduce_mean(actor_losses[index]) for index in range(self.n_agents)]
        
        critic_gradients = [tape.gradient(critic_losses[index], self.agents[index].critic.trainable_variables) for index in range(self.n_agents)]
        actor_gradients = [tape.gradient(actor_losses[index], self.agents[index].actor.trainable_variables) for index in range(self.n_agents)]
        
        for index in range(self.n_agents):
            self.agents[index].critic.optimizer.apply_gradients(zip(critic_gradients[index], self.agents[index].critic.trainable_variables))
            self.agents[index].actor.optimizer.apply_gradients(zip(actor_gradients[index], self.agents[index].actor.trainable_variables))
            self.agents[index].update_target_networks(self.agents[index].tau)
     #######################SERVICE#########################################################""
