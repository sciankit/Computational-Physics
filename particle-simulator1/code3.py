## Importing Libraries

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


## Collision Detection
###############
def collision(particle1,particle2):
    x1,y1=particle1[0],particle1[1]
    #print(x1,y1)
    x2,y2=particle2[0],particle2[1]
    #print(x2,y2)
    r1,r2 = particle1[4],particle2[4]
    dis = ((x1-x2)**2+(y1-y2)**2)**0.5
    print(x1,x2,y1,y2, "-->", dis-r1-r2)
    #print(dis, "distance_between particle center")
    return(dis-r1-r2)

## Cartesian to Polar convertor
#######################
def cart2pol(v1,v2):
    V = (v1**2+v2**2)**0.5
    theta = math.atan(v2/v1)
    if v1<0:
        theta=theta+math.pi
        
    return(V,theta)

## Polar to Cartesian Convertor
#########################
def pol2cart(V,theta):
    v1 = V*math.cos(theta)
    v2 = V*math.sin(theta)
    return(v1,v2)

## Collision Tangent plane angle 
###########################
def collision_angle(pos1,pos2):
    if pos1[0]-pos2[0]==0:
        angle_collisoin = 0+math.pi/2
    else:
        angle_collisoin = math.atan((pos1[1]-pos2[1])/(pos1[0]-pos2[0]))+math.pi/2
    #print(angle_collisoin*360/2/math.pi)
    return(angle_collisoin)


## Velocity update on collision
##########################
def velocity_update(particle,angle):
    V,theta = cart2pol(particle[2],particle[3])
    print("angle before",180/math.pi*theta)
    print(180/math.pi*angle,"angle")
    theta = -theta+2*angle
    print("angle after", 180/math.pi*theta)
    #coeff_of_rest  = 0.95
    #V = V*coeff_of_rest
    particle[2],particle[3]=pol2cart(V,theta)
    return(particle)
    #print(angle_of_collision)

## Position Update when velocity is know
###########################
def position_update(particle):
    particle[0]=particle[0]+particle[2]*delT
    particle[1]=particle[1]+particle[3]*delT
    return(particle)

## Variables
############
delT = 0.01
time_step=10
scats=[]
colour = ["blue","green","red","cyan","magenta","yellow","black"]


## Importing Data
##################
df = pd.read_csv(r'BodyData.dat')
data = df.values.tolist()
#print(data)
def pop(list1):
    list1.pop(0)
    #print(list1)
    return(list1)
data = list(map(pop,data))


fig = plt.figure(figsize=(7,5))

## Main SIMULATION FUNCTION
def main_sim(i):

    ### Scatter plot Animation
    ####################
    global scats
    for scat in scats:
        scat.remove()
    scats=[]
    plt.xlim(-2,3.5)
    plt.ylim(-2,3.5)

    for j in range(len(data)):
        point=data[j]
        #print(i,point)
        scats.append(plt.scatter(point[0],point[1],color=colour[j],s=2500*point[4]))
    
    ### COLLISION BETWEEN EACH PAIR
    ##################
    collision_list= []   ## List containing all colliding pair for given time step
    for j in range(len(data)):
        if j == len(data):
            break
        for k in range(len(data)-j-1):
            collied = collision(data[j],data[j+k+1])  ## COllision detection
            #print(collied, "collision_value")

            if collied<0:
                print("collision detected", collied)
                collision_list.append((j,j+k+1))
    if collision_list != []:
        for j in range(len(collision_list)):
            pair = collision_list[j]
            particle1 = data[pair[0]]
            particle2 = data[pair[1]]
            angle = collision_angle(particle1,particle2)
            #print(180/math.pi*angle)
            data[pair[0]] = velocity_update(particle1,angle)
            data[pair[1]] = velocity_update(particle2,angle)
            
    for j in range(len(data)):
        data[j]=position_update(data[j])


## Animation Command
animation = FuncAnimation(fig, main_sim, 50,interval=time_step)
plt.show()



