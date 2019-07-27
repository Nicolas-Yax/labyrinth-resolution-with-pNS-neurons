import pNS_Net
import copy

class Maze:
    #Maze class to load a maze tab
    start = None
    end = None
    tab = None
    size = None
    pos = None

    def __init__(self,tab,start,end):
        #Loads the maze tab
        self.start = start
        self.end = end
        self.tab = copy.copy(tab)
        self.size = (len(tab[0]),len(tab))

    def initialize(self):
        #Put the actual position at the begining of the maze
        self.pos = self.start

    def move(self,direction):
        #The move function for directions
        (x,y) = self.pos
        if direction == "top":
            self.pos = (x,y+1)
        elif direction == "left":
            self.pos = (x-1,y)
        elif direction == "bottom":
            self.pos(x,y-1)
        else:
            self.pos(x+1,y)

    def set_pos(self,pos):
        #The move function for positions
        self.pos = pos

class Resolution:
    rna = None
    maze = None

    def __init__(self,maze):
        #Initialize the resolution
        self.rna = pNS_Net.pNS_Network(maze.size[0],maze.size[1])
        self.maze = maze

    def step(self):
        #Computes one step in the maze
        (x,y) = self.maze.pos
        (vx,vy) = self.rna.get(x,y)
        scorex = vx*self.rna.get(x+sgn(vx),y)
        scorey = vy*self.rna.get(x,y+sgn(y))
        if abs(scorex) > abs(scorey):
            if scorex > 0:
                self.maze.move("left")
            else:
                self.maze.move("right")
        else:
            if abs(scorex) == abs(scorey) and scorex == 0:
                valid_squares = [(x+a,y+b) for (a,b) in [(1,0),(-1,0),(0,1),(0,-1)] if not(self.rna.is_wall(x+a,y+b))]
                r_index = random.randint(0,len(valid_squares)-1)
                self.maze.set_pos(valid_squares[r_index])

    def solve(self):
        #Solve the entiere maze
        count = 0
        while maze.pos != maze.end:
            self.step()
            count += 1
        return count
