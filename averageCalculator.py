import csv
from rawJob import rawJob
from testRawJob import TestRawJob
from string import Template

def parseAverages(filePath):
	averages = {}
	with open(filePath, 'rb') as fieldAverages:
		reader = csv.reader(fieldAverages, delimiter = ",")
		for row in reader:
			averages[row[0]] = float(row[1])
	return averages

def multipleAverages(inputPath, outputPath, averages, fields):
	results = {}
	means = []
	for average in averages:
		mean = 0
		for entry in average.keys():
			mean += float(average[entry])/len(average)
		means.append(mean)
	with open(inputPath, 'rb') as rawData:
		reader = csv.reader(rawData, delimiter=",")
		allJobs = [TestRawJob(row) for row in reader]
		for job in allJobs:
			value = 0
			for i in range(0,len(averages)):
				if job.data[fields[i]] in averages[i].keys():
					value += float(averages[i][job.data[fields[i]]])/len(averages)
				else:
					print "missed something: " + fields[i] + ": " + job.data[fields[i]]
					value += means[i]
			results[job.data["Id"]] = value
	with open(outputPath, 'w') as dataDump:
		form = Template('$Id,$Value\n')
		for Id in results.keys():
			dataDump.write(form.substitute(Id = Id, Value = results[Id]))
					
def trainAverages(dataFile, averages, fields, averagePaths, changeRatio = 3./5):
	'''Average adjustment will be done in reference to one
	set of averages. That set of averages will be held constant
	and the other averages will be adjusted around it. The set
	of averages being held constant should be the first entry
	in fields. changeRatio is the portion of the error in each
	comparison you'd like to correct for'''
	with open(dataFile) as rawData:
		reader = csv.reader(rawData, delimiter=",")
		for row in reader:
			job = rawJob(row)
			averagesIncrement(job, averages, fields, changeRatio)
	for i in range(0,len(averages)):
		dumpAverageToFile(averages[i], averagePaths[i])
				
def averagesIncrement(job, averages, fields, changeRatio):
	imaginedSalary = 0.0
	individualChange = changeRatio/(len(fields))
	realSalary = float(job.data["salaryNormalized"])
	for i in range(0,len(fields)):
		jobValue = job.data[fields[i]].lower()
		if jobValue in averages[i].keys():
			value = float(averages[i][jobValue])
		else:
			value = salary
		imaginedSalary += value
	incrementValue = ((len(fields)*realSalary) - imaginedSalary)*individualChange
	for j in range (0, len(fields)):
		averages[j][job.data[fields[j]]] += incrementValue
	
def dumpAverageToFile(average, averagePath):
	with open(averagePath, 'w') as dataDump:
		for key in average.keys():
			form = Template('"$key",$value\n')
			dataDump.write(form.substitute(key=key, value = average[key]))
			
categoryPath = "averages/totalTrained/categoryAverages.csv"
companyPath = "averages/totalTrained/companyAverages.csv"
locationPath = "averages/totalTrained/locationAverages.csv"

categoryAverage = parseAverages(categoryPath)
companyAverage = parseAverages(companyPath)
locationAverage = parseAverages(locationPath)

averages = [categoryAverage, companyAverage, locationAverage]
fields = ["Category", "Company", "Normalized Location"]
averagePaths = [categoryPath, companyPath, locationPath]

#trainAverages("../data/Train_rev1.csv", averages, fields, averagePaths)
multipleAverages("../data/Valid_rev1.csv", "attempts/totalTrained.csv", averages, fields)
				
