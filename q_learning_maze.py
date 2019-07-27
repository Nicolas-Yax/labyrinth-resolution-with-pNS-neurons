import sqlite3
import random
import matplotlib.pyplot as plt
from matplotlib import animation
import time

debug = False

def load_lab(index):
    conn = sqlite3.connect("lab.db")
    c = conn.cursor()
    c.execute("SELECT * FROM lab")
    lab = None
    for i in range(index):
        lab = eval(c.fetchone()[0])
    return lab
                
def close_maze(laby):
    for i in range(len(laby)):
        laby[i].append(1)
        laby[i].insert(0,1)
    laby.append([1 for i in range(len(laby[0]))])
    laby.insert(0,[1 for i in range(len(laby[0]))])
    return laby

lab = load_lab(1)
maze = close_maze(lab)
memory = [[0 for j in i] for i in maze]

lambda_factor = 0.3
gamma_factor = 0.92

p_explore = 0.1

IN = (1,1)
END = (25,25)

def allowed_pos(pos):
    (x,y) = pos
    xcond = x>=0 and x<len(memory[0])
    ycond = y>=0 and y<len(memory)
    return xcond and ycond

def all_move():
    return [(1,0),(-1,0),(0,1),(0,-1)]

def near(pos):
    (x,y) = pos
    l = [(x+a,y+b) for a,b in all_move() if allowed_pos((x+a,y+b)) and maze[y+b][x+a] == 0]
    return l

def get_reward(pos):
    if pos == END:
        return 1
    else:
        return -0.0001

    
def learn(pos):
    (x,y) = pos
    near_reward = max([memory[p[1]][p[0]] for p in near(pos)])
    memory[y][x] += lambda_factor*(get_reward(pos) + gamma_factor*near_reward - memory[y][x])

def get_explore_exploit(pos):
    near_pos = near(pos)
    maxi_reward = -10**5
    maxi_case = None
    for p in near_pos:
        r = memory[p[1]][p[0]]
        if r >= maxi_reward:
            maxi_reward = r
            maxi_case = p
    assert maxi_case != None
    near_pos.remove(maxi_case)
    return near_pos,[maxi_case]

def step(pos,last_pos):
    (x,y) = pos
    explore,exploit = get_explore_exploit(pos)
    r = random.random()
    if debug:
        print("step",r,p_explore,last_pos,exploit[0],explore)
    if (r < p_explore and explore != []):
        if debug:
            print("explore")
        if last_pos in explore and len(explore)>=2:
            explore.remove(last_pos)
        i = random.randint(0,len(explore)-1)
        next_pos = explore[i]
    else:
        if debug:
            print("exploit")
        next_pos = exploit[0]
    learn(next_pos)
    return next_pos,pos
"""
fig = plt.figure(figsize=(27,27),dpi=50)
color_map = plt.imshow(memory,cmap="inferno",vmin=-1,vmax=1)
"""
def solve(pos,last_pos=(-1,-1)):
    compt = 0
    while pos != END:
        compt += 1
        pos,last_pos = step(pos,last_pos)
    return compt

#nb = 500

POS = IN
LAST_POS = (-1,-1)
COMPT = 0
"""
def show():
    (x,y) = POS
    plt.clf()
    plt.imshow(memory,cmap="inferno",vmin=-1,vmax=1)
    #color_map.set_data(memory)
    #plt.plot([x-0.5,x-0.5,x+0.5,x+0.5,x-0.5],[y-0.5,y+0.5,y+0.5,y-0.5,y-0.5],color="red")
"""
def init():
    pass

def compute_and_show(useless):
    global POS,COMPT,LAST_POS
    show()
    if POS != END:
        COMPT += 1
        POS,LAST_POS = step(POS,LAST_POS)

nb_data = 150   
nb_ep = 200
SCORE = [[0]*nb_ep for i in range(nb_data)]
NB_DATA = 0
def compute(useless):
    global p_explore,NB_DATA,SCORE
    p_explore = 1/(useless**0.25+10) + 0.01
    score = solve(IN)
    #print(useless,score)
    SCORE[NB_DATA][i] += score
    #show()
    
_file = open("data_ql_maze1.result","w")
_file.write("")
_file.close()
"""
for i in range(nb_data):
    plt.plot([j for j in range(nb_ep)],SCORE[i],alpha=0.1,color="lightblue")
"""

for j in range(nb_data):
    print("-----------SAMPLE"+str(j)+"--------------")
    lab = load_lab(3)
    maze = close_maze(lab)
    memory = [[0 for j in i] for i in maze]
    for i in range(nb_ep):
        compute(i)
    NB_DATA += 1
for i in range(nb_data):
    plt.plot([j for j in range(nb_ep)],SCORE[i],alpha=0.01,color="lightblue")
_file = open("data_ql_maze1.result","w")
_file.write(str(SCORE))
_file.close()
plt.show()


