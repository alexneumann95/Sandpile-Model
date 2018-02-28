import numpy as np
import matplotlib.pyplot as plt

# PARAMETERS
dataFile = "Results/CriticalPoints/Experiment-13.dat"
numRows = 0
numCols = 0
matrix = np.array([])
avalancheRecord = dict() # Key: Avalanche Size, Value: Frequency
timeRecord = dict() # Key: Time Step, Value: Avalanche Size
numIterations = 0

# FUNCTIONS
def ReadData() :
	global numRows, numCols, matrix, avalancheRecord, timeRecord, numIterations

	f = open(dataFile)
		
	# Read in matrix data
	numRows, numCols = map(int, f.readline().split())
	matrix = np.zeros([numRows, numCols])
	rowNo = 0
	for line in f :
		matrix[rowNo, :] = line.split()		
		rowNo += 1	
		if (rowNo == numRows) :
			break

	# Read in avalanche data
	avalancheRecordSize = int(f.readline())
	recordNo = 1
	for line in f :
		key, value = map(int, line.split())
		avalancheRecord[key] = value
		recordNo += 1
		if (recordNo > avalancheRecordSize) :
			break

	# Read in time data
	timeRecordSize = int(f.readline())
	numIterations = timeRecordSize
	timeNo = 1
	for line in f :
		key, value = map(int, line.split())
		timeRecord[key] = value
		timeNo += 1
		if (timeNo > timeRecordSize) :
			break

	f.close()
	return 0

def PlotSandpile() :
	global matrix
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
	plot = ax.imshow(matrix, interpolation = 'nearest')
	plot.set_clim(vmin = 0, vmax = 3)
	colourBar = fig.colorbar(plot, ticks = [0, 1, 2, 3], orientation = 'vertical', fraction = 0.045)
	ax.set_title('Sandpile Height')
	ax.set_xlabel('X-Coordinate')
	ax.set_ylabel('Y-Coordinate')
	plt.draw()
	return 0

def PlotPowerLaw() :
	global avalancheRecord, numIterations
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
	ax.set_title('Frequency vs Size of Avalanche (Iterations: {:d})'.format(numIterations))
	ax.set_xlabel('Size')
	ax.set_ylabel('Frequency')
	ax.set_yscale('log')
	ax.set_xscale('log')

	sizes = list()
	frequency = list()
	linearSizes = list()
	linearFrequency = list()
	for key, value in sorted(avalancheRecord.items()) :
		sizes.append(key)
		frequency.append(value)
		if (key <= 300) :
			linearSizes.append(key)
			linearFrequency.append(value)

	m, c = np.polyfit(np.log(linearSizes), np.log(linearFrequency), 1)
	yfit = np.exp(m*np.log(sizes) + c)

	ax.scatter(sizes, frequency)
	ax.plot(sizes, yfit, 'red')
	ax.text(1000, 2500, 'm = {:.2f}'.format(m))

	plt.draw()
	return 0

def PlotTimeStructure() :
	global timeRecord, numIterations
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
	ax.set_title('Size of Avalanche vs Time (Iterations: {:d})'.format(numIterations))
	ax.set_xlabel('Time Step')
	ax.set_ylabel('Size')

	timesteps = list()
	sizes = list()
	lastKeyValue = 0
	maxAvalancheSize = 0
	for key, value in (timeRecord.items()) :
		timesteps.append(key)
		sizes.append(value)
		lastKeyValue = key
		if (value > maxAvalancheSize) : 
			maxAvalancheSize = value

	ax.set_xlim(-100, lastKeyValue+100)
	ax.set_ylim(0, maxAvalancheSize+100)
	ax.scatter(timesteps, sizes)

	plt.draw()
	return 0

ReadData()
plt.ion()
PlotSandpile()
PlotPowerLaw()
PlotTimeStructure()
plt.show()
