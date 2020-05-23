"""
Author: Jordan Yuan
   This is the class representation of the NQueen problem. 
   This class only contains three methods, one is the constructor, one is to write out
   the CFile, and one is to write out the RFile after the search is done. 
"""
class QueenGraph:
	def __init__(self, N, CFile):
		self.queen = [None for i in range(N)]  # a list represents the location of each queen
		self.domain = {i:[i for i in range(N)] for i in range(N)} # a dictionary represents the domain of each queen
		self.contraints = [x for y in [[(i, j, 0), (i, j, j-i)] for i in range(N-1) for j in range(i+1, N)] for x in y] # a list of tuples represent the constraints
		self.size = N # the size of the board
		self.solutions = [] # list of all solutions. Each solution is a list of location values
		self.cFile(CFile) # once construct the class, write out into a file

	def cFile(self, CFile):
		with open(CFile+'.txt', 'w') as file:
			file.writelines("Variables and Domains: \n")
			for i in range(self.size):
				file.writelines("Q{}: {}\n".format(i, self.domain[i]))
			file.writelines("\nContrains: \n")
			for c in self.contraints:
				file.writelines("|Q{} - Q{}| != 0 and {}\n".format(c[0], c[1], c[1]-c[0]))
		
	def rFile(self, RFile, time, steps):
		with open(RFile+'.txt', 'w') as file:
			file.writelines("{} solutions have been found for size {}".format(len(self.solutions), self.size)+'\n')
			file.writelines("Time: {}".format(time)+'\n')
			file.writelines("Total backtrack steps: {}".format(steps)+'\n')
			file.writelines("Note: not exhaustive, stop at 2*N solutions"+'\n\n')
			for s in self.solutions:
				file.writelines("The indexes of each Q in the solution:  ")
				file.writelines(str(s)+'\n')
				for i in range(self.size):
					file.writelines(str([1 if x == s.index(i) else 0 for x in range(self.size)])+'\n')	
				file.writelines('\n')


"""
These two methods implement the MAC algorithm
	queenGraph: a queenGraph instance
	assigned: the index of current assigned queen
"""
def AC3(queenGraph, assigned):
	queue = set()  # a set of all constraints
	unassigned = [] # a list of all unassigned queens
	for q in range(queenGraph.size):
		if queenGraph.queen[q] is not None:  # if the value is a number, means already assigned
			queenGraph.domain[q] = [queenGraph.queen[q]]
		else:  # for unassigned queens, add the constraints
			queue.add((q, assigned, 0))
			queue.add((q, assigned, abs(q-assigned)))
			unassigned.append(q)
	while queue: 
		t = queue.pop()
		if _revise(queenGraph,t):
			if queenGraph.domain[t[0]] == []:
				return False
			for k in set(unassigned)-set([t[0], t[1]]):
				queue.add((k, t[0], 0))
				queue.add((k, t[0], abs(k-t[0])))
	return True
"""queenGraph: a queenGraph instance
   contraint: a tuple represent a contraint. Such as (1, 2, 0) means Q1-Q2 != 0
"""
def _revise(queenGraph, contraint):
	revised = False
	for x in queenGraph.domain[contraint[0]][:]:
		satified = False
		for y in queenGraph.domain[contraint[1]]:
			if abs(x-y) != contraint[2]:
				satified = True
		if not satified:
			queenGraph.domain[contraint[0]].remove(x)
			revised = True
	return revised



"""
These method implement the forward checking algorithm
	queenGraph: a queenGraph instance
	assigned: the index of current assigned queen
"""
def FOR(queenGraph, assigned):
	for var in [i for i, v in enumerate(queenGraph.queen) if v is None]:
		for val in queenGraph.domain[var][:]:
			if (val == queenGraph.queen[assigned]) or (abs(val - queenGraph.queen[assigned]) == abs(var-assigned)):
				queenGraph.domain[var].remove(val)
				if queenGraph.domain[var] == []:
					return False
	return True


"""
These is the back tracking algorithm
	ALG: either 'MAC' or 'FOR'
	queenGraph: a queenGraph instance
	steps: keep track of the number of recursive calls
"""
def backTrack(ALG, queenGraph, steps):
	steps[0] += 1
	if len(queenGraph.solutions) == 2*queenGraph.size:
		return 
	if None not in queenGraph.queen:
		queenGraph.solutions.append(queenGraph.queen[:]) 
		return 
	i = queenGraph.queen.index(None)  # get an index of one unassigned queen
	if queenGraph.domain[i] == []: return

	for value in queenGraph.domain[i]:
		queen = copy.deepcopy(queenGraph.queen)
		domain = copy.deepcopy(queenGraph.domain)
		queenGraph.queen[i] = value
		if ALG == "FOR":
			if FOR(queenGraph, i):
				backTrack(ALG, queenGraph, steps)
		else:
			if AC3(queenGraph, i):
				backTrack(ALG, queenGraph, steps)
		queenGraph.queen = queen
		queenGraph.domain = domain	


def main(ALG, N, CFile, RFile):
	steps = [0]
	q = QueenGraph(N, CFile)
	start = time.time()
	backTrack(ALG, q, steps)
	end = time.time()
	q.rFile(RFile, end-start, steps[0])


if __name__ == '__main__':
	
	import sys, copy, time
	
	_ , ALG, N, CFile, RFile = sys.argv
	assert ALG in ["FOR", "MAC"], "ALG must be FOR or MAC, N must be an int"
	
	main(ALG, int(N), CFile, RFile)
