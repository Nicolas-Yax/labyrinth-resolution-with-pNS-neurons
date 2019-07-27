import random

#------------------------------------
#
#             pNS-Neuron
#
#------------------------------------
#To implement the pNS-Neuronn, I've chosen to use the same form than the one in the paper so
#that organelles will have the same shape, same arguments, same formulas. However usually it is
#not a good idea to put too many arguments in a function. That's why the first line each 
#function representing an organelle will be used to get the other arguments.


class pNS_Neuron:
    #Values
    vx = 0
    vy = 0
    wall = 0
    active = False
    #Neighbours
    a = None #(x+1,y)
    b = None #(x-1,y)
    c = None #(x,y+1)
    d = None #(x,y-1)
    #Learning rate
    lambda_factor = 0.1
    #------------------------------------
    #
    #             ORGANELLES
    #
    #------------------------------------
    def learn_active(self,value,active):
        #Update the active parameter
        if value != None:
            self.active = value
        if active != None:
            self.active = active

    def learn_wall(self,wall):
        self.wall = wall
        if wall:
            (self.vx,self.vy) = (0,0)

    def correct_self_div(self,s,ddiv,somme,target):
        #Get data
        (avx,avy,nb_walls) = (self.vx,self.vy,a.wall+b.wall+c.wall+d.wall)
        #Correct vx and vy according to the message received
        if not(self.wall):
            if somme == 0:
                if target == "vx":
                    self.vx += s*ddiv/nb_walls
                else:
                    self.vy += s*ddiv/nb_walls
            else:
                if target == "vx":
                    self.vx += s*ddiv*avx/somme
                else:
                    self.vy += s*ddiv*avy/somme

    def correct_other_div(self,div,active):
        (a,b,c,d) = (self.a.vx,self.b.vx,self.c.vy,self.d.vy)
        #Compute constants
        somme = 0
        if active != 1:
            somme += abs(a)
        if active != 2:
            somme += abs(b)
        if active != 3:
            somme += abs(c)
        if active != 4:
            somme += abs(d)
        ddiv = float(div - (a-b+c-d)
        #Send messages
        self.a.correct_self_div(1,ddiv,somme,"vx")
        self.b.correct_self_div(-1,ddiv,somme,"vx")
        self.c.correct_self_div(1,ddiv,somme,"vy")
        self.d.correct_self_div(-1,ddiv,somme,"vy")

    def correct_self_value(self,mu,vxlearn,vylearn,avx,bvx,cvy,dvy):
        #Compute constants
        cy = (-dvy*self.vy>=0) + (-cvy*self.vy>=0)
        cx = (-avx*self.vy>=0) + (-bvx*self.vx>=0)
        dev = mu*sv(self.vx)*sv(self.vy)*(cy*abs(self.vy/2) - cx*abs(self.vx/2))
        #Correct self value
        self.vx += (self.a.vx+self.b.vx)/2 + self.lambda_factor*vxlearn + dev
        self.vy += (self.c.vy+self.d.vy)/2 + self.lambda_factor*vylearn - dev
        #Send messages
        a.active = False
        b.active = False
        c.active = False
        d.active = False

    #------------------------------------
    #
    #     COMPUTATION OF ORGANELLES
    #
    #------------------------------------

    def compute(self,div,walla,wallb,wallc,walld,vxlearn,vylearn):
        (avx,bvx,cvy,dvy) = (self.a.vx,self.b.vx,self.c.vy,self.d.vy)
        #First circuit
        self.learn_active(True)
        self.a.learn_wall(walla)
        self.b.learn_wall(wallb)
        self.c.learn_wall(wallc)
        self.d.learn_wall(walld)
        self.correct_other_div(div)
        #Second circuit
        mu = (self.a.wall + self.b.wall + self.c.wall + self.d.wall <=1)
        self.correct_self_value(mu,vxlearn,vylearn,avx,bvx,cvy,dvy)

class pNS_Network():
    
    network = None
    
    def __init__(self,sizex,sizey):
        self.sizex = sizex
        self.sizey = sizey
        #Creation of neurons
        self.network = [[pNS_Neuron() for j in range(sizex)] for i in range(sizey)]
        #Connect neurons
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                if self.correct_pos(i,j+1):
                    self.network[i][j].a = self.network[i][j+1]
                if self.correct_pos(i,j-1):
                    self.network[i][j].b = self.network[i][j-1]
                if self.correct_pos(i+1,j):
                    self.network[i][j].c = self.network[i+1][j]
                if self.correct_pos(i-1,j):
                    self.network[i][j].d = self.network[i-1][j]

    def correct_pos(self,x,y):
        #Returns True if the position is in the array
        xcond = x>=0 and x<self.sizex
        ycond = y>=0 and y<self.sizey
        return xcond and ycond

    def computable_neuron(self,x,y):
        #Returns True if the position is in the array and not close to the border
        xcond = x>=1 and x<self.sizex-1
        ycond = y>=1 and y<self.sizey-1
        return xcond and ycond

    def learn(self,x,y,div,walls,learnx,learny):
        #Compute the neuron at this position
        #NOTE : Don't call learn on a wall
        if self.computable_neuron(x,y):
            self.network[y][x].compute(div,walls[0],walls[1],walls[2],walls[3],learnx,learny)
        else:
            print("ERROR : Wrong position x,y in learn(x,y,learnx,learny)")

    def get(self,x,y):
        #Get the speed vector at the asked position
        n = self.network[y][x]
        return (n.vx,n.vy)

    def is_wall(self,x,y):
        #Return True if the neuron at this position thinks it is a wall
        return self.network[y][x].wall == 1
            

def sv(x):
    #The sv function from the paper
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return random.randint(0,1)*2-1

net = pNS_Network(25,25)
net.learn(1,1,1,[0,1,0,1],0,0)
net.learn(1,2,0,[1,1,0,0],0,0)
print(net.get(1,1))
print(net.get(2,1))
print(net.get(1,2))
print(net.get(1,3))
print(net.get(3,1))
