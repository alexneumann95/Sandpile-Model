import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import time
from time import gmtime, strftime

# PARAMETERS

expNo = input("Experiment Number: ")
timeStamp = time.strftime("%H%M%S", gmtime())
dataFile = "Results/Experiment-%s.dat"%expNo
title_ = dataFile[8:-4]
numRows = 0
numCols = 0
matrix = np.array([])
fireRecord = dict() # Key: Fire Size, Value: Frequency
timeRecord = dict() # Key: Time Step, Value: Avalanche Size
numIterations = 0

# FUNCTIONS
def ReadData() :
	global numRows, numCols, matrix, fireRecord, timeRecord, numIterations

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
	fireRecordSize = int(f.readline())
	recordNo = 1
	for line in f :
		key, value = map(int, line.split())
		fireRecord[key] = value
		recordNo += 1
		if (recordNo > fireRecordSize) :
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

def PlotFireForest() :
	global matrix
	cmap = colors.ListedColormap(['white', 'darkgreen', 'red'])
	bounds=[-0.5,0.5,1.5,2.5]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
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
	ax.plot(timesteps, sizes)

	plt.draw()
	return 0

def save_all():
	global timeRecord, numIterations, avalancheRecord, numIterations, matrix, title_
	fig = plt.figure(figsize = (20,20))
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	
	#powerlaw
	ax2.set_title('Frequency vs Size of Avalanche (Iterations: {:d})'.format(numIterations))
	ax2.set_xlabel('Size')
	ax2.set_ylabel('Frequency')
	ax2.set_yscale('log')
	ax2.set_xscale('log')

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
	yfit = np.exp(m*np.log(sizes) + c)

	ax2.scatter(sizes, frequency)
	ax2.plot(sizes, yfit, 'red')

	#Matrix
	cmap = colors.ListedColormap(['white', 'darkgreen', 'red'])
	bounds=[-0.5,0.5,1.5,2.5]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	plot = ax4.imshow(matrix, cmap=cmap, norm=norm, interpolation='none', vmax=2, vmin = 0)
	colourBar = fig.colorbar(plot, ticks = [0, 1, 2], orientation = 'vertical', fraction = 0.045)
	ax4.set_title('Critical Points')
	ax4.set_xlabel('X-Coordinate')
	ax4.set_ylabel('Y-Coordinate')
	
	#time structure
	ax3.set_title('Size of Fire vs Time (Iterations: {:d})'.format(numIterations))
	ax3.set_xlabel('Time Step')
	ax3.set_ylabel('Size')

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

	ax3.set_xlim(-100, lastKeyValue+100)
	ax3.set_ylim(0, maxActiveFireSize+10)
	ax3.plot(timesteps, sizes)
	
	#largest time structure
	sizes = np.asarray(sizes)
	sortSizes = np.sort(sizes)
	Largest10 = sortSizes[-11]
	timesteps = np.asarray(timesteps)
	Largest10loc = np.where(sizes >= np.min(Largest10))
	lgTime = timesteps[Largest10loc[0]]
	lgSize = sizes[Largest10loc[0]]
	ax3.scatter(lgTime,lgSize, color = 'r')

	#Info panel
	ax1.axis('off')
	ax1.set_xlim(0,10)
	ax1.set_ylim(0,10)
	ax1.set_title(title_)
	ax1.text(0, 9, 'Gradient = {:.2f}'.format(m), fontsize=20)
	ax1.text(0, 7, 'Max Fire Size = {:.2f}'.format(maxActiveFireSize), fontsize=20)
	ax1.text(0, 5, 'Grid size = {:.1f} X {:.1f}'.format(numRows, numCols), fontsize=20)	
	ax1.text(0, 3, 'Iterations = {:.1f}'.format(numIterations), fontsize=20)
	ax1.text(0, 1, 'Data Points = {:.1f}'.format(len(fireRecord)), fontsize=20)

	#save file
	fig.savefig('Results/%s-%s.pdf'%(title_,timeStamp))
	plt.close(fig)
	return 0;


ReadData()
plt.ion()
PlotFireForest()
PlotFireRecord()
PlotTimeRecord()
plt.show()
save_all()

