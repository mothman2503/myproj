import numpy as np
import random
import time


def isOk(grid, num, row, col):

	for x in range(9):
		if grid[row][x] == num or grid[x][col] == num:
			return False

	quad_row = row - row % 3
	quad_col = col - col % 3

	for i in range(3):
		for j in range(3):
			if grid[quad_row + i][quad_col + j] == num:
				return False


	return True

def isSolvable(row, col, nogo = 10, nrow = 10, ncol = 10, createNew = False):

	if createNew:
		for i in range(9):
			rnum = random.randint(1, 9)
			while refgrid[0][i] == 0:
				if isOk(refgrid, rnum, 0, i):
					refgrid[0][i] = rnum
				rnum = random.randint(1, 9) 

	if row == 8 and col == 9:
		return True

	if col == 9:
		col = 0
		row += 1

	if refgrid[row][col] != 0:

		return isSolvable(row, col + 1, nogo = nogo, nrow = nrow, ncol = ncol)

	for num in range(1, 10, 1):

		if not (num == nogo and nrow == row and ncol == col) and isOk(refgrid, num, row, col) :

			refgrid[row][col] = num
			
			if isSolvable(row, col + 1, nogo = nogo, nrow = nrow, ncol = ncol):
				return True

		refgrid[row][col] = 0

	return False

def printG():
	
	for j in range(9):
		if (j%3) == 0:
			print("\n")
		for i in range(9):
			if (i%3) == 0:
				print("   ", end = " ")
			if refgrid[j][i] != 0:
				print(refgrid[j][i], end = "   ")
			if refgrid[j][i] == 0:
				print("_", end = "   ")
		print("\n")

class game:

	currow = 4
	curcol = 4

	grid = np.zeros((9,9), dtype = int)
	gridB = np.zeros((9,9), dtype = int)
	grid_ref = np.zeros((9,9), dtype = int)
	won = False
	solved = False

	def newgame(self, difficulty):

		global refgrid
		refgrid = np.zeros((9,9), dtype = int)


		self.solved = False
		self.won = False

		self.grid = np.zeros((9,9), dtype = int)
		refgrid = np.zeros((9,9), dtype = int)

		# generating a complete grid of sudoku
		isSolvable(0, 0, createNew = True)

		
		# will transpose either once or twice
		for i in range(random.randint(0,2)):
			refgrid = refgrid.transpose()

		# will rotate 0 to 4 times
		x = random.randint(0, 5)
		for i in range(x):
			refgrid = np.rot90(refgrid)

		# ciphering 3 to 10 times
		ciph = random.randint(3, 10)

		for i in range(ciph):

			x = random.randint(1, 9)
			y = random.randint(1, 9)

			refgrid[refgrid == x] = 0
			refgrid[refgrid == y] = x
			refgrid[refgrid == 0] = y

		#easy = 35 clues
		#medium = 31 clues
		#hard = 29 clues

		clues = 0


		if difficulty == "easy":
			clues = 35
		elif difficulty == "medium":
			clues = 31
		else:
			clues = 29

		#main backup in case it gets stuck/slow
		self.grid = np.array(refgrid)

		start = time.perf_counter_ns()
		start_abs = time.perf_counter_ns()

		while np.count_nonzero(refgrid) != clues:
			
			# checking to see if too slow. if yes, starting over.
			dur = (time.perf_counter_ns() - start)/1000000
			tot_dur = (time.perf_counter_ns() - start_abs)/1000000000

			if dur > 100 or tot_dur > 1:
				start_abs = time.perf_counter_ns()
				print("interrupted")
				refgrid = np.array(self.grid)

			start = time.perf_counter_ns()

			#blanking out the next rotational pair
			backup = np.array(refgrid)

			x = random.randint(0, 8)
			y = random.randint(0, 8) 

			if refgrid[x][y] == 0 or (x == 4 and y == 4):
				continue

			a = refgrid[x][y]
			b = refgrid[8 - x][8 - y]

			refgrid[x][y] = 0
			refgrid[8 - x][8 - y] = 0

			tmp = np.array(refgrid)

			if isSolvable(0,0, nogo = a, nrow = x, ncol = y):
				refgrid = np.array(backup)
				continue

			refgrid = np.array(tmp)

			if isSolvable(0,0, nogo = b, nrow = 8 - x, ncol = 8 - y):
				refgrid = np.array(backup)
				continue


		printG()			
		self.grid = np.array(refgrid)
		self.gridB = np.array(refgrid)

		print("\nNew puzzle generated successfully")

	def solve(self):

		global refgrid
		refgrid = self.gridB.copy()

		self.solved = isSolvable(0,0)
		printG()
		self.grid = np.array(refgrid)

	def disp_col(self, row, col):

		if self.gridB[row][col] != 0:
			return {"num" : str(self.grid[row][col]), "color" : 'blue'}
		elif self.solved:
			if self.won:
				return {"num" : str(self.grid[row][col]), "color" : 'green'}
			return {"num" : str(self.grid[row][col]), "color" : 'red'}
		elif self.grid[row][col] != 0:
			return {"num" : str(self.grid[row][col]), "color" : 'black'}
		else:
			return {"num" : '_', "color" : 'black'}




