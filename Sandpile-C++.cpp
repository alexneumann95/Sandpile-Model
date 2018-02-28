/*
	This is the Sandpile model already created in python but written in a C like way
	in order to gain the performance benefits of C++ when working with large
	matrices.
*/
#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <map>
#include <time.h>
using std::string;	using std::cout;	using std::endl;	using std::map;

// PARAMETERS
#define NUM_ROWS 51
#define NUM_COLS 51
#define K 4
#define MAX_GRAIN_COUNT 100000
#define FILE_NAME "Experiment-6.dat"

int** CreateMatrix();
void DeleteMatrix(int** matrix);
void SetMatrixToZero(int** matrix);
int AddGrain(int** matrix);
void ApplyInitialConditions(int** matrix);
int HandleAvalanches(int** matrix);
void ApplyBoundaryConditions(int** matrix);
void RecordAvalancheSize(map<int, int>& avalancheRecord, int size);
void RecordTimeStructure(map<int, int>& timeRecord, int iteration, int avalancheSize);
void OutputToFile(int** matrix, map<int, int>& avalancheRecord, map<int, int>& timeRecord);

int main()
{
	map<int, int> avalancheRecord;
	map<int, int> timeRecord;

	int** matrix = CreateMatrix();
	SetMatrixToZero(matrix);

	clock_t beginTime = clock();
	ApplyInitialConditions(matrix);
	std::cout << float(clock() - beginTime) / CLOCKS_PER_SEC << std::endl;	

	beginTime = clock();
	int numGrains = 0;
	int iterationNum = 0;
	while (numGrains < MAX_GRAIN_COUNT)
	{
		iterationNum += 1;
		numGrains += AddGrain(matrix);
		int avalancheSize = HandleAvalanches(matrix);
		RecordAvalancheSize(avalancheRecord, avalancheSize);
		RecordTimeStructure(timeRecord, iterationNum, avalancheSize);

		if (numGrains % 10000 == 0)
			std::cout << "Time taken so far for " << numGrains << ": " << float(clock() - beginTime) / CLOCKS_PER_SEC << std::endl;
	}

	OutputToFile(matrix, avalancheRecord, timeRecord);
	DeleteMatrix(matrix);
	return 0;
}

int** CreateMatrix()
{
	int** matrix = new int*[NUM_ROWS];
	for (int row = 0; row < NUM_ROWS; ++row)
		matrix[row] = new int[NUM_COLS];

	return matrix;
}

void DeleteMatrix(int** matrix)
{
	for (int row = 0; row < NUM_ROWS; ++row)
		delete matrix[row];

	delete matrix;
}

void SetMatrixToZero(int** matrix)
{
	for (int row = 0; row < NUM_ROWS; ++row)
	{
		for (int col = 0; col < NUM_COLS; ++col)
		{
			matrix[row][col] = 0;
		}
	}
}

void ApplyInitialConditions(int** matrix)
{
	for (int row = 1; row < NUM_ROWS - 1; ++row)
	{
		for (int col = 1; col < NUM_COLS - 1; ++col)
		{
			static int seed = 0;
			srand(seed++);
			matrix[row][col] = rand() % (K * 20) + (K * 10);
		}
	}

	HandleAvalanches(matrix);
}

int AddGrain(int** matrix)
{
	static int seed = 0;
	srand(seed++);

	int grainsAdded = 0;

	for (int i = 0; i < 1; ++i)
	{
		int row = rand() % (NUM_ROWS - 2) + 1;
		int col = rand() % (NUM_ROWS - 2) + 1;
		matrix[row][col] += 1;
		grainsAdded += 1;
	}

	return grainsAdded;
}

int HandleAvalanches(int** matrix)
{
	int avalancheSize = 0;
	bool recheckMatrix;
	do
	{
		recheckMatrix = false;

		for (int row = 0; row < NUM_ROWS; ++row)
		{
			for (int col = 0; col < NUM_COLS; ++col)
			{
				if (matrix[row][col] >= K)
				{
					matrix[row][col] -= 4;
					matrix[row + 1][col] += 1;
					matrix[row - 1][col] += 1;
					matrix[row][col + 1] += 1;
					matrix[row][col - 1] += 1;

					avalancheSize += 1;
					recheckMatrix = true;
				}
			}
		}
		ApplyBoundaryConditions(matrix);
	} while (recheckMatrix);

	return avalancheSize;
}

void ApplyBoundaryConditions(int** matrix)
{
	for (int row = 0; row < NUM_ROWS; ++row)
	{
		for (int col = 0; col < NUM_COLS; ++col)
		{
			if (row == 0 || row == NUM_ROWS - 1 || col == 0 || col == NUM_COLS - 1)
				matrix[row][col] = 0;
		}
	}
}

void RecordAvalancheSize(map<int, int>& avalancheRecord, int size)
{
	if (size == 0)
		return;

	map<int, int>::iterator it = avalancheRecord.find(size);
	if (it != avalancheRecord.end())
		it->second++;
	else
		avalancheRecord.insert(std::pair<int, int>(size, 1));
}

void RecordTimeStructure(map<int, int>& timeRecord, int iteration, int avalancheSize)
{
	timeRecord.insert(std::pair<int, int>(iteration, avalancheSize));
}

void OutputToFile(int** matrix, map<int, int>& avalancheRecord, map<int, int>& timeRecord)
{
	std::ofstream file(FILE_NAME);

	// Output Matrix Data
	file << NUM_ROWS << "\t" << NUM_COLS << "\n";

	for (int row = 0; row < NUM_ROWS; row++)
	{
		for (int col = 0; col < NUM_COLS; col++)
		{
			file << matrix[row][col] << "\t";
		}
		file << "\n";
	}

	// Output Avalanche Record Data
	file << avalancheRecord.size() << "\n";
	for (map<int, int>::iterator it = avalancheRecord.begin(); it != avalancheRecord.end(); ++it)
	{
		file << it->first << "\t" << it->second << "\n";
	}

	// Output Time Record Data
	file << timeRecord.size() << "\n";
	for (map<int, int>::iterator it = timeRecord.begin(); it != timeRecord.end(); ++it)
	{
		file << it->first << "\t" << it->second << "\n";
	}

	file.close();
}
