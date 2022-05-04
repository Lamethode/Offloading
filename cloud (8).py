#@title
import random




Pcloud=random.randint(100,200)



class  CloudServer :
    """
    1-diffusion du prix unitaire en tenant compte de la puissance maximale su cloud serveur
    2- temps traitement de la tache du vehicule
    3- temps d'envoi au véhicle de tache pour le resulat

    """

    def __init__(self):
        self.ressource=100000000
        self.Pcloud=random.randint(100,200)
        #self.CPU=1000 a vérifié
        self.direction=['d','u','l','r']
    
    def get_init_cloud(self,liste_dir):
        liste=[]
        for p in range(len(liste_dir)):
            l=[]
            for i in range(liste_dir[p]):
                l.append(0)
            liste.append(l)
        return liste

    def ressource_used(self,check_msg,ressoure_required,initial_cloud,liste_dir):
        self.check_msg=check_msg
        self.ressoure_required=ressoure_required
        self.initial_cloud=initial_cloud
        for p in range(len(liste_dir)):
            for i in range(liste_dir[p]):
                if self.check_msg[p][i]==False:
                    pass
                else:
                    for j in range(1,liste_dir[p]+1):
                        self.initial_cloud[p][j-1]=self.initial_cloud[p][j-1]+self.ressoure_required[p][i][j]
        return self.initial_cloud
        
    
    def broadcast_price (self):
        price=self.Pcloud # a remplacer par --self.Pcloud=150
        return price
    
    def exec_time (self,a,cpu_u_required,Task_size_u,resource_required,service_ressource): # fonction resource required doit etre crée et aussi pour  a -propoertion de décharge a voir de pret 
      self.a=a
      self.service_ressource=service_ressource
      self.cpu_u_required=cpu_u_required
      self.Task_size_u=Task_size_u
      self.resource_required=resource_required 
      self.resource_required=self.resource_required-self.service_ressource
    
      return (self.a*self.cpu_u_required*self.Task_size_u)/(self.resource_required)
      # liste pour stocker ces différents temps de calcul à définir 

    def liste_exec_time(self,a_liste,subtask,ressources_required,resource_serv,liste_dir,liste_dir_task):
        self.a_liste=a_liste
        self.subtask=subtask
        self.ressources_required=ressources_required
        self.resource_serv=resource_serv
        liste=[]
        for p in range(len(liste_dir_task)):
            m=[]
            for i in range(liste_dir_task[p]):
                l=[]
                for j in range(1,liste_dir[p]+1):
                    h=self.exec_time(self.a_liste[p][i][j-1],self.subtask[p][i][j][1],self.subtask[p][i][j][0],self.ressources_required[p][i][j],self.resource_serv[p][j-1])
                    l.append(h)
                m.append(l)
            liste.append(m)
        return liste
                
    
    
    def time_cloud_rsu(self,a,b,Task_size_u,resource_required,resource_task_u,RSU_connect):
      self.b_u=b
      self.R_lan=10**9
      self.a=a
      self.Task_size_u=Task_size_u
      self.resource_task_u=resource_task_u
      self.resource_required=resource_required
      self.RSU_connect=RSU_connect
      self.delta_t=0.5

      return (((self.a*self.b_u*self.Task_size_u*self.resource_required)/(self.R_lan*self.resource_task_u+0.001))+self.RSU_connect*self.delta_t)

    def liste_time_cloud_rsu(self,a_list,ressource_serv,resource_required,RSU,sub_task_u,liste_dir,liste_dir_task):
        m=[]
        self.a_liste,self.ressource_servs,self.resource_requireds,self.RSU,self.sub_task_us=a_list,ressource_serv,resource_required,RSU,sub_task_u
        for p in range(len(liste_dir)):
            if p==0:
                liste=[]
                rsu=RSU[2][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_cloud_rsu(self.a_liste[p][i][j-1],self.sub_task_us[p][i][j][3],self.sub_task_us[p][i][j][0],self.ressource_servs[p][j-1],self.resource_requireds[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
            elif p==1:
                liste=[]
                rsu=RSU[1][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_cloud_rsu(self.a_liste[p][i][j-1],self.sub_task_us[p][i][j][3],self.sub_task_us[p][i][j][0],self.ressource_servs[p][j-1],self.resource_requireds[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
            elif p==2:
                liste=[]
                rsu=RSU[3][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_cloud_rsu(self.a_liste[p][i][j-1],self.sub_task_us[p][i][j][3],self.sub_task_us[p][i][j][0],self.ressource_servs[p][j-1],self.resource_requireds[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
            elif p==3:
                liste=[]
                rsu=RSU[0][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_cloud_rsu(self.a_liste[p][i][j-1],self.sub_task_us[p][i][j][3],self.sub_task_us[p][i][j][0],self.ressource_servs[p][j-1],self.resource_requireds[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
        return m
        

   
    def update_ressource(self,resource_required,resource_cloud,liste_dir):
      self.resource_required=resource_required
      self.resource_cloud=resource_cloud
      for p in range(len(liste_dir)):
            for j in range(liste_dir[p]):
                self.resource_cloud=self.resource_cloud-self.resource_required[p][j]
      return self.resource_cloud

    def resource_per_task(self,num_service_vehicle,resource_required): # liste des ressources de décharges des véhicules de services vers le serveur cloud
      self.num_service_vehicle=num_service_vehicle
      self.resource_required=resource_required
      liste=[]
      for i in len(self.send_to_cloud_msg_list):
        if self.send_to_cloud_msg_list[i]==True:
          liste.append(self.resource_required[i])
      return liste

    
    def time_cloud(self,up_time,rsu_cloud_time,exec_time,cloud_rsu_time,down_time): # temps de calcul de la tache u en utilisant la communication v2i
      self.up_time=up_time
      self.rsu_cloud_time=rsu_cloud_time
      self.exec_time=exec_time
      self.cloud_rsu_time=cloud_rsu_time
      self.down_time=down_time
      return (self.up_time+self.rsu_cloud_time+ self.exec_time+self.cloud_rsu_time+self.down_time)
    
    def liste_time_cloud(self,list_up_time,list_rsu_cloud_time,list_exec_time,list_cloud_rsu_time,list_down_time,check_message,liste_dir,liste_dir_task):
        list_up_time,list_rsu_cloud_time,list_exec_time,list_cloud_rsu_time,list_down_time=list_up_time,list_rsu_cloud_time,list_exec_time,list_cloud_rsu_time,list_down_time
        check_message=check_message
        liste=[]
        for p in range(len(liste_dir)):
            m=[]
            for i in range(liste_dir_task[p]):
                l=[]
                for j in range(liste_dir[p]):
                    if check_message[p][j]==False:
                        l.append(0)
                    else:
                        l.append(self.time_cloud(list_up_time[p][i][j],list_rsu_cloud_time[p][i][j],list_exec_time[p][i][j],list_cloud_rsu_time[p][i][j],list_down_time[p][i][j]))
                m.append(l)
            liste.append(m)
        return liste

cloud=CloudServer()       
