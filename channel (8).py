#@title
import math
import random
import numpy as np

class  V2Vchannel:
   # Simulator of the V2V Channels
    def __init__(self):
      self.h=4
      self.N=2.5*(10**(-13))
      self.Pv2v=20
      self.Bandwith=3.5*10**6 #(Hz)
      self.delta_distance=2.6
      self.direction=['d','u','l','r']
    
    def get_path_loss_v2v(self, position_A,position_B): # toujours ajouter la delta_distance a pathloss et l'utiliser lors des calculs
              """
              position_A: position du véhicule de service
              position_B: position du véhicule de taches
              """
              self.position_A=position_A
              self.position_B=position_B
              d1 = abs(self.position_A[0] - self.position_B[0])
              d2 = abs(self.position_A[1] - self.position_B[1])
              distance = math.hypot(d1+random.randint(5,150), d2+random.randint(5,150))
              #print(distance)
              return 63.3+17.7*(math.log2(distance))
    
    def get_data_rate_v2v(self,path_loss):
      return self.Bandwith*math.log2(1+(self.Pv2v*10**(path_loss)*self.h**2)/self.N)

    def liste_data_rate_v2v(self,vehicle_serv,vehicle_task):
        self.vehicle_serv=vehicle_serv
        self.vehicle_task=vehicle_task
        u=[]
        d=[]
        l=[]
        r=[]
        #uu1,dd1,ll1,rr1=0,0,0,0
        #uu2,dd2,ll2,rr1=0,0,0,0
        for p in range(len(self.vehicle_task)):
            if self.vehicle_task[p].direction=='d':
                  b=[]
                  for j in range(len(vehicle_serv)):
                    if self.vehicle_serv[j].direction=='d':
                      b.append((self.Bandwith*math.log2(1+((self.Pv2v*(10**(self.get_path_loss_v2v(self.vehicle_task[p].position,self.vehicle_serv[j].position))/10))*self.h**2)/self.N)))
                      d.append(b)
            if self.vehicle_task[p].direction=='u':
                  b=[]
                  for j in range(len(vehicle_serv)):
                    if self.vehicle_serv[j].direction=='u':
                      b.append((self.Bandwith*math.log2(1+((self.Pv2v*(10**(self.get_path_loss_v2v(self.vehicle_task[p].position,self.vehicle_serv[j].position))/10))*self.h**2)/self.N)))
                      u.append(b)
            if self.vehicle_task[p].direction=='l':
                  b=[]
                  for j in range(len(vehicle_serv)):
                    if self.vehicle_serv[j].direction=='l':
                      b.append((self.Bandwith*math.log2(1+((self.Pv2v*(10**(self.get_path_loss_v2v(self.vehicle_task[p].position,self.vehicle_serv[j].position))/10))*self.h**2)/self.N)))
                      l.append(b)
            if self.vehicle_task[p].direction=='r':
                  b=[]
                  for j in range(len(vehicle_serv)):
                    if self.vehicle_serv[j].direction=='r':
                      b.append((self.Bandwith*math.log2(1+((self.Pv2v*(10**(self.get_path_loss_v2v(self.vehicle_task[p].position,self.vehicle_serv[j].position))/10))*self.h**2)/self.N)))
                      r.append(b)
                    
        return [d,u,l,r]




# mise à jour du pathloss et du taux de transmission de données
    def update_pathloss(self):
        self.update_pathloss_v2v = np.zeros(shape=(len(self.positions),len(self.positions)))
        for i in range(len(self.positions)):
            for j in range(len(self.positions)):
                self.update_pathloss_v2v[i][j] = self.get_path_loss(self.positions[i], self.positions[j])
        return self.update_pathloss_v2v

    def upload_data_rate(self,path_loss):
        self.update_data_rate_v2v=np.zeros(len(self.path_loss[0]),len(self.path_loss[1]))
        for i in range(len(self.path_loss[0])):
            for j in range(len(self.path_loss[1])):
              self.update_data_rate_v2v[i][j] = self.get_data_rate_v2v(path_loss[i][j])
              
        return self.update_data_rate_v2v
