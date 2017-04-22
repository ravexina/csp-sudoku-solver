#!/usr/bin/python3

# Author: ravexina (Milad As) 
# https://github.com/ravexina

# Repo on github
# https://github.com/ravexina/csp-sudoku-solver


# ----------------------------------------------------------------------------

# MIT License

# Copyright (c) 2017 ravexina (Milad As)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ----------------------------------------------------------------------------

import tkinter as tk
import random
import sys
import os
import time
import timeit

# Start tkinter, we need it for StringVar()
# Create base window
root = tk.Tk()

class solver:
	
	def __init__(self):
		# init some empty matrix
		
		# will be mapped to entries
		self.matrixa = [[1 for x in range(10)] for y in range(10)]
		
		# contains domain [1,1] = [-1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
		self.matrix_domains = [[1 for x in range(10)] for y in range(10)]
		
		# to keep track of primary state
		self.matrix_lock = [[1 for x in range(10)] for y in range(10)]
		
		# to keep track of entries - change thier attr if we need
		self.entryList = [[1 for x in range(10)] for y in range(10)]
		
		# default is to find entries with min domain
		self.rvt = 'min' # Min remained value / Max ...
		
		# fill with what
		self.fill_with = 'min' # Min effect on other domains / Random
		
		self.entry_stack = [] # solution stack (backtracking)
		self.stack_save = [] # usage: to save the solution
		self.backtrack_times = 1
		self.notbf = 0 # don't allways choose the best one
		

	# Put lables
	# Create entreis
	# Map matrixa to entries
	def new(self):
                # clear stack to ensure nothing is in there (after serveral run)
		self.entry_stack = []
		self.backtrack_times = 1
		
		# vertical labels are not set yet :)
		label_flag = 0
		
		for i in range(0, 10):
			# if column is one and vertical labels are not set yet then set them
			if i == 1 and label_flag == 0:
				for z in range(1,10):
					tk.Label(table, text=z).grid(row = z, column = 0)
				label_flag = 1
		
			# Create entries
			for j in range(1, 10):
				# Start with creating horizontal labels (first time - i = 0)
				if i == 0:
					tk.Label(table, text=j).grid(row = 0, column = j)
				# when i > 0 then create lables
				else:	
					# init matrixa to map it into tkinter entries
					self.matrixa[i][j] = tk.StringVar()
					# add corespondent entary
					self.entryList[i][j] = tk.Entry(table, width=4, justify='center', textvariable=self.matrixa[i][j])
					self.entryList[i][j].grid(row = i, column = j)
		self.colorize();
		
	# create a copy of solution to use with next
	def save(self):
		for i in range(1,10):
			for j in range(1,10):
				# clear this entry if it's not pre defined
				if self.matrix_lock[i][j] != 1:
					self.matrixa[i][j].set('')
		
		self.stack_save = self.entry_stack
		self.stack_save.reverse() # when poping we start from beginning
		print(colors.fail, "Saved in memory.", colors.endc);
	   
	def notb(self):
		if self.notbf == 0:
			self.notbf = 1
			print(colors.warning,"Don't always choose the best one", colors.endc)
		else:
			self.notbf = 0
			print(colors.green,"Always choose the best one", colors.endc)

	def h1(self):
		self.rvt = 'min' 
		self.fill_with = 'min' # random/min
		print(colors.header,"Select an entry with:", colors.endc , colors.green, " min remained value", colors.endc)
		print(colors.header,"Select an value for entry:", colors.endc, colors.blue, " with min effect on other domains", colors.endc)

	def h2(self):
		self.rvt = 'min'
		self.fill_with = 'random' # random/min
		print(colors.header,"Select an entry with:", colors.endc , colors.green, " min remained value", colors.endc)
		print(colors.header,"Select an value for entry:", colors.endc, colors.blue, " random", colors.endc)
	
	def next(self):
		# if table was full
		if self.stack_save == []:
                    print(colors.warning, "It's done :)", colors.endc);
		else:
			# pop an item from stack copy
			e = self.stack_save.pop()
			# retrive its value
			self.matrixa[e[0]][e[1]].set(e[2])
	# search and replace (fill)
	def sr(self):
		nextEntry = self.nextEntry()
		x = nextEntry[0]
		y = nextEntry[1]
		val = self.withWhat(x, y)
		self.matrixa[x][y].set(val)
		
		# add the value to the stack
		tmp = self.entry_stack.pop()
		self.entry_stack.append([x, y, val])
		
		# cal domains for effecteds entries
		self.calDomains(self.row(x,y), self.col(x,y), self.box(x,y));
	
	def nextLive(self):
		if self.checkDone() == 1:
			print("--- DONE ---")
		else:
			self.sr(); # search and fill
				
	def search(self):
		#self.out('search will started in 1 sec...')
		#self.out('entry stack: ', self.entry_stack)
		#time.sleep(1)
		start = timeit.default_timer()
		while 1:	
			self.sr(); # search and fill
			if self.checkDone() == 1:
				print("--- DONE ---")
				break;
			#os.system("sleep 0.0005")
			#time.sleep(0.025)
			
		stop = timeit.default_timer()
		timeLabel['text'] = str( round(stop - start, 2) ) + " SEC" 
		print("in: ", stop - start, "sec.")		

	def finalize(self):

		self.setPrimaryState()

		self.calDomains()
		
		os.system('cls' if os.name == 'nt' else 'clear')

	def checkDone(self):
		for i in range(1, 10):
			for j in range(1, 10):
				if not self.matrixa[i][j].get().isdigit() :
					return 0
		
		return 1
					 
	# ----------------------------------------------------------------------
	# Domains And Matrixs
	# ----------------------------------------------------------------------

	# select and returns an entriy with requested huristic to fill next
	# self.rvt: max/min 
	def nextEntry(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		self.out("start looking for a domain with ", self.rvt, " value.")
	
		# create a list of all entries without value and their domain count
		lst = []
		for i in range(1, 10):
			for j in range(1, 10):
				# add it if this entry does not have a value
				# to prevent proposing an entry with a value
				if not self.matrixa[i][j].get().isdigit() :
					domain = int(self.matrix_domains[i][j][0]);
					lst.append([i, j, domain ]) # [ [x,y, domainCount], ... ]
	
		# create a list of domain values form entries without value
		nlst = [] # [1, 2, ...]
		for i in lst:
			nlst.append(i[2])
		
		# remove duplicate numbers
		nlst = self.rmDup(nlst);
		# remove zero [to backtrack]
		if nlst.count(0) > 0:
			nlst.remove(0);

		self.out("Select from this domains:", nlst);
		
		# there is no domain to select a min/max from them		
		if nlst == []:
			self.out("All domains are taken.")
			# start backtracking
			self.backtrack()
			return self.nextEntry()
		else:
			# select min or max depend on h1/h2
			if self.rvt == 'min':
				# find the min
				val = min(nlst)
				#print("max: ", val)
			else:
				#find the max
				val = max(nlst)
				#print("max: ", val)

			# some log
			self.out("Selected domain: ", val)
		
			# create a list of all entries with the same selected domain (value)
			nlst = []
			for i in lst:
				if val == i[2]:
					nlst.append([i[0], i[1]])
				
			# select a random index and return it
			choice = random.choice(nlst)

			self.out("Choiced entry: ", choice)
			# print the choiced entry domain :)
			self.out("With the domain of: ", self.matrix_domains[choice[0]] [choice[1]])
		
			# add selected entry to entry_stack for backtracking purpose
			self.entry_stack.append(choice)
		
			# print entries stack
			self.out("\nEntry Stack: ", self.entry_stack, "\n")
		
			return choice

	# returns the best value to fill an entry
	def withWhat(self, x, y):
		# get available values in this entry domain
		lst = self.availVals(x,y)
		
		self.out("Available values for this entry are:", lst)
		self.out("Select form is: ", self.fill_with) 
		
		# based on h1/h2 return a value of choice
		if self.fill_with == 'random':
			choice = random.choice(lst);
		elif self.fill_with == 'min':

			# get a list of entries that will be effected by this value
			elst = self.row(x,y) + self.col(x,y) + self.box(x,y)
			elst.remove([x, y]) # remove the entry itself
			self.out("\nEntries that will be effected by this entry:", elst)
			# keep only empty entries
			elst = self.onlyEmpty(elst)
			self.out("\nThe empty ones:", elst)
			
			# Sum of all entries that will be effected [before any change]
			sum_d = 0
			for e in elst:
				sum_d += self.domainCount(e[0], e[1]) 
			self.out("\nSum of available value in all these entries domains:", sum_d)
			
			# keep a copy to reset after calculation
			domains_copy = self.matrix_domains
			matrixa_copy = self.matrixa
			
			# select a value which does less effect on other entries domains
			# if 1 make domains sum 20, and 2 make them 40 so pick the 2 cuse
			# it's changes them lesser than of 1
			
			choice_domain_range = 0 # lets say the max change is zero

			# not always best one functionality lists
			if self.notbf == 1:
				d = [] # list of domains to chose one of the best (NOT THE BEST) 
				v_d = {} # dictionary of domains and the value which make that domain to choose the value
			
			# lst = available values for this (selected) entry
			# check each val, see which one effects less
			for i in lst:	
				# reset for calculation
				self.matrixa = matrixa_copy
				self.matrix_domains = domains_copy
					
				# set a test value (from available values for this entry)
				self.matrixa[x][y].set(i)
				
				# calculate domains after setting test value
				self.calDomains(elst)
				
				# count the available values in entries domain after setting test value
				sum_d = 0
				for e in elst:
					sum_d += self.domainCount(e[0], e[1])
				
				# if this value make domains wider so pick it for now
				if sum_d >= choice_domain_range:
					choice_domain_range = sum_d
					choice = i
					
					# create a list for not allways choose the best one functionality
					if self.notbf == 1:
						# dict of domain and the value that makes that domain
						v_d[sum_d] = choice
						d.append(sum_d) # only doamins, to sort, reverse and find a good domain
			
			# if not always the best flag is set
			if self.notbf == 1:
				self.out("Available values changes on domains are like: ", d);
				d = self.rmDup(d)
				d.sort() # [1,2,3,4]
				d.reverse() # [4,2,3,1]
				if len(d) >= 2:
					choice_domain_range = d[1] # 2 => 2th best domain
					self.out("The second best is (domain range): ", d[1]);
				else:
					choice_domain_range = d[0]
					self.out("I can only choose the best (domain range) right now and its: ", d[0]);
					
				choice = v_d[choice_domain_range] # v_d[2] = ? (the value makes domains sum:2)
					
			self.out("this whill change domains to: ",  choice_domain_range)
			#self.matrixa = matrixa_copy
		
		self.out("choice is: ", choice)
		return choice
		
	# gets a list of entries
	# returns only the empty ones
	def onlyEmpty(self, lst):
		nlst = []
		for e in lst:
			if self.matrixa[e[0]][e[1]].get() == '':
				nlst.append([ e[0],  e[1] ])
		return nlst
		
	# returns available values in a domain
	def availVals(self, x, y):
		# get entry domain
		domain = self.matrix_domains[x][y] # [-1, 1, 0, ..., 1]
		# create a list of available values in this domain
		lst = []
		for i in range(1,10):
			if domain[i] == 1:
				lst.append(i)
		return lst
				
	def backtrack(self):
		self.out("Backtracking ...")
		# NO IDEA :D
		# so lets remove some of the entries
		
		# incrase backtrack each time
		self.backtrack_times += 1
		#if self.backtrack_f == 10:
		#	self.backtrack_f = 1
		r = 5 * self.backtrack_times
		
		# if there is something in stack backtrack
		if r > len(self.entry_stack):		
			r = len(self.entry_stack);
			self.backtrack_times = 1
			
		for i in range(r):
			entry = self.entry_stack.pop();
			x = entry[0]
			y = entry[1]
			self.matrixa[x][y].set('');
			# calculate all effected entriies domain
			self.calDomains( self.row(x,y), self.col(x,y), self.box(x,y) ); 

	# calculate domain of AN ENTRY
	def calDomain(self, x, y):
		# get all values that efects this entry point domain
		entries = self.row(x,y) + self.col(x,y) + self.box(x,y)
		entries.remove([x, y]) # remove itself from entries
		vals = self.getVals(entries) 

		# reset domain
		self.matrix_domains[x][y] = [-1,1,1,1,1,1,1,1,1,1]
		
		# then turn off the bits that are in conflict right now
		for i in vals:
			self.matrix_domains[x][y][int(i)] = 0
		
		# set number of on bits in this domain
		self.matrix_domains[x][y][0] = self.domainCount(x, y)
		
		# show the domain TST
		# #print(self.matrix_domains[x][y])

	# calculate domain of a LIST OF ENTRIES
	def calDomains(self, *args):
		listOfEntries = []  # to clac domain for
		# if we have a list only calc for these entries
		if len(args) > 0:
			# create a list of lists
			for arg in args:
				listOfEntries += arg
		else:
		# if not calc for all entries
		# create a list of all matrixa enties
			for i in range(1,10):
				for j in range(1,10):
					listOfEntries.append([i, j])
					
		# calc domain for each entry
		for i in listOfEntries:
			self.calDomain(i[0], i[1])

	# return the number of on bits (1) within a entary domain
	# number of the remained values in a entries domain
	# [-1,1,1,1,1,1,1,1,0,1] : 8
	def domainCount(self, x, y):
		count = 0
		for i in self.matrix_domains[x][y]:
			if i == 1:
				count += 1
		return count
	
	# create a list of primary state numbers
	# so we won't change them in backtraking
	def setPrimaryState(self):
		for i in range(1, 10):
			for j in range(1, 10):
				# entry has a value	
				if self.matrixa[i][j].get() != '' :
					# lock it - when saving (clearning) we skip this entry
					self.matrix_lock[i][j] = 1
					self.entryList[i][j]['fg'] = 'red'
					#self.entryList[i][j]['state'] = 'disabled'
				else:
					self.matrix_lock[i][j] = 0

	# ----------------------------------------------------------------------
	# Row and values
	# ----------------------------------------------------------------------
		
	# create a list of values form selected entries
	# entries should be specified as a list of lists
	# [ [1,2], [2,5], [4,8], ... ] will return the value of 1,2 etc. 
	def getVals(self, *args):
		# combine the lists of entaries passed as an argument
		# example retVals(row(), col())
		# combine the row and cols [[1,2] ... [1,3]]
		listOfEntries = []
		for arg in args:
			listOfEntries += arg

		# remove duplicate entaries
		listOfEntries = self.rmDup(listOfEntries)
		
		# crate a list of values
		lst = []
		for i in listOfEntries:
			# dont add empty valeues
			if self.matrixa[i[0]][i[1]].get() != '':
				lst.append( self.matrixa[i[0]][i[1]].get() ) # add the value of matrixa[1][3]
		return lst

	# return a list of all entry points in a same row
	def row(self, x, y):
		lst = []
		for i in range(1,10):
			# skip selected entry
			if i != y:
				lst.append([x, i])
		return lst

	# return a list of all entry points in a same column
	def col(self, x, y):
		lst = []
		for i in range(1,10):
			# skip selected entry
			if i != x:
				lst.append([i, y])
		return lst
	
	# return a list of all entries in a same box as matrixa[x][y]
	def box(self, x, y):
		# point the center :)
		if x == 3 or x == 6 or x == 9:
			x = x-1;
		if x == 1 or x == 4 or x == 7:
			x = x+1;
		if y == 1 or y == 4 or y == 7:
			y = y+1;
		if y == 3 or y == 6 or y == 9:
			y = y-1;
		
		# each two are an entry point
		lst = [	[x-1, y-1], 
			[x-1, y],
			[x-1, y+1],
			[x, y-1],
			[x, y],
			[x, y+1],
			[x+1, y-1],
			[x+1, y],
			[x+1, y+1]
		      ]
		return lst

	# ----------------------------------------------------------------------
	# --- HELPERS --- #	
	# ----------------------------------------------------------------------

	# remove duplicate items from a list
	def rmDup(self, lst):
		# create a new list
		nlist = []
	
		for i in lst:
			if i not in nlist:
				nlist.append(i)
		return nlist
		
	def out(self, *args):
		if len(sys.argv) > 1 :
			if sys.argv[1] == '-v':
				text = ''
				for arg in args:
					text += str(arg)
				
				print(text)
	def colorize(self):
		lst = [ [2,2], [2,4], [2,8],
			[5,2], [5,4], [5,8],
			[8,2], [8,4], [8,8] 
		]
		color = '#e5e5e5'
		for e in lst:
			nlst = self.box(e[0], e[1])
			for i in nlst:
				self.entryList[i[0]][i[1]]['bg'] = color
		    
			if color == '#e5e5e5' :
				color = '#c9c9c9'
			else:
				color = '#e5e5e5';

class colors:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    
# init base class
solver = solver()
	
# ----------------------------------------------------------------------
# --- GUI --- #	
# ----------------------------------------------------------------------

# table frame
table = tk.Frame(root, width=350, height=200)
table.grid(row = 1, column = 0, sticky="w")

# seperator
tk.Frame(root, height=200, width=10).grid(row = 1, column = 1)

# left buttons (#start, search)
buttons = tk.Frame(root, height=200, width=140)
buttons.grid(row = 1, column = 2,  sticky="e")

# seperator
tk.Frame(root, height=10, width=350).grid(row = 2, column = 0)

# down buttons (#next)
dbuttons = tk.Frame(root, height=50, width=350)
dbuttons.grid(row = 3, column = 0)

# Create menu objoect and add it to root
menubar = tk.Menu(root)

# Create a cascade file menu 
filemenu = tk.Menu(menubar, tearoff=0)

filemenu.add_command(label="New",  command=solver.new)
filemenu.add_command(label="Save", command=solver.save)
filemenu.add_command(label="NaTb", command=solver.notb)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

# Add the cascade file menu to menu bar object
menubar.add_cascade(label="File", menu=filemenu)

# Add two more independet item to menubar
menubar.add_command(label="First way", command=solver.h1)
menubar.add_command(label="Second way", command=solver.h2)


# Display Menu (menubar as menu)
root.config(menu=menubar)

# deny resize 
root.resizable(0,0)
table.pack_propagate(0)
#buttons.pack_propagate(0)
#dbuttons.pack_propagate(0)

# set root geometry
root.geometry("500x275")

# buttons
tk.Button(buttons, width=12, text='Create start state', command = solver.finalize).pack()
tk.Button(buttons, width=12, text='Start searching', command = solver.search).pack()
tk.Button(dbuttons, width=12, text='Next', command = solver.next).pack()
tk.Button(dbuttons, width=12, text='Next Live', command = solver.nextLive).pack()
timeLabel = tk.Label(buttons, width=12, text='00')
timeLabel.pack()

root.title("Python CSP Sudoku Solver - by: ravexina (Milad As)");

tk.mainloop()

# --------------------------------------------