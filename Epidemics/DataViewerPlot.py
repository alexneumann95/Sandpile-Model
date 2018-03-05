import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import time
from time import gmtime, strftime

# PARAMETERS

expNo = input("Experiment Number: ")
timeStamp = time.strftime("%j(%H%-M%-S)", gmtime())
dataFile = "Results/Experiment-%s.dat"%expNo
title_ = dataFile[8:-4]
numRows = 0
numCols = 0
matrix = np.array([])
infectedRecord = dict() # Key: infected Size, Value: Frequency
timeRecord = dict() # Key: Time Step, Value: Avalanche Size
numIterations = 0

# FUNCTIONS
def ReadData() :
	global numRows, numCols, matrix, infectedRecord, timeRecord, numIterations

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
	infectedRecordSize = int(f.readline())
	recordNo = 1
	for line in f :
		key, value = map(int, line.split())
		infectedRecord[key] = value
		recordNo += 1
		if (recordNo > infectedRecordSize) :
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

def PlotinfectedForest() :
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

def PlotinfectedRecord() :
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)
	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_title('Frequency of Epidemic vs Size of Epidemic')
	ax.set_xlabel('Size')
	ax.set_ylabel('Frequency')

	sizes = list()
	frequency = list()
	linearSizes = list()
	linearFrequency = list()
	for key, value in sorted(infectedRecord.items()) :
		sizes.append(key)
		frequency.append(value)
		if (key <= 0.075*len(infectedRecord))  :
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
	ax.set_title('Number of infected vs Time Step')
	ax.set_xlabel('Time Step')
	ax.set_ylabel('Number')

	timesteps = list()
	sizes = list()
	lastKeyValue = 0
	maxActiveinfectedSize = 0
	for key, value in (timeRecord.items()) :
		timesteps.append(key)
		sizes.append(value)
		lastKeyValue = key
		if (value > maxActiveinfectedSize) : 
			maxActiveinfectedSize = value

	ax.set_xlim(-100, lastKeyValue+100)
	ax.set_ylim(0, maxActiveinfectedSize+10)
	ax.plot(timesteps, sizes)

	plt.draw()
	return 0
	
def PlotTimeDepend() :
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)

	timesteps = list()
	sizes = list()
	lastKeyValue = 0
	maxActiveinfectedSize = 0
	currentEpidemicSize = 0

	for key, value in (timeRecord.items()) :
		if value == 0 :
			if (currentEpidemicSize != 0) :
				timesteps.append(key - 1)
				sizes.append(currentEpidemicSize)
				currentEpidemicSize = 0
			if (currentEpidemicSize > maxActiveinfectedSize) : 
				maxActiveinfectedSize = currentEpidemicSize	
		if value > 0:
			currentEpidemicSize += value

	dataLength  = len(sizes)
	timeSize = sizes[1:dataLength]
	PreviousTimeSize = sizes[0:dataLength-1]
	ax.scatter(timeSize, PreviousTimeSize)
	ax.set_title("Time Dependence")
	ax.set_ylabel("Previous Infection Size")
	ax.set_xlabel("Infection Size")
	
	#correlation coefficient
	C = np.corrcoef(timeSize, PreviousTimeSize)[1,0]
	print(C)
	ax.text(0, 0.98*np.max(PreviousTimeSize), "Correlation = %1.7f"%C)
	
	
	plt.draw()
	
	return 0

