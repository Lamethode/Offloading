#@title

""" Mise en place de l environnement pour notre projet IOV"""
import numpy as np
import time
import random
import math

from numpy.random.mtrand import laplace
from vehicle import *
from cloud import *

class Environnement_task :
  """ Configuration de l'environnement"""

  def __init__(self, down_lane, up_lane, left_lane, right_lane, width, height, n_task, n_neighbor):
        self.timestep = 0.01
        self.down_lanes = down_lane
        self.up_lanes = up_lane
        self.left_lanes = left_lane
        self.right_lanes = right_lane
        self.width = width
        self.height = height
        self.vehicles = []
        #self.demands = []   # a voir son impact
        self.delta_distance = [] # a mettre en place une distance delta mobile pour les RSU mobile et les véhicules de taches
        self.n_task = n_task
        self.n_neighbor = n_neighbor # les véhicules de types contraires
        #
        #
        self.eb_local=0.05
        self.y=0.26
        self.time_discount_factor=20
        self.expendure_discount_factor=0.15
        self.u_sucess=20

        
  def crossroad(self):
    return [0,0]



  def add_new_vehicles(self, start_position, start_direction, start_velocity,start_index):    
        self.vehicles.append(TaskVehicle(start_position, start_direction, start_velocity,start_index))

  def add_new_vehicles_by_number(self, n):
        g=0
        for i in range(n):
            index=i%int(n/4)+g
            ind = np.random.randint(0,len(self.down_lanes))
            start_position = [self.down_lanes[ind], random.randint(0,self.height)]
            start_direction = 'd'
            start_index=(0,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            start_position = [self.up_lanes[ind], random.randint(0,self.height)]
            start_direction = 'u'
            start_index=(1,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            start_position = [random.randint(0,self.width), self.left_lanes[ind]]
            start_direction = 'l'
            start_index=(2,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            start_position = [random.randint(0,self.width), self.right_lanes[ind]]
            start_direction = 'r'
            start_index=(3,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            g+=1

        #self.delta_distance = np.asarray([c.velocity*self.time_slow for c in self.vehicles])
  

  def renew_positions(self):
        # ========================================================
        # This function update the position of each vehicle
        # ===========================================================
        i = 0
        #for i in range(len(self.position)):
        while(i < len(self.vehicles)):
            #print ('start iteration ', i)
            #print(self.position, len(self.position), self.direction)
            delta_distance = self.vehicles[i].velocity * self.timestep
            change_direction = False
            if self.vehicles[i].direction == 'u':
                #print ('len of position', len(self.position), i)
                for j in range(len(self.left_lanes)):
                    
                    if (self.vehicles[i].position[1] <=self.left_lanes[j]) and ((self.vehicles[i].position[1] + delta_distance) >= self.left_lanes[j]):   # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.vehicles[i].position[0] - (delta_distance - (self.left_lanes[j] - self.vehicles[i].position[1])),self.left_lanes[j] ] 
                            self.vehicles[i].direction = 'l'
                            change_direction = True
                            break
                if change_direction == False :
                    for j in range(len(self.right_lanes)):
                        if (self.vehicles[i].position[1] <=self.right_lanes[j]) and ((self.vehicles[i].position[1] + delta_distance) >= self.right_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.vehicles[i].position[0] + (delta_distance + (self.right_lanes[j] - self.vehicles[i].position[1])), self.right_lanes[j] ] 
                                self.vehicles[i].direction = 'r'
                                change_direction = True
                                break
                if change_direction == False:
                    self.vehicles[i].position[1] += delta_distance
            if (self.vehicles[i].direction == 'd') and (change_direction == False):
                #print ('len of position', len(self.position), i)
                for j in range(len(self.left_lanes)):
                    if (self.vehicles[i].position[1] >=self.left_lanes[j]) and ((self.vehicles[i].position[1] - delta_distance) <= self.left_lanes[j]):  # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.vehicles[i].position[0] - (delta_distance - ( self.vehicles[i].position[1]- self.left_lanes[j])), self.left_lanes[j] ] 
                            #print ('down with left', self.vehicles[i].position)
                            self.vehicles[i].direction = 'l'
                            change_direction = True
                            break
                if change_direction == False :
                    for j in range(len(self.right_lanes)):
                        if (self.vehicles[i].position[1] >=self.right_lanes[j]) and (self.vehicles[i].position[1] - delta_distance <= self.right_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.vehicles[i].position[0] + (delta_distance + ( self.vehicles[i].position[1]- self.right_lanes[j])),self.right_lanes[j] ] 
                                #print ('down with right', self.vehicles[i].position)
                                self.vehicles[i].direction = 'r'
                                change_direction = True
                                break
                if change_direction == False:
                    self.vehicles[i].position[1] -= delta_distance
            if (self.vehicles[i].direction == 'r') and (change_direction == False):
                #print ('len of position', len(self.position), i)
                for j in range(len(self.up_lanes)):
                    if (self.vehicles[i].position[0] <= self.up_lanes[j]) and ((self.vehicles[i].position[0] + delta_distance) >= self.up_lanes[j]):   # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.up_lanes[j], self.vehicles[i].position[1] + (delta_distance - (self.up_lanes[j] - self.vehicles[i].position[0]))]
                            change_direction = True
                            self.vehicles[i].direction = 'u'
                            break
                if change_direction == False :
                    for j in range(len(self.down_lanes)):
                        if (self.vehicles[i].position[0] <= self.down_lanes[j]) and ((self.vehicles[i].position[0] + delta_distance) >= self.down_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.down_lanes[j], self.vehicles[i].position[1] - (delta_distance - (self.down_lanes[j] - self.vehicles[i].position[0]))]
                                change_direction = True
                                self.vehicles[i].direction = 'd'
                                break
                if change_direction == False:
                    self.vehicles[i].position[0] += delta_distance
            if (self.vehicles[i].direction == 'l') and (change_direction == False):
                for j in range(len(self.up_lanes)):
                    
                    if (self.vehicles[i].position[0] >= self.up_lanes[j]) and ((self.vehicles[i].position[0] - delta_distance) <= self.up_lanes[j]):   # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.up_lanes[j], self.vehicles[i].position[1] + (delta_distance - (self.vehicles[i].position[0] - self.up_lanes[j]))]
                            change_direction = True
                            self.vehicles[i].direction = 'u'
                            break
                if change_direction == False :
                    for j in range(len(self.down_lanes)):
                        if (self.vehicles[i].position[0] >= self.down_lanes[j]) and ((self.vehicles[i].position[0] - delta_distance) <= self.down_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.down_lanes[j], self.vehicles[i].position[1] - (delta_distance - (self.vehicles[i].position[0] - self.down_lanes[j]))]
                                change_direction = True
                                self.vehicles[i].direction = 'd'
                                break
                    if change_direction == False:
                        self.vehicles[i].position[0] -= delta_distance
            # if it comes to an exit
            if (self.vehicles[i].position[0] < 0) or (self.vehicles[i].position[1] < 0) or (self.vehicles[i].position[0] > self.width) or (self.vehicles[i].position[1] > self.height):
            # delete
            #    print ('delete ', self.position[i])
                if (self.vehicles[i].direction == 'u'):
                    self.vehicles[i].direction = 'r'
                    self.vehicles[i].position = [self.vehicles[i].position[0], self.right_lanes[-1]]
                else:
                    if (self.vehicles[i].direction == 'd'):
                        self.vehicles[i].direction = 'l'
                        self.vehicles[i].position = [self.vehicles[i].position[0], self.left_lanes[0]]
                    else:
                        if (self.vehicles[i].direction == 'l'):
                            self.vehicles[i].direction = 'u'
                            self.vehicles[i].position = [self.up_lanes[0],self.vehicles[i].position[1]]
                        else:
                            if (self.vehicles[i].direction == 'r'):
                                self.vehicles[i].direction = 'd'
                                self.vehicles[i].position = [self.down_lanes[-1],self.vehicles[i].position[1]]
                
            i += 1



  def renew_neighbor(self):   
        # ==========================================
        # update the neighbors of each vehicle.
        # ===========================================
        for i in range(len(self.vehicles)):
            self.vehicles[i].neighbors = []
            self.vehicles[i].actions = []
            #print('action and neighbors delete', self.vehicles[i].actions, self.vehicles[i].neighbors)
        Distance = np.zeros((len(self.vehicles),len(self.vehicles)))
        z = np.array([[complex(c.position[0],c.position[1]) for c in self.vehicles]])
        Distance = abs(z.T-z)
        for i in range(len(self.vehicles)):       
            sort_idx = np.argsort(Distance[:,i])
            for j in range(3):
                self.vehicles[i].neighbors.append(sort_idx[j+1])              
            destination = np.random.choice(sort_idx[1:int(len(sort_idx)/5)],3, replace = False)
            self.vehicles[i].destinations = destination

  def get_info(self):
        liste=[]
        for i in range(len(self.vehicles)):
          l=[]
          l.append(self.vehicles[i].position[0])
          l.append(self.vehicles[i].position[1])
          l.append(self.vehicles[i].velocity)
          liste.append(l)
        return liste

  def get_info_l(self,liste_dir_task):
     liste_dir_task
     liste=[]
     mm=[i for i in range(len(self.vehicles))]
     for p in range(len(liste_dir_task)):
       l=[]
       for i in range(liste_dir_task[p]):
         m=[]
         g=random.sample(mm,1)[0]
         m.append(self.vehicles[g].position[0])
         m.append(self.vehicles[g].position[1])
         m.append(self.vehicles[g].velocity)
         l.append(m)
       liste.append(l)
     return liste

     

   


  def get_update_info(self):
      liste=[]
      self.renew_positions() 
      for i in range(len(self.vehicles)):
        l=[]
        l.append(self.vehicles[i].position[0])
        l.append(self.vehicles[i].position[1])
        l.append(self.vehicles[i].velocity)
        liste.append(l)
      return liste
      
  def reward_task_vehicle(self,a,time_all,time_complete,p_pay,resource_purchase,unit_price_per_resource): 
      t=random.random()
      h=random.random()
      k=1-(t+h)
      while k<0:
        t=random.random()                         # time_all time_complete doivent etre des listes  ############ a faire ####################
        h=random.random()
        k=1-(t+h)
      self.price_sensitive_factor= t
      self.time_sensitive_factor= h
      self.sucess_sensitive_factor= k
      self.p_pay=p_pay
      self.time_all=time_all
      self.time_complete=time_complete
      self.resource_purchase=resource_purchase
      self.unit_price_per_resource=unit_price_per_resource

      return (self.time_sensitive_factor*self.time_discount_factor*math.ln(1+self.time_all-self.time_complete))-(self.price_sensitive_factor*self.expendure_discount_factor*((self.p_pay+self.eb_local)**(self.y)))+(self.sucess_sensitive_factor*self.u_sucess)


  def p_pay (self,ressource_required:list,list_price_sub_task_u:list): # number_total_list - nombre de la liste global des toutes les taches d'origine
    #som=0
    ressource_required=ressource_required
    list_price_sub_task_u=list_price_sub_task_u
    #list_sub_task_u=list_sub_task_u
    big_list=[]
    for p in range(len(liste_dir)):
        liste=[]
        for i in range(liste_dir_task[p]):
            som=0
            for j in range(liste_dir[p]):
                som=som+ressource_required[p][i][j]*list_price_sub_task_u[p][i][j]
            liste.append(som)
        big_list.append(liste)
    return big_list


      #def get_state_update(self):



###########################################################################################################################################################################################
# a revoir cette partie pour savoir si elle doit etre en dehors de la classe environnement ou etre dedans puis adapté

  def new_random_game(self, n_task=0):
        # make a new game

          self.vehicles = []
          if n_task > 0:
              self.n_task = n_task
          self.add_new_vehicles_by_number(int(self.n_task/4))
          self.renew_neighbor()

# définir la génération de taches, (fait)
#les différentes recompenses pour les environnements leader et foller (pas encore fait)
#diviser l'environnement en 2 () leader et follower


######################################################################## recompences pour les véhicules de taches##################################################################################


    

 
  ############################################################################################################################################################################################################################################

    




##########################################" Environnement service############################################################################################################################"""""
class Environnement_service:

    """ Configuration de l'environnement"""
      
    def __init__(self, down_lane, up_lane, left_lane, right_lane, width, height, n_serv, n_neighbor,Cloudserver):
        self.timestep = 0.01
        self.down_lanes = down_lane
        self.up_lanes = up_lane
        self.left_lanes = left_lane
        self.right_lanes = right_lane
        self.width = width
        self.height = height
        self.vehicles = []
        #self.demands = []   # a voir son impact
        self.delta_distance = [] # a mettre en place une distance delta mobile pour les RSU mobile et les véhicules de taches
        self.n_serv = n_serv
        self.n_neighbor = n_neighbor # les véhicules de types contraires

        
    def crossroad(self):
      return [0,0]



    def add_new_vehicles(self, start_position, start_direction, start_velocity,start_index):    
        self.vehicles.append(ServiceVehicle(start_position, start_direction, start_velocity,start_index))

    def add_new_vehicles_by_number(self, n):
        g=0
        for i in range(n):
            index=i%int(n/4)+g
            ind = np.random.randint(0,len(self.down_lanes))
            start_position = [self.down_lanes[ind], random.randint(0,self.height)]
            start_direction = 'd'
            start_index=(0,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            start_position = [self.up_lanes[ind], random.randint(0,self.height)]
            start_direction = 'u'
            start_index=(1,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            start_position = [random.randint(0,self.width), self.left_lanes[ind]]
            start_direction = 'l'
            start_index=(2,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            start_position = [random.randint(0,self.width), self.right_lanes[ind]]
            start_direction = 'r'
            start_index=(3,index)
            self.add_new_vehicles(start_position,start_direction,random.randint(30,50),start_index)
            g+=1

        #self.delta_distance = np.asarray([c.velocity*self.time_slow for c in self.vehicles])
  

    def renew_positions(self):
        # ========================================================
        # This function update the position of each vehicle
        # ===========================================================
        i = 0
        #for i in range(len(self.position)):
        while(i < len(self.vehicles)):
            #print ('start iteration ', i)
            #print(self.position, len(self.position), self.direction)
            delta_distance = self.vehicles[i].velocity * self.timestep
            change_direction = False
            if self.vehicles[i].direction == 'u':
                #print ('len of position', len(self.position), i)
                for j in range(len(self.left_lanes)):
                    
                    if (self.vehicles[i].position[1] <=self.left_lanes[j]) and ((self.vehicles[i].position[1] + delta_distance) >= self.left_lanes[j]):   # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.vehicles[i].position[0] - (delta_distance - (self.left_lanes[j] - self.vehicles[i].position[1])),self.left_lanes[j] ] 
                            self.vehicles[i].direction = 'l'
                            change_direction = True
                            break
                if change_direction == False :
                    for j in range(len(self.right_lanes)):
                        if (self.vehicles[i].position[1] <=self.right_lanes[j]) and ((self.vehicles[i].position[1] + delta_distance) >= self.right_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.vehicles[i].position[0] + (delta_distance + (self.right_lanes[j] - self.vehicles[i].position[1])), self.right_lanes[j] ] 
                                self.vehicles[i].direction = 'r'
                                change_direction = True
                                break
                if change_direction == False:
                    self.vehicles[i].position[1] += delta_distance
            if (self.vehicles[i].direction == 'd') and (change_direction == False):
                #print ('len of position', len(self.position), i)
                for j in range(len(self.left_lanes)):
                    if (self.vehicles[i].position[1] >=self.left_lanes[j]) and ((self.vehicles[i].position[1] - delta_distance) <= self.left_lanes[j]):  # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.vehicles[i].position[0] - (delta_distance - ( self.vehicles[i].position[1]- self.left_lanes[j])), self.left_lanes[j] ] 
                            #print ('down with left', self.vehicles[i].position)
                            self.vehicles[i].direction = 'l'
                            change_direction = True
                            break
                if change_direction == False :
                    for j in range(len(self.right_lanes)):
                        if (self.vehicles[i].position[1] >=self.right_lanes[j]) and (self.vehicles[i].position[1] - delta_distance <= self.right_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.vehicles[i].position[0] + (delta_distance + ( self.vehicles[i].position[1]- self.right_lanes[j])),self.right_lanes[j] ] 
                                #print ('down with right', self.vehicles[i].position)
                                self.vehicles[i].direction = 'r'
                                change_direction = True
                                break
                if change_direction == False:
                    self.vehicles[i].position[1] -= delta_distance
            if (self.vehicles[i].direction == 'r') and (change_direction == False):
                #print ('len of position', len(self.position), i)
                for j in range(len(self.up_lanes)):
                    if (self.vehicles[i].position[0] <= self.up_lanes[j]) and ((self.vehicles[i].position[0] + delta_distance) >= self.up_lanes[j]):   # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.up_lanes[j], self.vehicles[i].position[1] + (delta_distance - (self.up_lanes[j] - self.vehicles[i].position[0]))]
                            change_direction = True
                            self.vehicles[i].direction = 'u'
                            break
                if change_direction == False :
                    for j in range(len(self.down_lanes)):
                        if (self.vehicles[i].position[0] <= self.down_lanes[j]) and ((self.vehicles[i].position[0] + delta_distance) >= self.down_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.down_lanes[j], self.vehicles[i].position[1] - (delta_distance - (self.down_lanes[j] - self.vehicles[i].position[0]))]
                                change_direction = True
                                self.vehicles[i].direction = 'd'
                                break
                if change_direction == False:
                    self.vehicles[i].position[0] += delta_distance
            if (self.vehicles[i].direction == 'l') and (change_direction == False):
                for j in range(len(self.up_lanes)):
                    
                    if (self.vehicles[i].position[0] >= self.up_lanes[j]) and ((self.vehicles[i].position[0] - delta_distance) <= self.up_lanes[j]):   # came to an cross
                        if (random.uniform(0,1) < 0.4):
                            self.vehicles[i].position = [self.up_lanes[j], self.vehicles[i].position[1] + (delta_distance - (self.vehicles[i].position[0] - self.up_lanes[j]))]
                            change_direction = True
                            self.vehicles[i].direction = 'u'
                            break
                if change_direction == False :
                    for j in range(len(self.down_lanes)):
                        if (self.vehicles[i].position[0] >= self.down_lanes[j]) and ((self.vehicles[i].position[0] - delta_distance) <= self.down_lanes[j]):
                            if (random.uniform(0,1) < 0.4):
                                self.vehicles[i].position = [self.down_lanes[j], self.vehicles[i].position[1] - (delta_distance - (self.vehicles[i].position[0] - self.down_lanes[j]))]
                                change_direction = True
                                self.vehicles[i].direction = 'd'
                                break
                    if change_direction == False:
                        self.vehicles[i].position[0] -= delta_distance
            # if it comes to an exit
            if (self.vehicles[i].position[0] < 0) or (self.vehicles[i].position[1] < 0) or (self.vehicles[i].position[0] > self.width) or (self.vehicles[i].position[1] > self.height):
            # delete
            #    print ('delete ', self.position[i])
                if (self.vehicles[i].direction == 'u'):
                    self.vehicles[i].direction = 'r'
                    self.vehicles[i].position = [self.vehicles[i].position[0], self.right_lanes[-1]]
                else:
                    if (self.vehicles[i].direction == 'd'):
                        self.vehicles[i].direction = 'l'
                        self.vehicles[i].position = [self.vehicles[i].position[0], self.left_lanes[0]]
                    else:
                        if (self.vehicles[i].direction == 'l'):
                            self.vehicles[i].direction = 'u'
                            self.vehicles[i].position = [self.up_lanes[0],self.vehicles[i].position[1]]
                        else:
                            if (self.vehicles[i].direction == 'r'):
                                self.vehicles[i].direction = 'd'
                                self.vehicles[i].position = [self.down_lanes[-1],self.vehicles[i].position[1]]
                
            i += 1



    def renew_neighbor(self):   
        # ==========================================
        # update the neighbors of each vehicle.
        # ===========================================
        for i in range(len(self.vehicles)):
            self.vehicles[i].neighbors = []
            self.vehicles[i].actions = []
            #print('action and neighbors delete', self.vehicles[i].actions, self.vehicles[i].neighbors)
        Distance = np.zeros((len(self.vehicles),len(self.vehicles)))
        z = np.array([[complex(c.position[0],c.position[1]) for c in self.vehicles]])
        Distance = abs(z.T-z)
        for i in range(len(self.vehicles)):       
            sort_idx = np.argsort(Distance[:,i])
            for j in range(3):
                self.vehicles[i].neighbors.append(sort_idx[j+1])              
            destination = np.random.choice(sort_idx[1:int(len(sort_idx)/5)],3, replace = False)
            self.vehicles[i].destinations = destination
      
    def get_info(self):
        liste=[]
        for i in range(len(self.vehicles)):
          l=[]
          l.append(self.vehicles[i].position[0])
          l.append(self.vehicles[i].position[1])
          l.append(self.vehicles[i].velocity)
          liste.append(l)
        return liste

    def get_update_info(self):
        liste=[]
        self.renew_positions() 
        for i in range(len(self.vehicles)):
          l=[]
          l.append(self.vehicles[i].position[0])
          l.append(self.vehicles[i].position[1])
          l.append(self.vehicles[i].velocity)
          liste.append(l)
        return liste



    ###########################################################################################################################################################################################
    # a revoir cette partie pour savoir si elle doit etre en dehors de la classe environnement ou etre dedans puis adapté

    def new_random_game(self, n_serv=0):
            # make a new game
          self.vehicles = []
          if n_serv> 0:
              self.n_serv = n_serv
          self.add_new_vehicles_by_number(int(self.n_serv/4))
          self.renew_neighbor()
        


