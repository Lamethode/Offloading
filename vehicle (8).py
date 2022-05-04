#@title
import random
import cloud
from cloud import *
from env import *


def a_list(resource_required,liste_dir_task,liste_dir):
        liste_dir_task=liste_dir_task
        liste_dir=liste_dir
        resource_required=resource_required
        liste=[]
        for p in range(len(liste_dir_task)):
            m=[]
            for i in range(liste_dir_task[p]):
                l=[]
                for j in range(1,liste_dir[p]+1):
                    h=(resource_required[p][i][j])/sum(resource_required[p][i])
                    if h==0:
                      h=0.01
                      l.append(h)
                    else:
                      l.append(h)
                m.append(l)
            liste.append(m)
        return liste


class  Vehicle:
      # Vehicle simulator: include all the information for a vehicle
      #time -time of the simulation
      #timstep  - duration of one calculation step (seconds)
    def __init__(self, start_position, start_direction,velocity):
        self.position = start_position
        self.direction = start_direction
        self.velocity = velocity
        self.neighbors = []
        self.destinations = []

#############################################################################################################################################################################
class  ServiceVehicle(Vehicle):

    """ Vehicle that can receive offloaded tasks """
    def __init__(self, start_position, start_direction,velocity):
        super().__init__(start_position, start_direction,velocity)  
        #time: int  time_step:float, information:list
        #self.p_base=p_base # prix de base pour une unité de calcul pour le véhicule de service
        #self.resource=random.randint(2000,5000) #(MHz)
        self.e=4*10**(-9)*10**(6)
        self.k= 2*10**(-4)*10**(6)

        self.directions=['d','u','l','r']

    def price_unit(self,price_cloud):
      self.price_cloud=price_cloud
      
      price=random.randint(self.price_cloud,500)
      return price
    
    def action_space(self,vehicle_serv): #action d'un véhicule
      self.price_cloud=cloud.Pcloud
      vehicle_serv=vehicle_serv
      d=[]
      u=[]
      l=[]
      r=[]
      for i in range(len(vehicle_serv)):
        if vehicle_serv[i].direction=='d':
            k=[]
            k.append(self.price_unit(self.price_cloud))
            d.append(k)
            continue
                     
        if vehicle_serv[i].direction=='u':
            k=[]
            k.append(self.price_unit(self.price_cloud))
            u.append(k)
            continue
                     
        if vehicle_serv[i].direction=='l':
            k=[]
            k.append(self.price_unit(self.price_cloud))
            l.append(k)
            continue
        if vehicle_serv[i].direction=='r':
            k=[]
            k.append(self.price_unit(self.price_cloud))
            r.append(k)
            continue       
      return [d,u,l,r] #liste en [i,j]

    def action_space_l(self,liste_dir):
      self.price_cloud=cloud.Pcloud
      liste_dir=liste_dir
      liste=[]
      for p in range(len(liste_dir)):
        l=[]
        for i in range(liste_dir[p]):
            k=[]
            k.append(self.price_unit(self.price_cloud))
            l.append(k)
        liste.append(l)
      return liste
    
    
    def action_space_t(self): #liste de des actions de tous les véhcules
      liste=[]
      for i in range(Environnement_service.num_service_vehicle):
          liste.append(self.strategy_price(Environnement_task.num_task_vehicle,CloudServer.broadcast_price()))
      return liste

    def ressource_utilization(self,list_resource_required,liste_dir,liste_dir_task):
        
        self.list_resource_required=list_resource_required
        self.liste_dir,self.liste_dir_task=liste_dir,liste_dir_task
        ress=[[0 for p in range(self.liste_dir[i])]for i in range(len(self.liste_dir))]
        for p in range(len(self.liste_dir)):
            for i in range(self.liste_dir_task[p]):
                for j in range(1,self.liste_dir[p]+1):
                    ress[p][j-1]=ress[p][j-1]+self.list_resource_required[p][i][j]
        return ress

    def get_state(self,i,p,env_serv,resource_serv,vehicle_serv,ressource,liste_dir,liste_dir_task): # état d'un agent i  # à mettre dans vehicule task
            # a reconfigurer dans le code principale
          env_serv=env_serv
          liste_dir,liste_dir_task=liste_dir,liste_dir_task
          ressource=ressource
          vehicle_serv=vehicle_serv
          resource_serv=resource_serv
          self.i=i
          self.p=p
          self.inf=env_serv.get_info()
          self.resource=resource_serv
          liste=[]
          
          liste.append(self.inf[i])
          liste.append(cloud.broadcast_price())
          if vehicle_serv[i].direction=='d':
              liste.append(self.resource[0][p])
              liste.append(vehicle_serv[0].ressource_utilization(ressource,liste_dir,liste_dir_task)[0][p])
          if vehicle_serv[i].direction=='u':
              liste.append(self.resource[1][p])
              liste.append(vehicle_serv[0].ressource_utilization(ressource,liste_dir,liste_dir_task)[1][p])
          if vehicle_serv[i].direction=='l':
              liste.append(self.resource[2][p])
              liste.append(vehicle_serv[0].ressource_utilization(ressource,liste_dir,liste_dir_task)[2][p])
          if vehicle_serv[i].direction=='r':
              liste.append(self.resource[3][p])
              liste.append(vehicle_serv[0].ressource_utilization(ressource,liste_dir,liste_dir_task)[3][p])
          #liste.append(cloud.broadcast_price())
          # a corriggé
          return liste


    def state_space(self,vehicle_serv,env_serv,resource_serv,ressource,liste_dir,liste_dir_task):
          liste_dir,liste_dir_taskv=liste_dir,liste_dir_task
          vehicle_serv=vehicle_serv
          ressource=ressource
          resource_serv=resource_serv
          d,u,l,r=[],[],[],[]
          dd,uu,ll,rr=0,0,0,0
          for i in range(len(vehicle_serv)):
            if vehicle_serv[i].direction=='d':
              d.append(self.get_state(i,dd,env_serv,resource_serv,vehicle_serv,ressource,liste_dir,liste_dir_task))
              dd=dd+1
            if vehicle_serv[i].direction=='u':
              u.append(self.get_state(i,uu,env_serv,resource_serv,vehicle_serv,ressource,liste_dir,liste_dir_task))
              uu=uu+1
            if vehicle_serv[i].direction=='l':
              l.append(self.get_state(i,ll,env_serv,resource_serv,vehicle_serv,ressource,liste_dir,liste_dir_task))
              ll=ll+1
            if vehicle_serv[i].direction=='r':
              r.append(self.get_state(i,rr,env_serv,resource_serv,vehicle_serv,ressource,liste_dir,liste_dir_task))
              rr=rr+1
          return [d,u,l,r]

    def next_state_space(self,state_space,liste_dir):
      state_space,liste_dir=state_space,liste_dir
      for p in range(len(liste_dir)):
        for i in range(liste_dir[p]):
          state_space[p][i][0][0]=state_space[p][i][0][0]+random.randint(0,5)
          state_space[p][i][0][1]=state_space[p][i][0][1]+random.randint(0,8)
          state_space[p][i][0][2]=state_space[p][i][0][2]+random.random()
      return state_space

    def ressource_l(self,liste_dir):
      liste_dir=liste_dir
      liste=[]
      for p in range(len(liste_dir)):
        l=[]
        for i in range(liste_dir[p]):
          res=random.randint(2000,5000)
          l.append(res)
        liste.append(l)
      return liste

    def resource(self,service_vehicle): # liste des resources des véhicules de services
      liste=[]
      self.service_vehicle=service_vehicle
      d=[]
      u=[]
      l=[]
      r=[]
      
      for i in range(len(self.service_vehicle)):
        if self.service_vehicle[i].direction=='d':
          res=random.randint(2000,5000)
          d.append(res)
          continue
        
        if self.service_vehicle[i].direction=='u':
          res=random.randint(2000,5000)
          u.append(res)
          continue
        
        if self.service_vehicle[i].direction=='l':
          res=random.randint(2000,5000)
          l.append(res)
          continue
        
        if self.service_vehicle[i].direction=='r':
          res=random.randint(2000,5000)
          r.append(res)
          continue
         
      return [d,u,l,r]            #liste en [i]
  
    #def list_resource_required(self,resource:list):
      #self.resource=resource
      #return resource


     #liste en [i,j]


    """    def update_ressource(self,resource_required,resource): # le required ressource représentant notre de prix vendu au véhicule de tache U pour calculer sa tache
      self.resource_required=resource_required
      self.resource=resource
      return (self.resource-self.resource_required)"""
   

      #liste ressource et update ressources doivent etre des listes
  
    def liste_update_resource(self,list_resource_required,list_ressource,liste_dir,liste_dir_task):
      self.liste_dir,self.liste_dir_task=liste_dir,liste_dir_task
      self.list_resource_required=list_resource_required
      self.list_ressource=list_ressource
      for p in range(len(self.liste_dir)):
        for i in range(self.liste_dir_task[p]):
            for j in range(1,self.liste_dir[p]+1):
                if self.list_ressource[p][j-1]<=0:
                    self.list_ressource[p][j-1]=0
                else:
                   self.list_ressource[p][j-1]=self.list_ressource[p][j-1]-self.list_resource_required[p][i][j]
      return self.list_ressource   #liste en [i]


    def broadcast_price(self, price):
      self.price=price
      return price
    

                        

    def price_task_u (self,price_base,global_list_sub_task,resource_required,resource,liste_dir,liste_dir_task): # liste des prix des services des véhicules de services pour les taches U par véhicule de tache
          self.liste_dir,self.liste_dir_task=liste_dir,liste_dir_task
          self.global_list_sub_task=global_list_sub_task # prendre les M sous-taches
          self.price_factor=2*10**(-5)
          self.server_factor=2*10**(-3)
          self.resource_required=resource_required
          self.price_base=price_base
          self.resource=resource
          liste_global=[]
          for p in range(len(self.liste_dir)):
              liste=[]
              for i in range(self.liste_dir_task[p]):
                liste_sub_task=[]
                for j in  range(1,self.liste_dir[p]+1):
                        size_u= self.global_list_sub_task[p][i][j][0]
                        time_u=self.global_list_sub_task[p][i][j][3]
                        resource_u=self.resource_required[p][i][j]
                        a=(self.price_base[p][j-1][0]+((self.price_factor*(size_u/time_u))))+(self.server_factor*(((self.resource[p][j-1])-(resource_u)/(self.resource[p][j-1]+0.05))-1))
                        #print(a)
                        liste_sub_task.append(a)
                liste.append(liste_sub_task)
              liste_global.append(liste)
          return liste_global # liste en [i,j]

    def time_exec(self,a,size_u,cpu_u_required,data_rate):
      self.a=a
      self.size_u=size_u
      self.data_rate=data_rate
      self.cpu_u_required=cpu_u_required
      return ((a*cpu_u_required*size_u)/data_rate)

    def list_time_exec(self,a_list,list_sub_task,data_rate_list,liste_dir,liste_dir_task): #a terminer
      self.a_list=a_list
      self.data_rate_list=data_rate_list
      self.list_sub_task=list_sub_task
      self.data_rate_list=data_rate_list
      big_list=[]
      for p in range(len(self.liste_dir)):
          m=[]
          for i in range(self.liste_dir_task[p]):
            liste=[]
            for j in range(1,self.liste_dir[p]+1):
              liste.append(self.time_exec(a_list[p][i][j-1],self.list_sub_task[p][i][j][0],self.list_sub_task[p][i][j][1],self.data_rate_list[p][i][j-1]))
            m.append(liste)
          big_list.append(m)
      return big_list # liste en [i,j] 
        
  
    def send_to_cloud_msg (self,service_vehicle,resource_service) :
       # vérifie si le vehicule de service a envoyer un message de déchargement de calcul au serveur cloud 
       # si oui, utiliser la fréquence de resolution de la tache en surpluse pour calculer la tache avec le serveru cloud
      liste=[]
      d,u,l,r=[],[],[],[]
      self.service_vehicle=service_vehicle
      self.resource_service=resource_service
      dd,uu,ll,rr=0,0,0,0
      for i in range(len(self.service_vehicle)):
            if self.service_vehicle[i].direction=='d':
                if resource_service[0][dd]<0:
                  d.append(True)
                else:
                  d.append(False)
                dd +=1
            elif self.service_vehicle[i].direction=='u':
                if resource_service[1][uu]<0:
                  u.append(True)
                else:
                  u.append(False)
                uu +=1
            elif self.service_vehicle[i].direction=='l':
                if resource_service[2][ll]<0:
                  l.append(True)
                else:
                  l.append(False)
                ll +=1
            elif self.service_vehicle[i].direction=='r':
                if resource_service[3][rr]<0:
                  r.append(True)
                else:
                  r.append(False)
                rr +=1
      return [d,u,l,r]


    def return_time(self,a,size_u,data_rate):
        self.b_u=5
        self.a=a
        self.size_u=size_u
        self.data_rate=data_rate
        return ((self.a*self.b_u*self.size_u)/self.data_rate)