#GAP SIZE
def downTime():
	fig = plt.figure(figsize = (9,9))
	ax = plt.subplot(111)

	downTimes = list()
	sizes = list()
	maxActiveinfectedSize = 0
	downTimeLength = 0
	currentEpidemicSize = 0
	
	for key, value in (timeRecord.items()) :
		if value == 0:
			downTimeLength += 1
			if (currentEpidemicSize != 0) :
				sizes.append(currentEpidemicSize)
				currentEpidemicSize = 0
		elif value > 0:
			if (downTimeLength != 0) :
				downTimes.append(downTimeLength)
				downTimeLength = 0
			currentEpidemicSize += value
			if (currentEpidemicSize > maxActiveinfectedSize) : 
				maxActiveinfectedSize = currentEpidemicSize

	if (len(downTimes) != len(sizes)) :
		if (downTimeLength != 0) :
			downTimes.append(downTimeLength)
	
	ax.scatter(downTimes, sizes)
	
	ax.set_ylabel("Size")
	ax.set_xlabel("Down Time")
	
	#correlation coefficient
	C = np.corrcoef(downTimes, sizes)[1,0]
	print(C)
	ax.set_title("Down Times Vs Size of Infection - Correlation = %1.4f"%C)
	
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
	for key, value in sorted(infectedRecord.items()) :
		sizes.append(key)
		frequency.append(value)
		if (key <= 0.075*len(infectedRecord)) :
			linearSizes.append(key)
			linearFrequency.append(value)

	m, c = np.polyfit(np.log(linearSizes), np.log(linearFrequency), 1)
	yfit = np.exp(m*np.log(sizes) + c)

	ax2.scatter(sizes, frequency)
	ax2.plot(sizes, yfit, 'red')

	#Matrix
	cmap = colors.ListedColormap(['white', 'springgreen', 'red'])
	bounds=[-0.5,0.5,1.5,2.5]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	plot = ax4.imshow(matrix, cmap=cmap, norm=norm, interpolation='none', vmax=2, vmin = 0)
	colourBar = fig.colorbar(plot, ticks = [0, 1, 2], orientation = 'vertical', fraction = 0.045)
	ax4.set_title('Critical Points')
	ax4.set_xlabel('X-Coordinate')
	ax4.set_ylabel('Y-Coordinate')
	
	#time structure
	ax3.set_title('Size of infected vs Time (Iterations: {:d})'.format(numIterations))
	ax3.set_xlabel('Time Step')
	ax3.set_ylabel('Size')

	timesteps = list()
	sizes = list()
	lastKeyValue = 0
	maxActiveinfectedSize = 0
	for key, value in (timeRecord.items()) :
		timesteps.append(key)
		sizes.append(value)
		lastKeyValue = key
		if (value > maxActiveinfectedSize) : 
			maxActiveinfectedSize = value

	ax3.set_xlim(-100, lastKeyValue+100)
	ax3.set_ylim(0, maxActiveinfectedSize+10)
	ax3.scatter(timesteps, sizes)
	
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
	ax1.text(0, 7, 'Max infected Size = {:.2f}'.format(maxActiveinfectedSize), fontsize=20)
	ax1.text(0, 5, 'Grid size = {:.1f} X {:.1f}'.format(numRows, numCols), fontsize=20)	
	ax1.text(0, 3, 'Iterations = {:.1f}'.format(numIterations), fontsize=20)
	ax1.text(0, 1, 'Data Points = {:.1f}'.format(len(infectedRecord)), fontsize=20)

	#save file
	fig.savefig('Results/%s-%s.pdf'%(title_,timeStamp))
	plt.close(fig)
	

	
	#time Dependance
	fig = plt.figure(figsize = (20,20))
	ax = plt.subplot(111)
	timesteps = list()
	sizes = list()
	lastKeyValue = 0
	maxActiveinfectedSize = 0
	
	for key, value in (timeRecord.items()) :
		if value > 0:
			timesteps.append(key)
			sizes.append(value)
			lastKeyValue = key
			if (value > maxActiveinfectedSize) : 
				maxActiveinfectedSize = value
	dataLength  = len(sizes)
	timeSize = sizes[1:dataLength]
	PreviousTimeSize = sizes[0:dataLength-1]
	ax.scatter(timeSize, PreviousTimeSize)
	ax.set_title("Time Dependence")
	ax.set_ylabel("Previous Infection Size")
	ax.set_xlabel("Infection Size")
	
	#correlation coefficient
	C = np.corrcoef(timeSize, PreviousTimeSize)[1,0]
	ax.text(0, 0.99*np.max(PreviousTimeSize), "Correlation = %1.4f"%C)

	fig.savefig('Results/%s-%s-TIME.pdf'%(title_,timeStamp))
	plt.close(fig)	
	
	return 0;


ReadData()
plt.ion()
PlotinfectedForest()
PlotinfectedRecord()
PlotTimeRecord()
PlotTimeDepend()
downTime()
plt.show()
#save_all()

