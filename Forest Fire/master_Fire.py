import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import random
import matplotlib.pyplot as plt
from matplotlib import colors

# PARAMETERS
numRows = 100
numCols = 100
maxIterations = 1000000
fileName = "Results/Experiment-#2.dat"
neighbourhood = ((-1,0), (1, 0), (0, 1), (0, -1))
EMPTY, TREE, FIRE = 0, 1, 2
T = 0.05
F = 0.001

# DATA
fireRecord = dict() # key: size, value: frequency
timeRecord = dict() # key: timestep, value: number of active fires

# FUNCTIONS
def CreateMatrix() :
	matrix = np.zeros([numRows, numCols], dtype=int)
	for row in range(0, numRows - 1) :
		for col in range(0, numCols - 1) :
			matrix[row, col] = np.random.choice((EMPTY, TREE, FIRE), p = [1-(T+F), T, F])	
			
	return matrix
	
def RecordFireSize(record, size) :
	if (size != 0) :
		if size in record :
			record[size] += 1
		else :
			record[size] = 1
	return record

def RecordTimeStep(record, timestep, numberOfActiveFires) :
	record[timeStep] = numberOfActiveFires
	return record

def IsTreeConvertToFire(matrix, row, col) :
	if (matrix[row, col] == TREE) :
		matrix[row, col] = FIRE
		return 1
	return 0


def HandleFire(matrix) :
	fireLocs = np.where(matrix == FIRE)
	rowIndexes = fireLocs[0]
	colIndexes = fireLocs[1]
	fireSize = 0
	for i in range (0, len(rowIndexes)) :
		matrix[rowIndexes[i], colIndexes[i]] = EMPTY
		if (rowIndexes[i] != numRows - 1 and colIndexes[i] != numCols - 1 and rowIndexes[i] != 0 and colIndexes[i] != 0) :
			for irow, icol in neighbourhood :
				fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
		else :
			if (rowIndexes[i] == 0 and colIndexes[i] != 0 and colIndexes[i] != numCols - 1): # TOP
				for irow, icol in neighbourhood :
					if (irow == -1) :
						fireSize += IsTreeConvertToFire(matrix, numRows - 1, colIndexes[i] + icol)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (rowIndexes[i] == numRows - 1 and colIndexes[i] != 0 and colIndexes[i] != numCols - 1): # BOTTOM
				for irow, icol in neighbourhood :
					if (irow == 1) :
						fireSize += IsTreeConvertToFire(matrix, 0, colIndexes[i] + icol)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == 0 and rowIndexes[i] != 0 and rowIndexes[i] != numRows - 1) : # LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, numCols - 1)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] != 0 and rowIndexes[i] != numRows - 1) : # RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, 0)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			# CORNER HANDLING
			elif (colIndexes[i] == 0 and rowIndexes[i] == 0) : # TOP LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						fireSize += IsTreeConvertToFire(matrix, 0, numCols - 1)
					elif (irow == -1) :
						fireSize += IsTreeConvertToFire(matrix, numRows - 1, 0)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == 0 and rowIndexes[i] == numRows - 1) : # BOTTOM LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						fireSize += IsTreeConvertToFire(matrix, numRows - 1, numCols - 1)
					elif (irow == 1) :
						fireSize += IsTreeConvertToFire(matrix, 0, 0)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] == 0) : # TOP RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						fireSize += IsTreeConvertToFire(matrix, 0, 0)
					elif (irow == -1) :
						fireSize += IsTreeConvertToFire(matrix, numRows - 1, numCols - 1)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] == numRows - 1) : # BOTTOM RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						fireSize += IsTreeConvertToFire(matrix, numRows - 1, 0)
					elif (irow == 1) :
						fireSize += IsTreeConvertToFire(matrix, 0, numCols - 1)
					else :
						fireSize += IsTreeConvertToFire(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
	
	return fireSize

def UpdateMatrix(matrix) :
	decision = np.random.choice((EMPTY, TREE, FIRE), p = [1-(T+F), T, F])

	if decision == TREE :
		emptySpace = np.where(matrix == EMPTY)
		rRow = random.randint(0, len(emptySpace[0]) - 1)
		rCol = random.randint(0, len(emptySpace[0]) - 1)
		matrix[emptySpace[0][rRow], emptySpace[1][rCol]] = TREE	
		
	decision = np.random.choice((EMPTY, TREE, FIRE), p = [1-(T+F), T, F])

	if decision == FIRE and np.max(matrix) < 2:
		treeSpaces = np.where(matrix == TREE)
		rRow = random.randint(0, len(treeSpaces[0]) - 1)
		rCol = random.randint(0, len(treeSpaces[0]) - 1)
		matrix[treeSpaces[0][rRow], treeSpaces[1][rCol]] = FIRE	
	
	return 0
	
def PlotForest() :
	global matrix
	cmap = colors.ListedColormap(['white', 'darkgreen', 'red'])
	bounds=[-0.5,0.5,1.5,2.5]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
	#plot = ax.imshow(matrix, interpolation = 'nearest', cmap)
	plot = ax.imshow(matrix, cmap=cmap, norm=norm, interpolation='none', vmax=2, vmin = 0)
	plot.set_clim(vmin = 0, vmax = 2)
	colourBar = fig.colorbar(plot, ticks = [0, 1, 2], orientation = 'vertical', fraction = 0.045)
	ax.set_title('Critical Points')
	ax.set_xlabel('X-Coordinate')
	ax.set_ylabel('Y-Coordinate')
	plt.draw()
	plt.show()
	return 0
	
def PlotFireRecord() :
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
	ax.set_yscale('log')
	ax.set_xscale('log')

	sizes = list()
	frequency = list()
	linearSizes = list()
	linearFrequency = list()
	for key, value in sorted(fireRecord.items()) :
		sizes.append(key)
		frequency.append(value)
		if (key <= 300) :
			linearSizes.append(key)
			linearFrequency.append(value)

	m, c = np.polyfit(np.log(linearSizes), np.log(linearFrequency), 1)
	print(m)
	yfit = np.exp(m*np.log(sizes) + c)

	ax.scatter(sizes, frequency)
	ax.plot(sizes, yfit, 'red')
	ax.text(1000, 2500, 'm = {:.2f}'.format(m))

	plt.draw()
	return 0
	
def PlotTimeRecord() :
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)

	timesteps = list()
	sizes = list()
	lastKeyValue = 0
	maxActiveFireSize = 0
	for key, value in (timeRecord.items()) :
		timesteps.append(key)
		sizes.append(value)
		lastKeyValue = key
		if (value > maxActiveFireSize) : 
			maxActiveFireSize = value

	ax.set_xlim(-100, lastKeyValue+100)
	ax.set_ylim(0, maxActiveFireSize+10)
	ax.scatter(timesteps, sizes)

	plt.draw()
	return 0
	
