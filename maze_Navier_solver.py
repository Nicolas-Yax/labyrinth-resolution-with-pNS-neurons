import sqlite3
import copy
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from matplotlib import animation
import time
#------------------------------
#
# * Labyrinth Loading functions *
#
#------------------------------

def load_lab(index):
    conn = sqlite3.connect("labcroiss.db")
    c = conn.cursor()
    c.execute("SELECT * FROM lab")
    lab = None
    for i in range(index):
        lab = eval(c.fetchone()[0])
    assert lab != None
    return lab
                
def close_maze(laby):
    for i in range(len(laby)):
        laby[i].append(1)
        laby[i].insert(0,1)
    laby.append([1 for i in range(len(laby[0]))])
    laby.insert(0,[1 for i in range(len(laby[0]))])
    return laby

lab = load_lab(2) #Load the second maze
maze = close_maze(lab) #Close the maze (adds a border of walls around it)
V = [[(0,0) for j in i] for i in maze] #Initialization of the values of the neural network
#------------------------------
#
# * Usefull functions *
#
#------------------------------

def allowed_pos(x,y):
    allowed_x = x>=0 and x<len(maze[0])
    allowed_y = y>=0 and y<len(maze)
    return allowed_x and allowed_y

def access(x,y):
    return V[y][x]

def affect(x,y,val):
    V[y][x] = val

def is_obstacle(x,y):
    return maze[y][x] == 1

def move_list():
    return [(1,0),(-1,0),(0,1),(0,-1)]

def sg(x):
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0

#------------------------------
#
# * Resolution *
#
#------------------------------

X = 1
Y = 1
APOS = (0,1) #Previous position

N = 0

START = (1,1) #Start position
END = (25,25) #BE CAREFULL !!! This position MUST be accessible or the algorithme will never find it !

SCORE = [] #Only to store values in a database
NB_STEP = 0

def solve(pos,ancient_pos): #Solve the pNS Equation it needs the current position and the previous one
    (x,y) = pos
    (ax,ay) = ancient_pos
    #List of all possible next position
    list_new_pos = [(x+a,y+b,a+b,b) for a,b in move_list()
                    if allowed_pos(x+a,y+b)
                    and not(is_obstacle(x+a,y+b))
                    and (x+a,y+b) != ancient_pos]
    #If it's empty, we add the previous one with all necessary information
    if list_new_pos == []:
        list_new_pos = [(x+a,y+b,a+b,b) for a,b in move_list()
                        if allowed_pos(x+a,y+b)
                        and not(is_obstacle(x+a,y+b))
                        and (x+a,y+b) == ancient_pos]
    ddiv = 0-sum([(a+b)*access(x+a,y+b)[b] for a,b in move_list()]) #Computation of ddiv
    (a,b,g,h) = (access(x+1,y)[0],access(x-1,y)[0],access(x,y+1)[1],access(x,y-1)[1])
    if (x,y) == START: #The value of div
        ddiv += 1.0
    elif (x,y) == END:
        ddiv -= 1.0
    elif not(a or b or g or h): #Lost case (shouldn't occur)
        ddiv += 0
    #Computation of the sum factor
    somme = sum([abs(access(i,j)[index]) for (i,j,s,index) in list_new_pos])
    
    #Correct self div organelle and correct other div organelle
    for (i,j,s,index) in list_new_pos:
        v = access(i,j)[index]
        if somme != 0:
            if len([access(k,l)[index2] for (k,l,s2,index2) in list_new_pos+[(ancient_pos[0],ancient_pos[1],(x-ancient_pos[0]+y-ancient_pos[1]),(abs(y-ancient_pos[1]))==1)] if access(k,l)[index2] != 0]) == 1 and (x,y) != START and (x,y) != END:
                new_val = 0
            elif list_new_pos[0][0] == ancient_pos[0] and list_new_pos[0][1] == ancient_pos[1]:
                new_val = 0
            else:
                epsilon = (random.random()-0.5)/10**2*0
                new_val = v + s*ddiv*(abs(v)+epsilon)/somme
        else:
            epsilon = (random.random()-0.5)/10**2*0
            new_val = v + s*ddiv*(1+epsilon)/len(list_new_pos)
        new_v = list(access(i,j))
        new_v[index] = new_val
        new_v = tuple(new_v)
        affect(i,j,new_v)
    #Correct self value organelle
    vx = (access(x+1,y)[0] + access(x-1,y)[0])/2
    vy = (access(x,y+1)[1] + access(x,y-1)[1])/2
    (pa,pb,pc,pd) = (is_obstacle(x+1,y),is_obstacle(x-1,y),is_obstacle(x,y+1),is_obstacle(x,y-1))
    nu1 = (pa+pb+pc+pd <= 1)
    svx = sg(vx)
    svy = sg(vy)
    if svx == 0:
        svx = random.randint(0,1)*2-1
        #On verifie que l'on ne va pas dans un mur
        if is_obstacle(x+svx,y):
            svx = -svx
    if svy == 0:
        svy = random.randint(0,1)*2-1
        #On verifie que l'on ne va pas dans un mur
        if is_obstacle(x,y+svy):
            svy = -svy
    epsilon = random.random()
    deviation = nu1*((-g*vy>=0)*vy*epsilon + (-h*vy>=0)*vy*epsilon - (-a*vx>=0)*vx*(1-epsilon) - (-b*vx>=0)*vx*(1-epsilon))
    vx += deviation*svx*svy
    vy -= deviation*svy*svx
    eta = (pa*pc+pa*pd+pb*pc+pb*pd == 1)
    corry = eta*((vy>0 and pc==1)+(vy<0 and pd==1))*abs(vx)
    corrx = eta*((vx>0 and pa==1)+(vx<0 and pb==1))*abs(vy)
    vx += -corrx*svx+corry*svx
    vy += -corry*svy+corrx*svy
    affect(x,y,(vx,vy))
    