#liste
    def liste_return_time(self,a_liste,liste_sub_task,liste_data_rate,liste_dir,liste_dir_task):
        self.liste_dir,self.liste_dir_task=liste_dir,liste_dir_task
        self.a_liste=a_liste
        self.liste_sub_task=liste_sub_task
        self.liste_data_rate=liste_data_rate
        big_list=[]
        for p in range(len(self.liste_dir)):
            m=[]
            for i in range(self.liste_dir_task[p]):
                liste=[]
                for j in range(1,self.liste_dir[p]+1):
                  liste.append(self.return_time(self.a_liste[p][i][j-1],self.liste_sub_task[p][i][j][0],self.liste_data_rate[p][i][j-1]))
                m.append(liste)
            big_list.append(m)
        return big_list
        

    def list_time_mec(self,num_global_sub_task,uptime_list,exec_time_list,down_time_list,liste_dir,liste_dir_task):
      self.liste_dir,self.liste_dir_task=liste_dir,liste_dir_task
      self.num_global_sub_task=num_global_sub_task
      self.uptime_list=uptime_list
      self.exec_time_list=exec_time_list
      self.down_time_list=down_time_list
      liste=[]
      for p in range(len(self.liste_dir)):
          m=[]
          for i in range(self.liste_dir_task[p]):
            l=[]
            for j in range(1,self.liste_dir[p]+1):
                l.append(self.time_mec(self.uptime_list[p][i][j-1],self.exec_time_list[p][i][j-1],self.down_time_list[p][i][j-1]))
            m.append(l)
          liste.append(m)
      return liste


    def time_mec(self,up_time,exec_time,down_time): # temps total utiliser pour calculer la tache u en mode v2v
      self.up_time=up_time
      self.exec_time=exec_time
      self.down_time=down_time
      return (self.up_time+self.exec_time+self.down_time)


    def first_term (self,list_price_sub_task_u:list,list_sub_task_u:list,resource_required,liste_dir,liste_dir_task): # number_total_list - nombre de la liste global des toutes les taches d'origine
      liste_dir,liste_dir_task=liste_dir,liste_dir_task
      self.list_price_sub_task_u=list_price_sub_task_u
      self.list_sub_task_u=list_sub_task_u
      self.resource_required=resource_required
      m=[]
      for p in range(len(self.liste_dir)):
          liste=[]  
          for i in range(1,self.liste_dir[p]+1):
            som=0
            for j in range(self.liste_dir_task[p]):
                som =som+(self.resource_required[p][j][i]*self.list_price_sub_task_u[p][j][i-1])
            #l.append(som)
            liste.append(som)
          m.append(liste)
      return m

    def second_term(self,a_liste,list_sub_task_u:list,total_resource_task,ressource,liste_dir,liste_dir_task):
      liste_dir,liste_dir_task=liste_dir,liste_dir_task
      self.a_liste=a_liste
      ressource=ressource
      self.list_sub_task_u=list_sub_task_u
      self.total_resource_task=total_resource_task
      m=[]
      for p in range(len(self.liste_dir)):
          liste=[]
          for i in range(1,self.liste_dir[p]+1):
            some=0
            for j in range(self.liste_dir_task[p]):
               some=some+(((ressource[p][j][i-1])**(2))*((self.a_liste[p][j][i-1]*self.list_sub_task_u[p][j][i][0])/self.total_resource_task[p][j]))
               some=some*(self.e*self.k)
            liste.append(some)
          m.append(liste)
      return m
    
    def third_term (self,resource_cloud_used:list,liste_dir):
      self.liste_dir=liste_dir
      self.p_cloud=1.5*10**(-3)
      self.resource_cloud_used=resource_cloud_used
      for p in range(len(self.liste_dir)):
          for i in range(self.liste_dir[p]):
              self.resource_cloud_used[p][i]=self.p_cloud*self.resource_cloud_used[p][i]
      return self.resource_cloud_used

    def reward(self,first_term,second_term,third_term,liste_dir): # a completer
        self.liste_dir=liste_dir
        first_term=first_term
        second_term=second_term
        third_term=third_term
        m=[]
        for p in range(len(self.liste_dir)):
          liste=[]
          for i in range(self.liste_dir[p]):
              liste.append((first_term[p][i] - second_term[p][i] - third_term[p][i]))
          m.append(liste)
        return m


    """
      1- diffusion du prix de base aux vehicules de tache
      2- calcul de prix de la tche du véchile de taches en tenant compte de ses pécificités
      3-temps de calcul des taches + temps de retour du résultat de la tache
      4-envoie de message au cloud serveur pour pour décharger une partie de la tache
    """
        
 ################################################################################################################################################################################   



