"""
Author: Jordan Yuan
"""
class State:  # State class represents a tile's current state
	def __init__(self, nparray, depth=0, path=""):
		self.coordinates = nparray  # coordinates for current state
		self.depth = depth  # path length, or g(n)
		self.path = path 	# path from root
		self.h = self.h_distance(self.coordinates) # h(n)
		self.f = self.depth + self.h # f(n)

	def incre_0(self):  # increse latitude 0 and 180 and return a new state
		c = self.coordinates.copy()
		c[c[:, 1] == 0, 0] += 30
		c[c[:, 1] == 180, 0] -= 30
		c[np.where((c[:,0] == 180) & (c[:,1] == 0))] = [180,180]
		c[np.where((c[:,0] == 0) & (c[:,1] == 180))] = [0,0]
		rotation = "incre_0 "
		return State(c, self.depth+1, self.path + rotation)

	def decre_0(self):  # decrese latitude 0 and 180 and return a new state
		c = self.coordinates.copy()
		c[c[:, 1] == 0, 0] -= 30
		c[c[:, 1] == 180, 0] += 30
		c[np.where((c[:,0] == -30) & (c[:,1] == 0))] = [30,180]
		c[np.where((c[:,0] == 210) & (c[:,1] == 180))] = [150,0]
		rotation = "decre_0 "
		return State(c, self.depth+1, self.path + rotation)

	def incre_90(self):  # increse latitude 90 and 270 and return a new state
		c = self.coordinates.copy()
		c[c[:, 1] == 90, 0] += 30
		c[c[:, 1] == 270, 0] -= 30
		c[np.where((c[:,0] == 0) & (c[:,1] == 0))] = [30,90]
		c[np.where((c[:,0] == 180) & (c[:,1] == 180))] = [150,270]
		c[np.where((c[:,0] == 180) & (c[:,1] == 90))] = [180,180]
		c[np.where((c[:,0] == 0) & (c[:,1] == 270))] = [0,0]
		rotation = "incre_90 "
		return State(c, self.depth+1, self.path + rotation)

	def decre_90(self):  # decrese latitude 90 and 270 and return a new state
		c = self.coordinates.copy()
		c[c[:, 1] == 90, 0] -= 30
		c[c[:, 1] == 270, 0] += 30
		c[np.where((c[:,0] == 0) & (c[:,1] == 0))] = [30,270]
		c[np.where((c[:,0] == 180) & (c[:,1] == 180))] = [150,90]
		c[np.where((c[:,0] == 0) & (c[:,1] == 90))] = [0,0]
		c[np.where((c[:,0] == 180) & (c[:,1] == 270))] = [180,180]
		rotation = "decre_90 "
		return State(c, self.depth+1, self.path + rotation)

	def incre_eq(self):  # increse equator and return a new state
		c = self.coordinates.copy()
		c[c[:, 0] == 90, 1] += 30
		c[np.where((c[:,0] == 90) & (c[:,1] == 360))] = [90,0]
		rotation = "incre_eq "
		return State(c, self.depth+1, self.path + rotation)

	def decre_eq(self):  # decrese equator and return a new state
		c = self.coordinates.copy()
		c[c[:, 0] == 90, 1] -= 30
		c[np.where((c[:,0] == 90) & (c[:,1] == -30))] = [90,330]
		rotation = "decre_eq "
		return State(c, self.depth+1, self.path + rotation)		

	def expand(self): # get all children for current state
		return (self.incre_0(), self.decre_0(), self.incre_90(), self.decre_90(), self.incre_eq(), self.decre_eq())

	def h_distance(self,c):  # computer h(n) 

		# d1 is the Manhattan distance for north pole (0, 0)
		# d2 is the Manhattan distrance for south pole (180, 180)
		d1 = c[0][0]/30 if c[0][1] in [0, 90, 180, 370] else 4
		d2 = (180-c[1][0])/30 if c[1][1] in [0, 90, 180, 370] else 4

		# d3 is the Manhattan distance for (90, 0) 
		if (c[10][0] == 90):
			d3 = 6 - abs(c[10][1]-180)/30
		elif (c[10][1] in [90, 270]):
			d3 = 4
		elif c[10][1] == 0:
			d3 = abs(c[10][0]-90)/30
		else:
			d3 = 6 - abs(c[10][0]-90)/30

		# d5 is the Manhattan distance for (90, 180) 
		if (c[11][0] == 90):
			d5 = abs(c[11][1]-180)/30
		elif (c[11][1] in [90, 270]):
			d5 = 4
		elif c[11][1] == 0:
			d5 = 6 - abs(c[11][0]-90)/30
		else:
			d5 = abs(c[11][0]-90)/30

		# d4 is the Manhattan distance for (90, 90) 
		if (c[12][0] == 90):
			d4 = abs(c[12][0]-90)/30 if c[12][1] <= 180 else (6 - abs(c[12][0]-270)/30)
		elif (c[12] == [0, 0]).all() or (c[12] == [180,180]).all():
			d4 = 3
		elif (c[12][1] in [0, 180]):
			d4 = 4
		elif c[12][1] == 90:
			d4 = abs(c[12][0]-90)/30
		else:
			d4 = 6 - abs(c[12][0]-90)/30

		# if (c[13][0] == 90):
		# 	d6 = abs(c[13][0]-270)/30 if c[13][1] > 180 else (6 - abs(c[13][0]-90)/30) 
		# elif (c[13] == [0, 0]).all() or (c[13] == [180,180]).all():
		# 	d6 = 3
		# elif (c[13][1] in [0, 180]):
		# 	d6 = 4
		# elif c[13][1] == 90:
		# 	d6 = 6 - abs(c[13][0]-90)/30
		# else:
		# 	d6 = abs(c[13][0]-90)/30
		return (d1 + d2 + d3 + d4 + d5) / 4

	def __lt__(self, other):  # custom comparison for State object
		return self.f  < other.f if self.f != other.f else self.h < other.h

