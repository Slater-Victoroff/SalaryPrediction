import csv
from rawJob import rawJob
from Job import Job
import cProfile

def parsedData(filePath):
	with open(filePath, 'rb') as rawData:
		reader = csv.reader(rawData, delimiter=",")
		allJobs = (Job(rawJob(row)) for row in reader)
	return allJobs

def averageLocationSalary(jobList):
	locationTicks = {}
	locationValues = {}
	for job in jobList:
		location = job.location
		if location in locationValues.keys():
			locationTicks[location] += 1
			locationValues[location] += (job.salary - locationValues[location])/locationTicks[location]
		else:
			locationTicks[location] = 1
			locationValues[location] = job.salary
	return locationValues
	
def runningAverageLocationSalary(filePath):
	locationTicks = {}
	locationValues = {}
	with open(filePath, 'rb') as rawData:
		reader = csv.reader(rawData, delimiter=",")
		for row in reader:
			job = Job(rawJob(row))
			location = job.location
			if location in locationValues.keys():
				locationTicks[location] += 1
				locationValues[location] += (job.salary - locationValues[location])/locationTicks[location]
			else:
				locationTicks[location] = 1
				locationValues[location] = job.salary
			del job
	return locationValues
	
jobList = parsedData("../data/Train_rev1.csv")
print averageLocationSalary(jobList)
#print runningAverageLocationSalary("../data/Train_rev1.csv")
