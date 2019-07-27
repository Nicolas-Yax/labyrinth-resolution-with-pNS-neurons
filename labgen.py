from termcolor import colored
import random
import sys
import time
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import animation
import collections

COUNT = 0

def labgen(height,width):
	tab = [[1 for i in range(height)] for j in range(width)]
        free_pos = {(2*i,2*j):(i+j) for i in range(height//2) for j in range(width//2)}
	path = {}
	_in = (2,2)
	origin = (-1,-1)
	global origin,path
	def access(pos):
		(x,y) = pos
		#print(x,y)
		return tab[y][x]
	def modify(pos,val):
                if val == 0:
                        (x,y) = pos
                        l = [(x+i,y+j) for i in range(-1,2) for j in range(-1,2) if x+i>=0 and x+i<width and y+j>=0 and y+j<height]
                        for x,y in l:
                                try:
                                        del free_pos[(x,y)]
                                except:
                                        pass
		(x,y) = pos
		tab[y][x] = val
	def possible_moves(pos):
		(x,y) = pos
		moves = []
		pas = 2
		if x-pas>=0:
			moves.append(3)
		if y-pas>=0:
			moves.append(4)
		if x+pas<width:
			moves.append(5)
		if y+pas<height:
			moves.append(6)
		#print(moves,x,y)
		return moves
	def apply_move(pos,move):
		pas = 1
		if move == 3:
			return (pos[0]-pas,pos[1])
		elif move == 4:
			return (pos[0],pos[1]-pas)
		elif move == 5:
			return (pos[0]+pas,pos[1])
		elif move == 6:
			return (pos[0],pos[1]+pas)
		else:
			assert False #Not a move
	def print_tab():
		for i in tab:
			s = ""
			for j in i:
				if j == 0:
					s += colored(str(j),"white")
				elif j == 1:
					s += colored(str(j),"blue")
				elif j == 3:
					s += "<"
				elif j == 4:
					s += "^"
				elif j == 5:
					s += ">"
				elif j == 6:
					s += "v"
			print(s)
	def step(pos):
                #print("step")
		global origin,path,COUNT
		#print(pos)
		while True:
			#time.sleep(0.05)
			#print("---",access(pos),pos)
			#print_tab()
			#print(path)
			if access(pos) == 0:
				#Creates the path in the maze
				while True:
					if origin == pos:
						break
					#print(origin,access(origin))
					next = apply_move(origin,access(origin))
					modify(next,0)
					next = apply_move(next,access(origin))
					modify(origin,0)
					origin = next
                                        COUNT += 1
                                        if COUNT % 10000 == 0:
                                                print("COUNT",COUNT//10000)
				#Remove the rest
				for p in path:
					if access(p) != 0:
						modify(p,1)
                                                
				path = {}
				break
			else:
				moves = possible_moves(pos)
				move = random.choice(moves)
				modify(pos,move)
				path[pos] = 0
				next_pos = apply_move(apply_move(pos,move),move)
				pos = next_pos
	def get_next_start_pos():
                #print(len(free_pos.keys()))
                if free_pos != {}:
                        r = free_pos.keys()[0]
                        #print(free_pos.keys()[:50])
                        return r
                return (-1,-1)
                """
		for x in range(width):
			for y in range(height):
				l = [(x+i,y+j) for i in range(-1,2) for j in range(-1,2) if x+i>=0 and x+i<width and y+j>=0 and y+j<height and access((x+i,y+j)) != 1]
				if len(l) == 0:
					return (x,y)
		return (-1,-1)
                """
	modify(_in,0)
        
	while True:
		next_pos = get_next_start_pos()
		if next_pos == (-1,-1):
			break
		origin = next_pos
		step(next_pos)
	#print_tab()
	return tab

def gen(nb):
        width = 25
        height = 25
	conn = sqlite3.connect("labcroiss.db")
	c = conn.cursor()
	c.execute('''create table if not exists lab (laby text)''')
	for i in range(nb):
		print(i,width,height)
		c.execute("insert into lab values (?)",[(str(labgen(width,height)))])
                width += 5
                height += 5
	conn.commit()
	conn.close()
gen(60)