class  TaskVehicle(Vehicle):
    """
    1-prix d'achat pour le calcul des taches
    2-temps de calcul en local de la tache T0
    3-temps de calcul si toute les taches étaient effectuées en local
    4- temps d'envoi de la tache            et de reception de la tache aux véhicule de services
    si conditiore de insuffisance de ressource de calcul vérifiée
    temps de transmission                   et de reception de la taches

    """
    def __init__(self, start_position, start_direction,velocity):
        super().__init__(start_position, start_direction,velocity) #time: int  time_step:float, information:list
        
        self.computation_power= 2200  #(MHz)
        self.directions=['d','u','l','r']
        self.eb_local=0.05
        self.y=0.26
        self.time_discount_factor=20
        self.expendure_discount_factor=0.15
        self.u_sucess=20
      
    def price_task(self,service_price):
      self.service_price=service_price
      return self.service_price

#liste
    
    def exec_time(self,n_cpu_required,sub_task_u,resource_required):
      self.n_cpu_required=n_cpu_required
      self.sub_task_u=sub_task_u
      self.resource_required=resource_required
      return ((self.n_cpu_required*self.sub_task_u)/self.resource_required)
#liste

    def local_time(self,list_sub_task,resource_required,liste_dir_task):
      liste=[]
      self.liste_dir_task=liste_dir_task
      self.l=list_sub_task
      self.p=resource_required
      for p in range(len(self.liste_dir_task)):    
          m=[]
          #k=[]
          for i in range(self.liste_dir_task[p]):
                    #k=[]  
                    elt=self.exec_time(self.l[p][i][0][1],self.l[p][i][0][0],self.p[p][i][0])
                    m.append(elt)
          #m.append(k)
          liste.append(m)
          #print(liste)
          
      return liste#liste en [i]

    """def state_space(self,vehicle_task,env_task,data_rate_liste_v,data_rate_liste_i,liste_dir,liste_tu,price_task_u): # a reconfigurer lorsque on fera le programme principales par les grandes variables stockées
        vehicle_task=vehicle_task
        data_rate_liste_v=data_rate_liste_v
        data_rate_liste_i=data_rate_liste_i
        env_task=env_task
        dd,uu,ll,rr=[],[],[],[]
        ddi,uui,lli,rri=0,0,0,0
        ddj,uuj,llj,rrj=0,0,0,0
        for i in range(len(vehicle_task)):
            if vehicle_task[i].direction=='d':
              #print(ddi)
              l=[]
              t=[]
              a=env_task.get_info()[i]
              l.append(a)
              l.append(liste_tu[0][ddi])
              l.append(data_rate_liste_v[0][ddi])
              l.append(data_rate_liste_i[0][ddi])
              for j in range(self.liste_dir[0]):
                      b=price_task_u[0][ddi][j]
                      t.append(b)
              l.append(t)
              dd.append(l)
              ddi +=1
            if vehicle_task[i].direction=='u':
              l=[]
              t=[]
              a=env_task.get_info()[i]
              l.append(a)
              l.append(liste_tu[0][uui])
              l.append(data_rate_liste_v[1][uui])
              l.append(data_rate_liste_i[1][uui])
              for j in range(self.liste_dir[1]):
                      b=price_task_u[1][uui][j]
                      t.append(b)
              l.append(t)
              uu.append(l)
              uui +=1
            if vehicle_task[i].direction=='l':
              #print(ddi)
              l=[]
              t=[]
              a=env_task.get_info()[i]
              l.append(a)
              l.append(liste_tu[2][lli])
              l.append(data_rate_liste_v[2][lli])
              l.append(data_rate_liste_i[2][lli])
              for j in range(self.liste_dir[2]):
                    #print(ddj)
                    #if vehicle_serv[j].direction=='d':
                      b=price_task_u[2][lli][j]
                      t.append(b)
                      #ddj +=1
              l.append(t)
              ll.append(l)
              lli +=1
            if vehicle_task[i].direction=='r':
              #print(ddi)
              l=[]
              t=[]
              a=env_task.get_info()[i]
              l.append(a)
              l.append(liste_tu[3][rri])
              l.append(data_rate_liste_v[3][rri])
              l.append(data_rate_liste_i[3][rri])
              for j in range(self.liste_dir[3]):
                    #print(ddj)
                    #if vehicle_serv[j].direction=='d':
                      b=price_task_u[3][rri][j]
                      t.append(b)
                      #ddj +=1
              l.append(t)
              rr.append(l)
              rri +=1
        return [dd,uu,ll,rr]"""

    def state_space(self,vehicle_task,env_task,data_rate_liste_v,data_rate_liste_i,liste_dir,liste_dir_task,liste_tu,price_task_u):
      vehicle_task,env_task,data_rate_liste_v,data_rate_liste_i,liste_dir,liste_tu,price_task_u=vehicle_task,env_task,data_rate_liste_v,data_rate_liste_i,liste_dir,liste_tu,price_task_u   
      liste_dir_task=liste_dir_task
      liste=[]     
      for p in range(len(liste_dir_task)):
              l=[]
              for i in range(liste_dir_task[p]):
                t=[]
                mm=[]
                a=env_task.get_info_l(liste_dir_task)[p][i]
                t.append(a)
                t.append(liste_tu[p][i])
                t.append(data_rate_liste_v[p][i])
                t.append(data_rate_liste_i[p][i])
                for j in range(liste_dir[p]):
                        b=price_task_u[p][i][j]
                        mm.append(b)
                t.append(mm)
                l.append(t)
              liste.append(l)
      return liste


    def next_state_space(self,state_space,liste_dir_task):
      state_space,liste_dir_task=state_space,liste_dir_task
      for p in range(len(liste_dir_task)):
        for i in range(liste_dir_task[p]):
          state_space[p][i][0][0]=state_space[p][i][0][0]+random.randint(0,5)
          state_space[p][i][0][1]=state_space[p][i][0][1]+random.randint(0,8)
          state_space[p][i][0][2]=state_space[p][i][0][2]+random.random()
      return state_space

    def liste_ressouce_l(self,liste_dir_task):
      liste_dir_task=liste_dir_task
      liste=[]
      for p in range(len(liste_dir_task)):
        l=[]
        for i in range(liste_dir_task[p]):
          l.append(2200)
        liste.append(l)
      return liste



    def liste_ressouce(self,task_vehicle):
        self.task_vehicle=task_vehicle
        d=[]
        u=[]
        l=[]
        r=[]
        for i in range(len(self.task_vehicle)):
            if self.task_vehicle[i].direction=='d': 
                d.append(2200) #Coputation ressource
            if self.task_vehicle[i].direction=='u':
                 u.append(2200)
            if self.task_vehicle[i].direction=='l':
                 l.append(2200)
            if self.task_vehicle[i].direction=='r':
                 r.append(2200)
            
        return [d,u,l,r]
    
    def update_resource(self,resource,ressource_u):

      self.resource=resource
      self.ressource_u=ressource_u
      
      return (self.resource-(ressource_u)) # chaque traitement de sous-tache en local prendre 10% des ressources disponibles
