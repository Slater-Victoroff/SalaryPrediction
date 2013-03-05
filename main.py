import csv
from rawJob import rawJob
from Job import Job
import cProfile
from string import Template
from visual import *
from visual.graph import *
from salaryProbabilityReader import SalaryDistribution

def runningAverage(filePath, field, outputPath):
	fieldTicks = {}
	fieldValues = {}
	with open(filePath, 'rb') as rawData:
		reader = csv.reader(rawData, delimiter=",")
		for row in reader:
			testJob = rawJob(row)
			data = testJob.data[field].lower()
			if data in fieldValues.keys():
				fieldTicks[data] += 1
				fieldValues[data] += (float(testJob.data["salaryNormalized"]) - fieldValues[data])/fieldTicks[data]
			else:
				fieldTicks[data] = 1
				fieldValues[data] = float(testJob.data["salaryNormalized"])
			del testJob
	with open(outputPath, 'w') as dataDump:
		for datum in fieldValues.keys():
			dataDump.write(Template('"$key",$value\n').substitute(key=datum, value=fieldValues[datum]))
	
def plotFrequency(filePath, columnWidth):
	data = []
	with open(filePath, 'rb') as rawData:
		reader = csv.reader(rawData, delimiter=",")
		for row in reader:
			job = rawJob(row)
			number = float(job.data["salaryNormalized"])
			data.append(number)
			del job
	frequency = ghistogram(bins=arange(0,200000,columnWidth), color=color.red)
	frequency.plot(data=data)
	values = {}
	for position in frequency.vbars.pos:
		values[position[0]] = position[1]
	print values
	
def standardizeSalaryFiles(inputPath, outputPath, granularity):
	sweeper = SalaryDistribution(inputPath, granularity)
	sweeper.parse()
	sweeper.fileDump(outputPath)
	
#runningAverage("../data/Train_rev1.csv", "company", "averages/companyAverages.csv")

#set_printoptions(threshold='nan')
#plotFrequency("../data/Train_rev1.csv", 50)

#standardizeSalaryFiles("usefulData/50GrainedFrequencies.csv","usefulData/50GrainedFrequencies.csv",50)
