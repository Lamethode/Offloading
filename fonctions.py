from copy import copy, deepcopy
import numpy as np
import pandas as pd


def liste_dir_function(vehicle,num):
    up=[]
    down=[]
    right=[]
    left=[]
    liste_dir=[]
    for i in range(num):
        if vehicle[i].direction=='d':
            down.append(vehicle[i].indexe)
        elif  vehicle[i].direction=='u':
            up.append(vehicle[i].indexe)
        elif vehicle[i].direction=='l':
            left.append(vehicle[i].indexe)
        else:
            right.append(vehicle[i].indexe)
    liste_dir.append(down)
    liste_dir.append(up)
    liste_dir.append(left)
    liste_dir.append(right)
    return liste_dir

def liste_dir_functions(vehicle,num,name):
    up=[]
    down=[]
    right=[]
    left=[]
    liste_dir=[]
    for i in range(num):
        if vehicle[i].direction=='d':
            direction='down_road'
            down.append((direction,name+' {0}'.format(i)))
        elif  vehicle[i].direction=='u':
            direction='up_road'
            up.append((direction,name+' {0}'.format(i)))
        elif vehicle[i].direction=='l':
            direction='left_road'
            left.append((direction,name+' {0}'.format(i)))
            
        else:
            direction='right_road'
            right.append((direction,name+' {0}'.format(i)))
            
    liste_dir.append(down)
    liste_dir.append(up)
    liste_dir.append(left)
    liste_dir.append(right)
    return liste_dir



def update_r1(element_to_update,actual_index,update_index):
  actual_index,update_index=actual_index,update_index
  old_one=element_to_update
  old_two=deepcopy(old_one)
  
  for p in range(len(actual_index)):
    if type(old_one[p]) is list:
        if old_one[p]==[]:
              old_one[p].append(0)
        else:
          pass
    else:
          elt=deepcopy(old_one[p])
          old_one[p]=[]
          old_one[p].append(elt)
    

    if len(actual_index[p])-len(update_index[p])==0:
      t=set(actual_index[p])
      x=set(update_index[p])
      h=t-x
      h=list(h)
      if h==[]:
        for i in update_index[p]:
          if i not in actual_index[p]:
              new_position=update_index[p].index(i)
              for c in range(len(actual_index)):
                if i in actual_index[c]:
                  old_position=actual_index[c].index(i)
                  l=old_two[c][old_position]
                  break
              old_one[new_position]=l

    elif len(actual_index[p])-len(update_index[p])>0:
      i=len(actual_index[p])-len(update_index[p])
      t=set(actual_index[p])
      x=set(update_index[p])
      h=t-x
      h=list(h)
      for k in range(len(h)):
        m=h[k]
        old_position=actual_index[p].index(m)
        l=old_two[p][old_position]
        old_one[p].remove(l)
        if type(old_one[p]) is list:
            pass
        elif old_one[p]==[]:
          old_one[p].append(0)
        else:
          elt=deepcopy(old_one[p])
          old_one[p]=[]
          old_one[p].append(elt)
    elif len(actual_index[p])-len(update_index[p])<0:
      #print(actual_index[p])
      #print('\n')
      #print(update_index[p])
      i=abs(len(actual_index[p])-len(update_index[p]))
      t=set(actual_index[p])
      x=set(update_index[p])
      h=x-t
      h=list(h)
      for k in range(len(h)):
        mm=h[k]
        new_position=update_index[p].index(mm)
        for c in range(len(actual_index)):
            if mm in actual_index[c]:
              old_position=actual_index[c].index(mm)
              ll=old_two[c][old_position]
        old_one[p].insert(new_position,ll)
        if type(old_one[p]) is list:
            pass
        else:
          elt=deepcopy(old_one[p])
          old_one[p]=[]
          old_one[p].append(elt)
  

  #print(old_one==old_two)
  return old_one


def liste_dir_func(vehicle,num):
    up=0
    down=0
    right=0
    left=0
    liste_dir=[]
    for i in range(num):
        if vehicle[i].direction=='d':
            down=down+1
        elif  vehicle[i].direction=='u':
            up=up+1
        elif vehicle[i].direction=='l':
            left=left+1
        else:
            right=right+1
    liste_dir.append(down)
    liste_dir.append(up)
    liste_dir.append(left)
    liste_dir.append(right)
    return liste_dir
    