#liste
    
    def liste_update_ressource(self,resource,resource_u,liste_dir,liste_dir_task):
        self.resource=resource
        self.resource_u=resource_u
        for i in range(len(self.liste_dir)):
            for j in range(self.liste_dir_task[i]):
                if self.resource[i][j]<=0:
                    self.resource[i][j]=0
                else:
                    self.resource[i][j]-=self.resource_u[i][j][0]
        return self.resource
        
    def list_resource_required(self,task_to_subtask,task_vehicle,service_vehicle,liste_dir): # liste des actions des vehciles de taches
      d=[]
      u=[]
      l=[]
      r=[]
      self.task_to_subtask=task_to_subtask
      self.task_vehicle=task_vehicle
      self.service_vehicle=service_vehicle
      self.liste_dir=liste_dir
      ddi,uui,lli,rri=0,0,0,0,
      for i in range(len(self.task_vehicle)):
        m=[]
        if self.task_vehicle[i].direction=='d':
            self.resource_required=random.randint(int((self.task_to_subtask[0][0][0][1])/self.liste_dir[0])+3,int((500/10))) # resource requis pour le calcul de la sous-tache
            m.append(self.resource_required)
            for j in range(1,self.liste_dir[0]+1):
                    if self.liste_dir[0]<=(len(self.service_vehicle)/4):
                        resource_required=random.randint(int((self.task_to_subtask[0][1][j][1])/(int(len(self.service_vehicle)/4))),int((500/10))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)
                    else:
                        resource_required=random.randint(int((self.task_to_subtask[0][1][j][1])/self.liste_dir[0])+3,int((500/20))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)
                
                                                     
            ddi+=1
        
            d.append(m)  
        #t+=1
            continue
        
        if self.task_vehicle[i].direction=='u':
            self.resource_required=random.randint(int((self.task_to_subtask[1][0][0][1])/self.liste_dir[1])+3,int((500/10))) # resource requis pour le calcul de la sous-tache
            m.append(self.resource_required)
            for j in range(1,self.liste_dir[1]+1):
                    if self.liste_dir[1]<=(len(self.service_vehicle)/4):
                        resource_required=random.randint(int((self.task_to_subtask[1][1][j][1])/(int(len(self.service_vehicle)/4))),int((500/10))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)
                    else:
                        resource_required=random.randint(int((self.task_to_subtask[1][1][j][1])/self.liste_dir[1]),int((500/20))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)
                
                                                     
            uui+=1
        
            u.append(m)  
       # t+=1
            continue  
        if self.task_vehicle[i].direction=='l':
            self.resource_required=random.randint(int((self.task_to_subtask[2][0][0][1])/self.liste_dir[2])+3,int((500/10))) # resource requis pour le calcul de la sous-tache
            m.append(self.resource_required)
            for j in range(1,self.liste_dir[2]+1):
                    if self.liste_dir[2]<=(len(self.service_vehicle)/4):
                        resource_required=random.randint(int((self.task_to_subtask[2][1][j][1])/(int(len(self.service_vehicle)/4))),int((500/10))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)
                    else:
                        resource_required=random.randint(int((self.task_to_subtask[2][1][j][1])/self.liste_dir[2]),int((500/20))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)                                
            lli+=1
            l.append(m)  
        #t+=1
            continue
        
        if self.task_vehicle[i].direction=='r':
            self.resource_required=random.randint(int((self.task_to_subtask[3][0][0][1])/self.liste_dir[3])+3,int((500/10))) # resource requis pour le calcul de la sous-tache
            m.append(self.resource_required)
            for j in range(1,self.liste_dir[3]+1):
                    if self.liste_dir[3]<=(len(self.service_vehicle)/4):
                        resource_required=random.randint(int((self.task_to_subtask[3][1][j][1])/(int(len(self.service_vehicle)/4))),int((500/10))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)
                    else:
                        resource_required=random.randint(int((self.task_to_subtask[3][1][j][1])/self.liste_dir[3]),int((500/20))) # resource requis pour le calcul de la sous-tache
                        m.append(resource_required)                                
            rri+=1
            r.append(m)  
        #t+=1
            continue
        
      return [d,u,l,r]

    def action_space(self,ressource):
        self.action=ressource
        return self.action
   
    def exec_time_all_l(self,global_l,ressource,liste_dir_task):
        global_l,ressource,liste_dir_task=global_l,ressource,liste_dir_task
        liste=[]
        for p in range(len(liste_dir_task)):
          l=[]
          for i in range(liste_dir_task[p]):
            time=global_l[p][i][1]*global_l[p][i][0]/ressource[p][i]
            l.append(time)
          liste.append(l)
        return liste
        
    def exec_time_all(self,global_task:list,ressource,task_vehicle): # task_u = size_u 
        d,u,l,r=[],[],[],[] 
        dd,uu,ll,rr=0,0,0,0#max_time_add_to_task represente 
        time=0                                                                                     #l'ensemble des taches avec leur durée max
        self.ressource=ressource
        self.global_task=global_task
        self.task_vehicle=task_vehicle
        for i in range(len(self.task_vehicle)):
            if self.task_vehicle[i].direction=='d':
              time=0 
              time=time+(self.global_task[i][1]*self.global_task[i][0])/(self.ressource[0][dd])
              d.append(time)
              dd +=1
              continue 
            if self.task_vehicle[i].direction=='u':
              time=0 
              time=time+(time+self.global_task[i][1]*self.global_task[i][0])/(self.ressource[1][uu])
              u.append(time)
              uu +=1
              continue
            if self.task_vehicle[i].direction=='l':
              #print(l)
              time=0 
              time=time+(self.global_task[i][1]*self.global_task[i][0])/(self.ressource[2][ll])
              l.append(time)
              ll +=1
              continue
            if self.task_vehicle[i].direction=='r':
              #print(r)
              time=0 
              time=time+(self.global_task[i][1]*self.global_task[i][0])/(self.ressource[3][rr])
              r.append(time)
              rr +=1
              continue
            
        return [d,u,l,r]
    
    def resource_required(self,ressource): #recevoir la liste des resources required du véhicules de services
      self.ressource=ressource

      return ressource #liste en [i,j]

    def time_to_rsu(self,a,size_u,resource_required,resource_service,data_rate_v2i):
      self.a=a
      self.size_u=size_u
      self.resource_required=resource_required
      self.resource_service=resource_service
      self.data_rate_v2i=data_rate_v2i

      return ((self.a*size_u*(resource_required-resource_service))/(data_rate_v2i*resource_required+0.01))
