import csv
from rawJob import rawJob
from Job import Job
import cProfile
from string import Template

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
	
runningAverage("../data/Train_rev1.csv", "company", "averages/companyAverages.csv")
