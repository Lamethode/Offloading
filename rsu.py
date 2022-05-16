#@title
class  RSU :

   def __init__(self,n_RSU):
     self.n_RSU=n_RSU
     self.direction=['d','u','l','r']

   def RSU (self,status,n_RSU,rsu_x_pos,rsu_y_pos,n_saut,direction):
    self.status=status  # pour oui si le RSU est directement connecté au serveur non sinon
    self.n_RSU=n_RSU
    self.rsu_x_pos=rsu_x_pos #position-x du rsu en mètre
    self.rsu_y_pos=rsu_y_pos #position-x du rsu en mètre
    self.n_saut=n_saut
    self.direction=direction
    
    return self.status,self.n_RSU,self.direction,[self.rsu_x_pos,self.rsu_y_pos]
  
   def get_rsu_pos(self,rsu_x_pos,rsu_y_pos,n_RSU ):
    self.x_pos=rsu_x_pos
    self.y_pos=rsu_y_pos
    self.RSU_pos=[]
    self.RSU_pos.append(self.x_pos)
    self.RSU_pos.append(self.y_pos)
    return self.RSU_pos
  
   def add_rsu(self): #permet de definir la liste des RSU il fautr s'inspirere de l'ajout des véhucles par nombres
    liste=[]
    for i in range(4):
      if i==0:
        liste.append(self.RSU(True,i,50,0,0,'r'))
      elif (i==1):
         liste.append(self.RSU(False,i,100,0,1,'u'))
      elif (i==2):
         liste.append(self.RSU(False,i,-50,-50,1,'d'))
      else:
         liste.append(self.RSU(False,i,-50,0,2,'l'))
    return liste


   def time_rsu_cloud(self,a,Task_size_u,resource_serv,resource_task_u,RSU_connect):
      self.R_lan=10**9
      self.RSU_connect=RSU_connect
      self.a=a
      self.Task_size_u=Task_size_u
      self.resource_task_u=resource_task_u
      self.resource_serv=resource_serv
      self.delta_t=0.5
      return ((self.a*self.Task_size_u*(self.resource_task_u-self.resource_serv)/(self.R_lan*self.resource_task_u+0.0001))+self.RSU_connect*self.delta_t)

   def liste_time_rsu_cloud(self,a_list,ressource_serv,resource_required,RSU,sub_task_u,liste_dir,liste_dir_task):
    liste_dir,liste_dir_task
    m=[]
    self.a_list,self.ressource_serv,self.resource_required,self.RSU,self.sub_task_u=a_list,ressource_serv,resource_required,RSU,sub_task_u
    for p in range(len(liste_dir)):
            if p==0:
                liste=[]
                rsu=RSU[2][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_rsu_cloud(self.a_list[p][i][j-1],self.sub_task_u[p][i][j][0],self.ressource_serv[p][j-1],self.resource_required[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
            elif p==1:
                liste=[]
                rsu=RSU[1][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_rsu_cloud(self.a_list[p][i][j-1],self.sub_task_u[p][i][j][0],self.ressource_serv[p][j-1],self.resource_required[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
            elif p==2:
                liste=[]
                rsu=RSU[3][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_rsu_cloud(self.a_list[p][i][j-1],self.sub_task_u[p][i][j][0],self.ressource_serv[p][j-1],self.resource_required[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
            elif p==3:
                liste=[]
                rsu=RSU[0][1]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_rsu_cloud(self.a_list[p][i][j-1],self.sub_task_u[p][i][j][0],self.ressource_serv[p][j-1],self.resource_required[p][i][j],rsu))
                    liste.append(k)
                m.append(liste)
                      
    return m

   def time_return (self,a,b,size_u,resource_required,resource_service,data_rate_v2i):
      self.b_u=b
      self.a=a
      self.size_u=size_u
      self.resource_required=resource_required
      self.resource_service=resource_service
      self.data_rate_v2i=data_rate_v2i

      return ((self.a*size_u*self.b_u*(resource_required-resource_service))/(data_rate_v2i*resource_required+0.05))


   def liste_return_time_rsu(self,a_list,ressource_serv,resource_required,sub_task_u,data_rate_v2i,liste_dir,liste_dir_task):
    m=[]
    a_list,ressource_serv,resource_required,data_rate_v2i,sub_task_u=a_list,ressource_serv,resource_required,data_rate_v2i,sub_task_u
    for p in range(len(liste_dir)):
                liste=[]
                for i in range(liste_dir_task[p]):
                    k=[]
                    for j in range(1,liste_dir[p]+1):
                            k.append(self.time_return(a_list[p][i][j-1],sub_task_u[p][i][j][3],sub_task_u[p][i][j][0],ressource_serv[p][j-1],resource_required[p][i][j],data_rate_v2i[p][i]))
                    liste.append(k)
                m.append(liste)
                
    return m

# intégration de RSU mobiles dans le scénario