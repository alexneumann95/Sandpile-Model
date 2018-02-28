import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import random

# PARAMETERS
numRows = 51
numCols = 51
k = 4
maxGrainCount = 100000
kMatrix = np.full([numRows, numCols], k, dtype=int)
fileName = "Results/DropRate/Experiment-1.dat"

# DATA CONTAINERS
avalancheRecord = dict() # Key: Avalanche Size, Value: Frequency
timeRecord = dict() # Key: Time Step, Value: Avalanche Size

# FUNCTIONS
def CreateMatrix() :
	""" Creates, initialises and returns a numRows x numCols 2D numpy array set to the value of 0 """
	global numRows, numCols
	matrix = np.zeros([numRows, numCols], dtype=int)
	return matrix

def ApplyInitialConditions(matrix) :
	""" Applies a random set of initial conditions to the matrix, and lets it settle """
	global numRows, numCols	
	for row in range(1, (numRows - 1)):
		for col in range(1, (numCols - 1)):
			matrix[row][col] = random.randint(k*10, k*20)

	locations = CheckForAvalanche(matrix)

	while(len(locations[0]) != 0) :
			HandleAvalanches(matrix, locations)
			ApplyBoundaryConditions(matrix)
			locations = CheckForAvalanche(matrix)	
	return matrix

def AddGrain(matrix) :
	""" Adds a grain to a random location in the 2D numpy array """
	numGrains = 0
	for i in range(0, 2) :	
		row = random.randint(1, (numRows - 2))
		col = random.randint(1, (numCols - 2))
		matrix[row, col] += 1
		numGrains += 1
	return numGrains

def CheckForAvalanche(matrix) :
	""" Checks for an avalanche and returns a tuple of ndarrays of indexes of avalanche locations.
		First array is all the row indexes, second array is all the column indexes. """
	global kMatrix
	result = matrix - kMatrix
	locations = np.where(result >= 0)
	return locations

def HandleAvalanches(matrix, locations) :
	""" Takes in the matrix and a tuple of ndarrays of indexes containing the location of avalanches.
		Computes the sandpile model. Returns the size of avalanche that occured in just one check of
		the matrix. """
	rowIndexes = locations[0]
	colIndexes = locations[1]	
	size = 0
	for i in range(0, len(locations[0])) :
		matrix[rowIndexes[i], colIndexes[i]] -= k
		matrix[rowIndexes[i] + 1, colIndexes[i]] += 1
		matrix[rowIndexes[i] - 1, colIndexes[i]] += 1
		matrix[rowIndexes[i], colIndexes[i] + 1] += 1
		matrix[rowIndexes[i], colIndexes[i] - 1] += 1
		size += 1
	return size

def RecordAvalancheSize(record, size) :
	""" Records the size of avalanche into the avalanche record (dict) """
	if (size != 0) :
		if size in record :
			record[size] += 1
		else :
			record[size] = 1
	return record

def RecordTimestep(record, timestep, size) :
	""" Records the size of avalanche for the timestep into the time record (dict) """
	record[timestep] = size
	return record

def ApplyBoundaryConditions(matrix) :
	""" Sets the top & bottom row as well as the first and last column of the matrix to 0 """
	global numRows, numCols
	matrix[0, 0:(numCols - 1)] = 0				# Top Row
	matrix[(numRows - 1), 0:(numCols - 1)] = 0	# Bottom Row
	matrix[0:(numRows - 1), 0] = 0				# First Column
	matrix[0:(numRows - 1), (numCols - 1)] = 0	# Last Column
	return matrix

def OutputToFile(matrix, avalancheRecord, timeRecord) :
	global numRows, numCols	
	f = open(fileName, 'w')

	# Output Matrix
	f.write('{:d}\t{:d}\n'.format(numRows, numCols))
	for row in range(0, numRows) :
		for col in range(0, numCols):
			f.write(str(matrix[row][col]))
			f.write('\t')
		f.write('\n')

	# Output Avalanche Record
	f.write('{:d}\n'.format(len(avalancheRecord)))
	for key, value in sorted(avalancheRecord.items()) :
		f.write('{:d}\t{:d}\n'.format(key, value))
	
	# Output Time Record
	f.write('{:d}\n'.format(len(timeRecord)))
	for key, value in sorted(timeRecord.items()) :
		f.write('{:d}\t{:d}\n'.format(key, value))

	f.close()
	return 0

# SET UP INITIAL CONDITIONS
startTime = time.time()
matrix = CreateMatrix()
matrix = ApplyInitialConditions(matrix)
numGrains = 0 # Current grain count
timeStep = 0
print('Applied Initial Conditions! Time took: {:.2f} s'.format(time.time() - startTime))

# SIMULATION
startTime = time.time()
while (numGrains < maxGrainCount) :
	timeStep += 1
	numGrains += AddGrain(matrix)

	locations = CheckForAvalanche(matrix)
	size = 0

	while (len(locations[0]) != 0) :
		size += HandleAvalanches(matrix, locations)
		ApplyBoundaryConditions(matrix)
		locations = CheckForAvalanche(matrix)

	RecordAvalancheSize(avalancheRecord, size)
	RecordTimestep(timeRecord, timeStep, size)

	if (numGrains % 10000 == 0) :
		print('Grains added: {}, Time taken to execute so far: {:.2f} s'.format(numGrains, time.time() - startTime))

OutputToFile(matrix, avalancheRecord, timeRecord)
	