def liste_dir_task_func(vehicle,num):
    up=0
    down=0
    right=0
    left=0
    liste_dir=[]
    for i in range(num):
        if vehicle[i].direction=='d':
            down=down+1
        elif  vehicle[i].direction=='u':
            up=up+1
        elif vehicle[i].direction=='l':
            left=left+1
        else:
            right=right+1
    liste_dir.append(down)
    liste_dir.append(up)
    liste_dir.append(left)
    liste_dir.append(right)
    return liste_dir

def concatenat(liste):
  l=[]
  for p in range(len(liste)):
      m=[]
      if len(liste[p][0][0])<=3:
        m=liste[p][0][0]
        m.append(liste[p][0][1])
        m.append(liste[p][0][2])
        m.append(liste[p][0][3])
        l.append(np.array(m))
      else: 
        m=np.array(liste[p][0][0])
        l.append(m)
  return l


def concat(liste):
    l=[]
    for p in range(len(liste)):
        m=[]
        if len(liste[p][0][0])<=3:
          m=liste[p][0][0]
          #l.append(np.array(m))
          for i in range(len(liste[p][0][1])):
            for j in range(len(liste[p][0][1][0])):
              m.append(liste[p][0][1][i][j])
          for i in range(len(liste[p][0][2])):
              m.append(liste[p][0][2][i])
          m.append(liste[p][0][3])
          for i in range(len(liste[p][0][4])):
              m.append(liste[p][0][4][i])
          l.append(np.array(m))        
        else: 
          l.append(np.array(liste[p][0][0]))
        
    return l

def change_format_1(vehicle,states,next_states,action,reward):
# fonction de formation de direction a général
              ddj,uuj,llj,rrj=0,0,0,0
              reward=reward
              states=states
              next_states=next_states
              action=action
              reward=reward

              
              big_states=[]
              big_next_states=[]
              big_actions=[]
              big_rewards=[]
              
              for i in range(len(vehicle)):
                dd1,uu1,ll1,rr1=[],[],[],[]
                dd2,uu2,ll2,rr2=[],[],[],[]
                
                if vehicle[i].direction=='d':
                  n=[]  
                  dd1.append(states[0][ddj])
                  n.append(reward[0][ddj])
                  dd2.append(next_states[0][ddj])
                  big_actions.append(action[0][ddj])
                  big_rewards.append(n)
                  big_states.append(dd1)
                  big_next_states.append(dd2)
                  ddj+=1

                elif vehicle[i].direction=='u':
                  n=[]
                  uu1.append(states[1][uuj])
                  n.append(reward[1][uuj])
                  uu2.append(next_states[1][uuj])
                  big_actions.append(action[1][uuj])
                  big_rewards.append(n)
                  big_states.append(uu1)
                  big_next_states.append(uu2)
                  uuj+=1

                elif vehicle[i].direction=='l':
                      n=[]                      
                      ll1.append(states[2][llj])
                      n.append(reward[2][llj])
                      ll2.append(next_states[2][llj])
                      big_actions.append(action[2][llj])
                      big_rewards.append(n)
                      big_states.append(ll1)
                      big_next_states.append(ll2)
                      llj+=1

                elif vehicle[i].direction=='r':
                      n=[]                      
                      rr1.append(states[3][rrj])
                      n.append(reward[3][rrj])
                      rr2.append(next_states[3][rrj])
                      big_actions.append(action[3][rrj])
                      big_rewards.append(n)
                      big_states.append(rr1)
                      big_next_states.append(rr2)
                      rrj+=1

              return big_states,big_next_states,big_actions,big_rewards

def stock_states(vehicle,states):
  liste=[]
  state=deepcopy(states)
  vv=[]
  for pp in range(len(vehicle)):
    if len(state[pp][0][0])<=3:
      vv= state[pp][0][0]
      vv.append(vehicle[pp].direction)
      liste.append(vv)
    else:
      vv=state[pp][0][0][:3]
      vv.append(vehicle[pp].direction)
      liste.append(vv)

  return liste

def state_diz(states):
    states=deepcopy(states)
    x=[]
    y=[]
    speed=[]
    direction=[]
    for i in range(len(states)):
      x.append(states[i][0])
      y.append(states[i][1])
      speed.append(states[i][2])
      direction.append(states[i][3])
    
    return [x,y,speed,direction]