def OutputToFile(matrix, fireRecord, timeRecord) :
	f = open(fileName, 'w')

	# Output Matrix
	f.write('{:d}\t{:d}\n'.format(numRows, numCols))
	for row in range(0, numRows) :
		for col in range(0, numCols):
			f.write(str(matrix[row][col]))
			f.write('\t')
		f.write('\n')

	# Output Fire Record
	f.write('{:d}\n'.format(len(fireRecord)))
	for key, value in sorted(fireRecord.items()) :
		f.write('{:d}\t{:d}\n'.format(key, value))
	
	# Output Time Record
	f.write('{:d}\n'.format(len(timeRecord)))
	for key, value in sorted(timeRecord.items()) :
		f.write('{:d}\t{:d}\n'.format(key, value))

	f.close()
	return 0;
	

# SIMULATION
timeStep = 0
currentFireSize = 0

matrix = CreateMatrix()

while timeStep < maxIterations :
	timeStep += 1
	currentFireSize += HandleFire(matrix)
	if (np.max(matrix) < 2) :
		RecordFireSize(fireRecord, currentFireSize)
		currentFireSize = 0
	RecordTimeStep(timeRecord, timeStep, len(np.where(matrix == 2)[0]))
	UpdateMatrix(matrix)
	
	if (timeStep % 10000 == 0) :
		print ("Time Step: %d" % timeStep)

OutputToFile(matrix, fireRecord, timeRecord)