def readData(fileName): # read data and return as np array
	current, target = [], []
	f = open(fileName, 'r')
	for line in f.readlines()[1:-1]:
		current.append(re.findall(r'\d+', line.split()[1]))
		target.append(re.findall(r'\d+', line.split()[2]))
	return (np.array(current).astype(int), np.array(target).astype(int))

def BFS(root, target):
	timeout = time.time() + 7200 # 2h limit, break the loop
	visited, queue = set(), [root]
	while queue:
		currentNode = queue.pop(0)
		if time.time() > timeout: # 2h, break the loop
			currentNode.path = "Maxinum time 2h limit reached. This is how far I got"
			break
		if np.array_equal(currentNode.coordinates, target): # found the goal
			break
		else:
			visited.add(hash(currentNode.coordinates.tostring())) 
			expandNodes = currentNode.expand()
			for node in expandNodes:
				if hash(node.coordinates.tostring()) not in visited:
					queue.append(node)
			if len(queue) % 1000000 in range(7): # do garbage collection regularly
				x = gc.collect()
				print("Garbage collection: ", x)
	return (len(visited), len(queue)+1, currentNode)

def aStar(root, target):
	timeout = time.time() + 7200 # 2h limit, break the loop
	visited, queue = set(), [root]
	heapq.heapify(queue)
	while queue:
		currentNode = heapq.heappop(queue)
		if time.time() > timeout: # 2h, break the loop
			currentNode.path = "Maxinum time 2h limit reached. This is how far I got"
			break
		if np.array_equal(currentNode.coordinates, target):
			break
		else:
			visited.add(hash(currentNode.coordinates.tostring())) 
			expandNodes = currentNode.expand()
			for node in expandNodes:
				if hash(node.coordinates.tostring()) not in visited:
					heapq.heappush(queue, node)
			if len(queue) % 1000000 in range(7): # do garbage collection regularly
				print("Garbage collection: ", gc.collect())
	return (len(visited), len(queue)+1, currentNode)


def RBFS(node, target, limit):
	timeout = time.time() + 7200 # 2h limit, break the loop
	num_expanded = [0]
	goal, _ = _RBFS(node, target, limit, num_expanded, timeout)
	return (num_expanded[0], goal.depth*5, goal)

def _RBFS(node, target, limit, num_expanded, timeout):
	num_expanded[0] += 1
	if time.time()> timeout:
		node.path = "Maxinum time 2h limit reached. This is how far I got"
		return node, 0
	if np.array_equal(node.coordinates, target):
		return node, 0
	successors = []
	for each in node.expand():
		each.f = max(each.f, node.f)
		successors.append(each)
	while True:
		successors = sorted(successors)
		best = successors[0]
		if best.f > limit:
			return False, best.f
		alternative = successors[1].f
		result, best.f = _RBFS(best, target, min(limit, alternative), num_expanded, timeout)
		if result:
			return result, 0

def main(ALG, FILE):
	print("Note: incre_0  means increse ring(0, 180)")
	print("      decre_0  means decrese ring(0, 180)")
	print("      incre_90 means increse ring(90, 270)")
	print("      decre_90 means decrese ring(90, 270)")
	print("      incre_eq means increse the equator")
	print("      decre_eq means decrese the equator")
	
	current, target = readData(FILE)
	root = State(current)
	start = time.time()
	if ALG == "BFS":
		num_expanded, max_queue, goal = BFS(root, target)
	elif ALG == "AStar":
		num_expanded, max_queue, goal = aStar(root, target)
	else:
		num_expanded, max_queue, goal = RBFS(root, target, math.inf)
	end = time.time()

	print("The number of states expanded: ", num_expanded)
	print("The maximum size of the queue: ", max_queue)
	print("The final path length: ", goal.depth)
	print("The final path: ", goal.path)
	print("Time taken: ", end - start)

if __name__ == '__main__':
	import re, math, time, heapq, sys, gc
	import numpy as np

	_ , ALG, FILE = sys.argv
	assert ALG in ["BFS", "AStar", "RBFS"], "Check your command line arguments"
	
	main(ALG, FILE)
	