#liste

    def list_time_to_rsu(self,a_list,global_list_sub_tasks,list_data_rate_v2i,ressource_required,service_ressource,liste_dir_task):
        self.a_list=a_list
        liste_dir_task=liste_dir_task
        self.service_ressource=service_ressource
        self.global_list_sub_tasks=global_list_sub_tasks
        self.list_data_rate_v2i=list_data_rate_v2i
        self.ressource_required=ressource_required
        liste=[]
        for p in range(len(self.liste_dir_task)):
            m=[]
            for i in  range(self.liste_dir_task[p]):
                l=[]
                for j in range(1,self.liste_dir[p]+1):
                    l.append(self.time_to_rsu(self.a_list[p][i][j-1],self.global_list_sub_tasks[p][i][j][0],self.ressource_required[p][i][j],self.service_ressource[p][j-1],self.list_data_rate_v2i[p][i]))
                m.append(l)
            liste.append(m)
        return liste
                
        
    def time_to_service(self,a,sub_task_u,data_rate_v2v):
      self.a=a
      self.sub_task_u=sub_task_u
      self.data_rate_v2v=data_rate_v2v
      return ((self.a*self.sub_task_u)/self.data_rate_v2v)
#liste
    def list_time_to_service(self,a_list,global_list_sub_tasks,list_data_rate_v2v,liste_dir,liste_dir_task):
      k=[]
      self.a_list=a_list
      self.global_list_sub_tasks=global_list_sub_tasks
      self.list_data_rate_v2v=list_data_rate_v2v
      for p in range(len(self.liste_dir)):
          liste=[]
          for i in range(self.liste_dir_task[p]):
            l=[]
            for j in range(1,self.liste_dir[p]+1):
                l.append(self.time_to_service(self.a_list[p][i][j-1],self.global_list_sub_tasks[p][i][j][0],self.list_data_rate_v2v[p][i][j-1]))
            liste.append(l)
          k.append(liste)
      return k # liste en [i,j]

    def  time_complete_u(self,local_time:list,mec_time:list,cloud_time:list,liste_dir_task): # les paramèrtres sent des listes
      local_time=local_time # liste en [i,0]
      mec_time=mec_time # liste en [i,j]
      cloud_time=cloud_time # liste en [i,j]
      m=[]
      for p in range(len(self.liste_dir_task)):
          liste=[]
          for i in range(self.liste_dir_task[p]):
            l=[]
            for j in range(self.liste_dir[p]):
              time_max=max(local_time[p][i],mec_time[p][i][j],cloud_time[p][i][j]) # la valeur de retour est une liste; donc on prendre la valeur a l(intérieure
              l.append(time_max)
            liste.append(l)
          m.append(liste)
      return m
    
    def time_all_complete(self,time_complete_u,liste_dir_task): # liste de la durée maximale de toutes les osus-taches d'un tache i
      time_complete_u=time_complete_u
      liste=[]
      liste_dir_task=liste_dir_task
      for p in range(len(self.liste_dir_task)):
            k=[]
            for i in range(self.liste_dir_task[p]):
                l=[]
                l.append(max(time_complete_u[p][i]))
                k.append(l)
            liste.append(k)
      return liste
    

    def reward_task_vehicle(self,time_all,time_complete,p_pay,liste_task_time): 
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
      p_pay=p_pay
      time_all=time_all
      time_complete=time_complete
      liste_task_time=liste_task_time

      if liste_task_time < time_complete : 
          if time_all-time_complete<0:
               return(self.time_sensitive_factor*self.time_discount_factor*math.log(1+(-1)*(time_all-time_complete))-(self.price_sensitive_factor*self.expendure_discount_factor*((p_pay+self.eb_local)**(self.y)))-(self.sucess_sensitive_factor*self.u_sucess))
          else:
            return (self.time_sensitive_factor*self.time_discount_factor*math.log(1+time_all-time_complete)-(self.price_sensitive_factor*self.expendure_discount_factor*((p_pay+self.eb_local)**(self.y)))-(self.sucess_sensitive_factor*self.u_sucess))
      else:
            if time_all-time_complete<0:
                    return (self.time_sensitive_factor*self.time_discount_factor*math.log(1+(-1)*(time_all-time_complete))-(self.price_sensitive_factor*self.expendure_discount_factor*((p_pay+self.eb_local)**(self.y)))+(self.sucess_sensitive_factor*self.u_sucess))
            else:
              return (self.time_sensitive_factor*self.time_discount_factor*math.log(1+time_all-time_complete)-(self.price_sensitive_factor*self.expendure_discount_factor*((p_pay+self.eb_local)**(self.y)))+(self.sucess_sensitive_factor*self.u_sucess))


    def list_reward_task(self,list_time_all,liste_time_complete,liste_ppay,global_task,liste_dir_task):
        liste_dir_task=liste_dir_task
        list_time_all,liste_time_complete,liste_ppay,global_task=list_time_all,liste_time_complete,liste_ppay,global_task
        liste=[]
        for p in range(len(self.liste_dir_task)):
            l=[]
            for i in range(self.liste_dir_task[p]):
                    l.append(self.reward_task_vehicle(list_time_all[p][i],liste_time_complete[p][i][0],liste_ppay[p][i],global_task[p][i][3]))
            liste.append(l)
        return liste

    def p_pay (self,ressource_required:list,list_price_sub_task_u:list,liste_dir,liste_dir_task): # number_total_list - nombre de la liste global des toutes les taches d'origine
        #som=0
        liste_dir,liste_dir_task=liste_dir,liste_dir_task
        ressource_required=ressource_required
        list_price_sub_task_u=list_price_sub_task_u
        #list_sub_task_u=list_sub_task_u
        big_list=[]
        for p in range(len(self.liste_dir)):
            liste=[]
            for i in range(self.liste_dir_task[p]):
                som=0
                for j in range(self.liste_dir[p]):
                    som=som+ressource_required[p][i][j]*list_price_sub_task_u[p][i][j]
                liste.append(som)
            big_list.append(liste)
        return big_list

  
  ################################ PART OF VEHICLE MAKING TASKS #####################################################################""
        
