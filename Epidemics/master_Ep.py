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
fileName = "Results/Experiment-#.dat"
neighbourhood = ((-1,0), (1, 0), (0, 1), (0, -1))
EMPTY, HEALTHY, INFECTED = 0, 1, 2
H = 0.05  #healthy from space
I = 0.001 #infected person arives on the grid
S = 0.5   #probability of catching infection from infected neighbour


# DATA
infectedRecord = dict() # key: size, value: frequency
timeRecord = dict() # key: timestep, value: number of active infecteds

# FUNCTIONS
def CreateMatrix() :
	matrix = np.zeros([numRows, numCols], dtype=int)
	for row in range(0, numRows - 1) :
		for col in range(0, numCols - 1) :
			matrix[row, col] = np.random.choice((EMPTY, HEALTHY, INFECTED), p = [1-(H+I), H, I])	
			
	return matrix
	
def RecordInfectedSize(record, size) :
	if (size != 0) :
		if size in record :
			record[size] += 1
		else :
			record[size] = 1
	return record

def RecordTimeStep(record, timestep, numberOfActiveInfecteds) :
	record[timeStep] = numberOfActiveInfecteds
	return record

def IsHealthyConvertToInfected(matrix, row, col) :
	D = np.random.choice((0,1), p = [1-S , S])
	if (D == 1 and matrix[row, col] == HEALTHY) :
		matrix[row, col] = INFECTED
		return 1
	return 0


def HandleInfected(matrix) :
	infectedLocs = np.where(matrix == INFECTED)
	rowIndexes = infectedLocs[0]
	colIndexes = infectedLocs[1]
	infectedSize = 0
	for i in range (0, len(rowIndexes)) :
		matrix[rowIndexes[i], colIndexes[i]] = EMPTY
		if (rowIndexes[i] != numRows - 1 and colIndexes[i] != numCols - 1 and rowIndexes[i] != 0 and colIndexes[i] != 0) :
			for irow, icol in neighbourhood :
				infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
		else :
			if (rowIndexes[i] == 0 and colIndexes[i] != 0 and colIndexes[i] != numCols - 1): # TOP
				for irow, icol in neighbourhood :
					if (irow == -1) :
						infectedSize += IsHealthyConvertToInfected(matrix, numRows - 1, colIndexes[i] + icol)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (rowIndexes[i] == numRows - 1 and colIndexes[i] != 0 and colIndexes[i] != numCols - 1): # BOTTOM
				for irow, icol in neighbourhood :
					if (irow == 1) :
						infectedSize += IsHealthyConvertToInfected(matrix, 0, colIndexes[i] + icol)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == 0 and rowIndexes[i] != 0 and rowIndexes[i] != numRows - 1) : # LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, numCols - 1)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] != 0 and rowIndexes[i] != numRows - 1) : # RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, 0)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			# CORNER HANDLING
			elif (colIndexes[i] == 0 and rowIndexes[i] == 0) : # TOP LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						infectedSize += IsHealthyConvertToInfected(matrix, 0, numCols - 1)
					elif (irow == -1) :
						infectedSize += IsHealthyConvertToInfected(matrix, numRows - 1, 0)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == 0 and rowIndexes[i] == numRows - 1) : # BOTTOM LEFT
				for irow, icol in neighbourhood :
					if (icol == -1) :
						infectedSize += IsHealthyConvertToInfected(matrix, numRows - 1, numCols - 1)
					elif (irow == 1) :
						infectedSize += IsHealthyConvertToInfected(matrix, 0, 0)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] == 0) : # TOP RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						infectedSize += IsHealthyConvertToInfected(matrix, 0, 0)
					elif (irow == -1) :
						infectedSize += IsHealthyConvertToInfected(matrix, numRows - 1, numCols - 1)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
			elif (colIndexes[i] == numCols - 1 and rowIndexes[i] == numRows - 1) : # BOTTOM RIGHT
				for irow, icol in neighbourhood :
					if (icol == 1) :
						infectedSize += IsHealthyConvertToInfected(matrix, numRows - 1, 0)
					elif (irow == 1) :
						infectedSize += IsHealthyConvertToInfected(matrix, 0, numCols - 1)
					else :
						infectedSize += IsHealthyConvertToInfected(matrix, rowIndexes[i] + irow, colIndexes[i] + icol)
	
	return infectedSize

def UpdateMatrix(matrix) :
	decision = np.random.choice((EMPTY, HEALTHY, INFECTED), p = [1-(H+I), H, I])

	if decision == HEALTHY :
		emptySpace = np.where(matrix == EMPTY)
		rRow = random.randint(0, len(emptySpace[0]) - 1)
		rCol = random.randint(0, len(emptySpace[0]) - 1)
		matrix[emptySpace[0][rRow], emptySpace[1][rCol]] = HEALTHY	
		
	decision = np.random.choice((EMPTY, HEALTHY, INFECTED), p = [1-(H+I), H, I])

	if decision == INFECTED and np.max(matrix) < 2:
		emptySpaces = np.where(matrix == EMPTY)
		rRow = random.randint(0, len(emptySpaces[0]) - 1)
		rCol = random.randint(0, len(emptySpaces[0]) - 1)
		matrix[emptySpaces[0][rRow], emptySpaces[1][rCol]] = INFECTED	
	
	return 0
		
def OutputToFile(matrix, infectedRecord, timeRecord) :
	f = open(fileName, 'w')

	# Output Matrix
	f.write('{:d}\t{:d}\n'.format(numRows, numCols))
	for row in range(0, numRows) :
		for col in range(0, numCols):
			f.write(str(matrix[row][col]))
			f.write('\t')
		f.write('\n')

	# Output Infected Record
	f.write('{:d}\n'.format(len(infectedRecord)))
	for key, value in sorted(infectedRecord.items()) :
		f.write('{:d}\t{:d}\n'.format(key, value))
	
	# Output Time Record
	f.write('{:d}\n'.format(len(timeRecord)))
	for key, value in sorted(timeRecord.items()) :
		f.write('{:d}\t{:d}\n'.format(key, value))

	f.close()
	return 0;
	

# SIMULATION
timeStep = 0
currentInfectedSize = 0

matrix = CreateMatrix()

while timeStep < maxIterations :
	timeStep += 1
	currentInfectedSize += HandleInfected(matrix)
	if (np.max(matrix) < 2) :
		RecordInfectedSize(infectedRecord, currentInfectedSize)
		currentInfectedSize = 0
	RecordTimeStep(timeRecord, timeStep, len(np.where(matrix == 2)[0]))
	UpdateMatrix(matrix)
	
	if (timeStep % 10000 == 0) :
		print ("Time Step: %d" % timeStep)

OutputToFile(matrix, infectedRecord, timeRecord)