def change_format_2(vehicle,liste):
    # le formattage des autres listes
    ddj,uuj,llj,rrj=0,0,0,0
    big_liste=[]
    listes=deepcopy(liste)
    for i in range(len(vehicle)):
      if vehicle[i].direction=='d':
        big_liste.append(listes[0][ddj])
        ddj+=1
      elif vehicle[i].direction=='u':
          big_liste.append(listes[1][uuj])
          uuj+=1
      elif vehicle[i].direction=='l':
          big_liste.append(listes[2][llj])
          llj+=1
      elif vehicle[i].direction=='r':
          big_liste.append(listes[3][rrj])
          rrj+=1
    return big_liste


def create_dataset_service(grande_episode_serv,grande_states_serv,grande_resources_serv,grande_price_base,grande_msg_cloud,grande_compute_to_cloud):
      df1=pd.DataFrame()
      df2_1=pd.DataFrame()
      df2_2=pd.DataFrame()
      df2_3=pd.DataFrame()
      df2_4=pd.DataFrame()
      df3=pd.DataFrame()
      df4=pd.DataFrame()
      df5=pd.DataFrame()
      df6=pd.DataFrame()
      

      for k in range(len(grande_resources_serv)):
          number_episode=pd.DataFrame({"number_episode": grande_episode_serv[k]})
          df1=df1.append(number_episode,ignore_index=True)
          

          x_coord=pd.DataFrame({"x_coord": grande_states_serv[k][0]})
          df2_1=df2_1.append(x_coord,ignore_index=True)

          y_coord=pd.DataFrame({"y_coord": grande_states_serv[k][1]})
          df2_2=df2_2.append(y_coord,ignore_index=True)

          speed=pd.DataFrame({"speed": grande_states_serv[k][2]})
          df2_3=df2_3.append(speed,ignore_index=True)       


          direction=pd.DataFrame({"direction": grande_states_serv[k][3]})
          df2_4=df2_4.append(direction,ignore_index=True)

          resources_serv=pd.DataFrame({"resources_serv": grande_resources_serv[k]})
          df3=df3.append(resources_serv,ignore_index=True)

          price_base=pd.DataFrame({"unit_price": grande_price_base[k]})
          df4=df4.append(price_base,ignore_index=True)

          msg_cloud=pd.DataFrame({"Is_offloaded_to_cloud": grande_msg_cloud[k]})
          df5=df5.append(msg_cloud,ignore_index=True)

          compute_to_cloud=pd.DataFrame({"compute_to_cloud": grande_compute_to_cloud[k]})
          df6=df6.append(compute_to_cloud,ignore_index=True)

      frame=[df1,df2_1,df2_2,df2_3,df2_4,df3,df4,df5,df6]
      result = pd.concat(frame,axis=1)

      return result


def change_format_3(vehicle,states,next_states):
# fonction de formation de direction a général
              ddj,uuj,llj,rrj=0,0,0,0
              states=states
              next_states=next_states
              
              big_states=[]
              big_next_states=[]
              big_actions=[]
              big_rewards=[]
              
              for i in range(len(vehicle)):
                dd1,uu1,ll1,rr1=[],[],[],[]
                dd2,uu2,ll2,rr2=[],[],[],[]
                
                if vehicle[i].direction=='d': 
                  dd1.append(states[0][ddj])
                  dd2.append(next_states[0][ddj])
                  big_rewards.append(n)
                  big_states.append(dd1)
                  big_next_states.append(dd2)
                  ddj+=1

                elif vehicle[i].direction=='u':

                  uu1.append(states[1][uuj])
                  
                  uu2.append(next_states[1][uuj])
                          
                  big_states.append(uu1)
                  big_next_states.append(uu2)
                  uuj+=1

                elif vehicle[i].direction=='l':
                                   
                      ll1.append(states[2][llj])

                      ll2.append(next_states[2][llj])
                    
                      big_states.append(ll1)
                      big_next_states.append(ll2)
                      llj+=1

                elif vehicle[i].direction=='r':
                                           
                      rr1.append(states[3][rrj])
                    
                      rr2.append(next_states[3][rrj])
                  
                   
                      big_states.append(rr1)
                      big_next_states.append(rr2)
                      rrj+=1

              return big_states,big_next_states