###################################################################################################################################################################################
class  V2Ichannel:
  # Simulator of the V2V Channels
  def __init__(self):
      self.h=4
      self.N=2.5*(10**(-13))
      self.Pv2i=30
      self.Bandwith=3.5*10**6 #(Hz)
      self.exp_path_loss=2
  
  def get_path_loss_v2i(self, position_A, RSU_pos):
        """
        position_A: position du véhicule de service
        RSU_pos: position du RSU le plus proche
        """
        d1 = abs((position_A[0]) - (RSU_pos[0]))
        d2 = abs((position_A[1]) - (RSU_pos[0]))
        distance = math.hypot(d1+random.randint(0,250), d2)
        return distance**(-self.exp_path_loss)

  def get_data_rate_v2i(self,path_loss):

      return self.Bandwith*math.log2(1+(((self.Pv2i*10**(path_loss/10))*self.h**2)/self.N))



  def liste_data_rate_v2i(self,vehicle_task,RSU):
    self.RSU=RSU
    self.vehicle_task=vehicle_task
    d,u,l,r=[],[],[],[]
    for i in range(len(self.vehicle_task)):
        if self.vehicle_task[i].direction=='d':
          for j in range(len(RSU)):
            if RSU[j][2]=='d':
                d.append((self.Bandwith*math.log2(1+(self.Pv2i*10**(self.get_path_loss_v2i(self.vehicle_task[i].position,RSU[j][3])/10)*self.h**2)/self.N)))
        if self.vehicle_task[i].direction=='u':
           for j in range(len(RSU)):
            if RSU[j][2]=='u':
                u.append((self.Bandwith*math.log2(1+(self.Pv2i*10**(self.get_path_loss_v2i(self.vehicle_task[i].position,RSU[j][3])/10)*self.h**2)/self.N)))
        if self.vehicle_task[i].direction=='l':
          for j in range(len(RSU)):
            if RSU[j][2]=='l':
                l.append((self.Bandwith*math.log2(1+(self.Pv2i*10**(self.get_path_loss_v2i(self.vehicle_task[i].position,RSU[j][3])/10)*self.h**2)/self.N)))
        if self.vehicle_task[i].direction=='r':
          for j in range(len(RSU)):
            if RSU[j][2]=='r':
                r.append((self.Bandwith*math.log2(1+(self.Pv2i*10**(self.get_path_loss_v2i(self.vehicle_task[i].position,RSU[j][3])/10)*self.h**2)/self.N)))

    return [d,u,l,r]

  def get_data_rate_rsu(self,numer_vehicle,liste_data_rate_v2i): #permet de determiner le plus grand datarate et son RSU correspondant
        
        self.numer_vehicle=numer_vehicle
        self.liste_data_rate_v2i=liste_data_rate_v2i
        liste=[]
        for i in range(len(self.liste_data_rate_v2i)):
            max_val=max(self.liste_data_rate_v2i[numer_vehicle])
            rsu_index=self.liste_data_rate_v2i[numer_vehicle].index(max_val)
            liste.append([max_val,rsu_index])
        return liste
    
  #ef liste_get_rate_rsu(self,)
    
        
# mise à jour du pathloss et du taux de transmission de donnée
  def update_pathloss(self):
        self.update_path_loss_v2i = np.zeros(len(self.positions))
        for i in range(len(self.positions)):
            d1 = abs((self.positions[i][0]) - (self.BS_position[0]))
            d2 = abs((self.positions[i][1]) - (self.BS_position[1]))
            distance = math.hypot(d1,d2) # change from meters to kilometers
            self.update_path_loss_v2i[i] = distance**(-self.exp_path_loss)
        return self.update_path_loss_v2i


  def update_data_rate(self,path_loss):
      self.update_data_rate_v2i = np.zeros(len(self.path_loss))
      for i in range(len(self.path_loss)):
        self.update_data_rate_v2i[i]=self.get_data_rate_v2i(path_loss[i])

      return self.update_data_rate_v2i 