def explore():
    global X,Y,APOS,N,NB_STEP,SCORE
    NB_STEP += 1
    if (X,Y) == APOS:
        assert False #Pb (X,Y) = APOS - shouldn't occur - if you see this error your maze may be incorrect
    if (X,Y) == END:
    	print("end")
        (X,Y) = START
        APOS = (0,1)
        SCORE.append(NB_STEP)
        NB_STEP = 0
    #Leaving standing water area
    l_remonte = [(X+a,Y+b) for a,b in move_list() if access(X+a,Y+b) != (0,0)]
    if l_remonte != []:
        remonte = l_remonte[0]
    else:
        remonte = None
        
    solve((X,Y),APOS)
    N += 1
    (vx,vy) = access(X,Y)
    svx = sg(vx)
    svy = sg(vy)
    if svx == 1:
        x_score = vx*access(X+svx,Y)[0]
    elif svx == -1:
        x_score = vx*access(X+svx,Y)[0]
    else:
        x_score = 0
    if svy == 1:
        y_score = vy*access(X,Y+svy)[1]
    elif svy == -1:
        y_score = vy*access(X,Y+svy)[1]
    else:
        y_score = 0
    if x_score == y_score and y_score == 0:
        list_new_pos = [(X+a,Y+b) for a,b in move_list()
                        if allowed_pos(X+a,Y+b)
                        and not(is_obstacle(X+a,Y+b))
                        and (X+a,Y+b) != APOS]
        if list_new_pos != []:
            if remonte == None:
                #assert False
                APOS = (X,Y)
                (X,Y) = random.choice(list_new_pos)
            else:
                APOS = (X,Y)
                (X,Y) = remonte
        else:
            newX = APOS[0]
            newY = APOS[1]
            APOS = (X,Y)
            (X,Y) = (newX,newY)
    elif x_score > y_score:
        APOS = (X,Y)
        X += svx
    else:
        APOS = (X,Y)
        Y += svy
    

#------------------------------
#
# * Graphical functions *
#
#------------------------------

fig = plt.figure(figsize=(27,27),dpi=50)
      
def show(V):
    plt.clf()
    X1 = [[j for j in range(len(V[i]))] for i in range(len(V))]
    Y1 = [[i for j in range(len(V[i]))] for i in range(len(V))]
    U1 = []
    V1 = []
    for b in range(len(V)):
        U1.append([])
        V1.append([])
        for a in V[b]:
            if a[0] != 0 or a[1] != 0:
                U1[b].append(float(a[0])/((float(a[0])**2+float(a[1])**2)**0.5))
                V1[b].append(float(a[1])/((float(a[0])**2+float(a[1])**2)**0.5))
            else:
                U1[b].append(0.)
                V1[b].append(0.)
    plt.quiver(X1,Y1,U1,V1,scale=50)
    #/!\ plot_blocks function is very long to compute. You can remove it if you want the animation to run faster
    def plot_blocks():
        for j in range(len(maze)):
            for i in range(len(maze[j])):
                if maze[j][i] != 0:
                    l1 = [i-0.5,i+0.5,i+0.5,i-0.5,i-0.5]
                    l2 = [j-0.5,j-0.5,j+0.5,j+0.5,j-0.5]
                    plt.plot(l1,l2,color="blue")
    #plot_blocks()
    
    plt.plot([X-0.5,X+0.5,X+0.5,X-0.5,X-0.5],[Y-0.5,Y-0.5,Y+0.5,Y+0.5,Y-0.5],color="red")
    #plt.show()

#------------------------------
#
# * Tests *
#
#------------------------------
def init():
    pass

SLOW = 0
SLOW_MAX = 0 #step_time = SLOW_MAX*50ms /!\ if the plot_blocks function is running it will slow the animation

def compute_and_show_step(useless):
    global V,X,Y,POS,APOS,END,SLOW,SLOW_MAX,NB_STEP
    if SLOW < SLOW_MAX:
        SLOW += 1
        return 0
    SLOW = 0
    explore()
    show(V)
    if (X,Y) == END:
        print("---ENDED---",NB_STEP+1,SCORE)
        
nb = 5000 #Number of steps in the maze


global anim
anim = animation.FuncAnimation(fig,compute_and_show_step,init_func=init,frames=nb,interval=50,repeat=False)

plt.show()

"""
#The code I used to generate graphics in the report
nb_ep = 200
nb_data = 50

RES = []
def resolve(nb_times):
    global N
    for j in range(nb_times):
        N = 0
        while (X,Y) != END:
            explore()
        explore()

for j in range(1,61):
    lab = load_lab(j)
    maze = close_maze(lab)
    for i in range(nb_data):
        print(j,i)
        SCORE = []
        resolve(nb_ep)
        RES.append(sum(SCORE))
        V = [[(0,0) for j in i] for i in maze]
        X = 1
        Y = 1
        APOS = (0,1)

print(RES)
"""
_file = open("data_pNS_maze1.result","w")
_file.write(str(RES))
_file.close()
