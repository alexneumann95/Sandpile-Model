import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import random
import matplotlib.pyplot as plt
from matplotlib import colors

# PARAMETERS
numRows = 50
numCols = 50
maxIterations = 100000
fileName = "Results/Experiment-#.dat"
neighbourhood = ((-1,0), (1, 0), (0, 1), (0, -1))
EMPTY, TREE, FIRE = 0, 1, 2
T = 0.05 * 10
F = 0.001

# IGNORE ME
number = 0

# FUNCTIONS
def CreateMatrix() :
	matrix = np.zeros([numRows, numCols], dtype=int)
	for row in range(0, numRows - 1) :
		for col in range(0, numCols - 1) :
			matrix[row, col] = np.random.choice((EMPTY, TREE, FIRE), p = [1-(T+F), T, F])	
			
	return matrix
	
def IsTreeConvertToFire(matrix, row, col) :
	if (matrix[row, col] == TREE) :
		matrix[row, col] = FIRE
	return matrix

def HandleFire(matrix) :
	fireLocs = np.where(matrix == FIRE)
	rowIndexes = fireLocs[0]
	colIndexes = fireLocs[1]
	for i in range (0, len(rowIndexes)) :
		matrix[rowIndexes[i], colIndexes[i]] = EMPTY
		if (rowIndexes[i] != numRows - 1 and colIndexes[i] != numCols - 1 and rowIndexes[i] != 0 and colIndexes[i] != 0) :
			for irow, icol in neighbourhood :
				IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
		else :
			if (rowIndexes[i] == 0 and colIndexes[i] != 0 and colIndexes[i] != numCols - 1): # TOP
				for irow, icol in neighbourhood :
					if (irow == -1) :
						IsTreeConvertToFire(matrix, numRows - 1, colIndexes[i] + icol)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (rowIndexes[i] == numRows - 1 and colIndexes[i] != 0 and colIndexes[i] != numCols - 1): # BOTTOM
				for irow, icol in neighbourhood :
					if (irow == 1) :
						IsTreeConvertToFire(matrix, 0, colIndexes[i] + icol)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == 0 and rowIndexes[i] != 0 and rowIndexes[i] != numRows - 1) : # LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, numCols - 1)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] != 0 and rowIndexes[i] != numRows - 1) : # RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, 0)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			# CORNER HANDLING
			elif (colIndexes[i] == 0 and rowIndexes[i] == 0) : # TOP LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						IsTreeConvertToFire(matrix, 0, numCols - 1)
					elif (irow == -1) :
						IsTreeConvertToFire(matrix, numRows - 1, 0)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == 0 and rowIndexes[i] == numRows - 1) : # BOTTOM LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						IsTreeConvertToFire(matrix, numRows - 1, numCols - 1)
					elif (irow == 1) :
						IsTreeConvertToFire(matrix, 0, 0)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] == 0) : # TOP RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						IsTreeConvertToFire(matrix, 0, 0)
					elif (irow == -1) :
						IsTreeConvertToFire(matrix, numRows - 1, numCols - 1)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] == numRows - 1) : # BOTTOM RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						IsTreeConvertToFire(matrix, numRows - 1, 0)
					elif (irow == 1) :
						IsTreeConvertToFire(matrix, 0, numCols - 1)
					else :
						IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
	
	return 0

def UpdateMatrix(matrix) :
	decision = np.random.choice((EMPTY, TREE, FIRE), p = [1-(T+F), T, F])

	if decision == TREE :
		emptySpace = np.where(matrix == EMPTY)
		rRow = random.randint(0, len(emptySpace[0]) - 1)
		rCol = random.randint(0, len(emptySpace[0]) - 1)
		matrix[emptySpace[0][rRow], emptySpace[1][rCol]] = TREE	
		
	decision = np.random.choice((EMPTY, TREE, FIRE), p = [1-(T+F), T, F])

	if decision == FIRE :
		treeSpaces = np.where(matrix == TREE)
		rRow = random.randint(0, len(treeSpaces[0]) - 1)
		rCol = random.randint(0, len(treeSpaces[0]) - 1)
		matrix[treeSpaces[0][rRow], treeSpaces[1][rCol]] = FIRE	
	
	return 0

# SIMULATION
timeStep = 0

matrix = CreateMatrix()

# PLOTTING
cmap = colors.ListedColormap(['white', 'darkgreen', 'red'])
bounds=[-0.5,0.5,1.5,2.5]
norm = colors.BoundaryNorm(bounds, cmap.N)
fig = plt.figure(figsize = (9,9))
ax = plt.subplot(111)
plot = ax.imshow(matrix, cmap=cmap, norm=norm, interpolation='none', vmax=2, vmin = 0)
colourBar = fig.colorbar(plot, ticks = [0, 1, 2], orientation = 'vertical', fraction = 0.045)
ax.set_title('Critical Points')
ax.set_xlabel('X-Coordinate')
ax.set_ylabel('Y-Coordinate')
plt.ion()

def UpdatePlot() :
	plot.set_data(matrix)
	plt.draw()
	plt.pause(0.00001)
	return 0

while timeStep < maxIterations :
	timeStep += 1
	HandleFire(matrix)
	UpdateMatrix(matrix)
	if (number % 2 == 0) :
		UpdatePlot()
	number += 1