class Task:

        def __init__(self):
          pass
        
        def tasks_generation(self):  # Ok
          task=[]
          self.size=random.randint(1000,1700)
          task.append(self.size)
          self.n_cpu=random.randint(200,500)
          task.append(self.n_cpu)
          self.b=int(self.size/100)
          task.append(self.b)
          return task #liste en [i]

        def task_to_subtask_l(self,global_task_l,liste_dir,liste_dir_task):
            global_task_l,liste_dir=global_task_l,liste_dir
            liste_dir_task=liste_dir_task
            liste=[]
            for p in range(len(liste_dir)):
                l=[]
                for i in range(liste_dir_task[p]):
                  pp=[]
                  for j in range(liste_dir[p]+1):
                    sub=[]
                    size_u=random.randint(int((global_task_l[p][i][0])/(liste_dir[p]+1)),int((global_task_l[p][i][0])/(liste_dir[p]-2)))
                    sub.append(size_u)
                    n_cpu_u=random.randint(5,int((global_task_l[p][i][1])/liste_dir[p]+1))
                    sub.append(n_cpu_u)
                    b_u=random.randint(1,global_task_l[p][i][2])
                    sub.append(b_u)
                    time_u=random.randint(int((global_task_l[p][i][3])/10)+3,int((global_task_l[p][i][3]/5)+5))
                    sub.append(time_u)
                    pp.append(sub)
                  l.append(pp)
                liste.append(l)
            return liste
              






        def task_to_subtask(self,global_task,task_vehicle,liste_dir):
          """ Affiche la list des soustaches pour chaque tache originale générée"""
          self.task_vehicle=task_vehicle
          self.global_task=global_task
          self.liste_dir=liste_dir
          liste_for_sub_task_d=[]
          liste_for_sub_task_u=[]
          liste_for_sub_task_l=[]
          liste_for_sub_task_r=[]
          for i in range(len(self.global_task)):
                
                if self.task_vehicle[i].direction=='d':
                    l=[]
                    for j in range(self.liste_dir[0]+1):
                      sub_task=[]
                      self.size_u=random.randint(int((self.global_task[i][0])/(self.liste_dir[0]+1)),int((self.global_task[i][0])/(self.liste_dir[0]-2)))
                      sub_task.append(self.size_u)
                      self.n_cpu_u=random.randint(5,int((self.global_task[i][1])/self.liste_dir[0]+1))
                      sub_task.append(self.n_cpu_u)
                      self.b_u=random.randint(1,self.global_task[i][2])
                      sub_task.append(self.b_u)
                      self.time_u=random.randint(int((self.global_task[i][3])/10)+3,int((self.global_task[i][3]/5)+5))
                      sub_task.append(self.time_u)
                      l.append(sub_task)
                    liste_for_sub_task_d.append(l)
                    continue
                      #self.liste_for_sub_task.append(self.list_sub_task)
                if self.task_vehicle[i].direction=='u':
                    l=[]
                    for j in range(self.liste_dir[1]+1):
                      sub_task=[]
                      self.size_u=random.randint(int((self.global_task[i][0])/(self.liste_dir[1]+1)),int((self.global_task[i][0])/(self.liste_dir[1]-2)))
                      sub_task.append(self.size_u)
                      self.n_cpu_u=random.randint(5,int((self.global_task[i][1])/self.liste_dir[1]+1))
                      sub_task.append(self.n_cpu_u)
                      self.b_u=random.randint(1,self.global_task[i][2])
                      sub_task.append(self.b_u)
                      self.time_u=random.randint(int((self.global_task[i][3])/10)+3,int((self.global_task[i][3]/5)+5))
                      sub_task.append(self.time_u)
                      l.append(sub_task)
                    liste_for_sub_task_u.append(l)
                    continue
                      #self.liste_for_sub_task.append(self.list_sub_task)
                if self.task_vehicle[i].direction=='l':
                    l=[]
                    for j in range(self.liste_dir[2]+1):
                      sub_task=[]
                      self.size_u=random.randint(int((self.global_task[i][0])/(self.liste_dir[2]+1)),int((self.global_task[i][0])/(self.liste_dir[2]-2)))
                      sub_task.append(self.size_u)
                      self.n_cpu_u=random.randint(5,int((self.global_task[i][1])/self.liste_dir[2]+1))
                      sub_task.append(self.n_cpu_u)
                      self.b_u=random.randint(1,self.global_task[i][2])
                      sub_task.append(self.b_u)
                      self.time_u=random.randint(int((self.global_task[i][3])/10)+3,int((self.global_task[i][3]/5)+5))
                      sub_task.append(self.time_u)
                      l.append(sub_task)
                    liste_for_sub_task_l.append(l)
                    continue
                      #self.liste_for_sub_task.append(self.list_sub_task)
                if self.task_vehicle[i].direction=='r':
                    l=[]
                    for j in range(self.liste_dir[3]+1):
                      sub_task=[]
                      self.size_u=random.randint(int((self.global_task[i][0])/(self.liste_dir[3]+1)),int((self.global_task[i][0])/(self.liste_dir[3]-2)))
                      sub_task.append(self.size_u)
                      self.n_cpu_u=random.randint(5,int((self.global_task[i][1])/self.liste_dir[3]+1))
                      sub_task.append(self.n_cpu_u)
                      self.b_u=random.randint(1,self.global_task[i][2])
                      sub_task.append(self.b_u)
                      self.time_u=random.randint(int((self.global_task[i][3])/10)+3,int((self.global_task[i][3]/5)+5))
                      sub_task.append(self.time_u)
                      l.append(sub_task)
                    liste_for_sub_task_r.append(l)
                    continue
                      #self.liste_for_sub_task.append(self.list_sub_task)
          return [liste_for_sub_task_d,liste_for_sub_task_u,liste_for_sub_task_l,liste_for_sub_task_r] # liste en [i,j]

        def global_task(self,number_task_vehicle):
          self.number_task_vehicle=number_task_vehicle
          liste=[]
          for i in range(self.number_task_vehicle):
            liste.append(self.tasks_generation())
          return liste # liste en [i,j]

        def global_task_l(self,liste_dir_task):
            liste_dir_task=liste_dir_task
            #d,u,l,r=[],[],[],[]
            liste=[]
            for p in range(len(liste_dir_task)):
                #l=[]
                m=[]
                for i in range(liste_dir_task[p]):
                  m.append(self.tasks_generation())
                #l.append(m)
                liste.append(m)
                
            return liste
                
        def max_time_add_to_task_l(self,vehicle,global_task_l:list): # ajoute lt tmax à la tache et retourne la tache 
          self.vehicle=vehicle # list of couple (x,y)
          self.global_task_l=global_task_l
          pp=[i for i in range(len(self.vehicle))]
          big_list=[]
          for p in range(len(self.global_task_l)):
            l=[]
            for i in range(len(global_task_l[p])):
              self.task_priority=random.random()
              g=random.sample(pp,1)[0]
              liste=[]
              liste.append(self.global_task_l[p][i][0])
              liste.append(self.global_task_l[p][i][1])
              liste.append(self.global_task_l[p][i][2])
              liste.append((self.task_priority*((self.vehicle[g].position[0])**2+(self.vehicle[g].position[1])**2)*self.global_task_l[p][i][0])*10**(-6))
              l.append(liste)
            big_list.append(l)
          return big_list # liste en [i,j]



        
        def max_time_add_to_task(self,vehicle,global_task:list): # ajoute lt tmax à la tache et retourne la tache 
          self.vehicle=vehicle # list of couple (x,y)
          self.global_task=global_task
          big_list=[]
          for i in range(len(self.global_task)):
            self.task_priority=random.random()
            liste=[]
            liste.append(self.global_task[i][0])
            liste.append(self.global_task[i][1])
            liste.append(self.global_task[i][2])
            liste.append((self.task_priority*((self.vehicle[i].position[0])**2+(self.vehicle[i].position[1])**2)*self.global_task[i][0])*10**(-6))
            big_list.append(liste)
          return big_list # liste en [i,j]
        
        def total_resource_task(self,ressource_required,liste_dir,liste_dir_task): # calcul la somme des resources alloué a la tache repartie entre les véhicules de services
          self.ressource_required=ressource_required
          self.liste_dir,self.liste_dir_task=liste_dir,liste_dir_task
          u=[]
          d=[]
          l=[]
          r=[]
          #service_vehicle=service_vehicle
          for p in range(len(self.liste_dir)):
            if p==0:
                for i in range(self.liste_dir_task[p]):
                        som=0
                        for j in range(1,self.liste_dir[p]+1):
                            som=som+self.ressource_required[p][i][j-1]
                        d.append(som)
            if p==1:
                for i in range(self.liste_dir_task[p]):
                        som=0
                        for j in range(1,self.liste_dir[p]+1):
                            som=som+self.ressource_required[p][i][j-1]
                        u.append(som)
            if p==2:
                for i in range(self.liste_dir_task[p]):
                        som=0
                        for j in range(1,self.liste_dir[p]+1):
                            som=som+self.ressource_required[p][i][j-1]
                        l.append(som)
            if p==3:
                for i in range(self.liste_dir_task[p]):
                        som=0
                        for j in range(1,self.liste_dir[p]+1):
                            som=som+self.ressource_required[p][i][j-1]
                        r.append(som)
                        #liste.append(som)
                #l.append(liste)
          #listes.append(l)
          return [d,u,l,r]