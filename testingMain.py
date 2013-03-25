import csv
from rawJob import rawJob
from Job import Job
import cProfile
from string import Template
from visual import *
from visual.graph import *
from salaryProbabilityReader import SalaryDistribution
from word import Word
from wordPair import WordPair
import cProfile

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
	
def wordTest(inputPath, distributionGranularity, wordGranularity, tempFile):
	salaryDictionary = SalaryDistribution(inputPath, distributionGranularity)
	salaryDictionary.parse()
	test1 = Word("Potato", wordGranularity)
	test1.initializeNewValues(salaryDictionary)
	test2 = Word("Celery", wordGranularity)
	test2.initializeNewValues(salaryDictionary)
	with open(tempFile, 'w') as dataDump:
		dataDump.write(test1.configure())
		dataDump.write(test2.configure())
	with open(tempFile, 'r') as reReading:
		wordList = []
		for line in reReading:
			try:
				wordList.append(Word.fromFileString(line))
			except NameError:
				continue
	print sum(wordList[0].values.values())
	print sum(wordList[1].values.values())
	wordList[0].increment(8250,increment = 147.25)
	print sum(wordList[0].values.values())
	print sum(wordList[1].values.values())
				
def wordPairTest(inputPath, distributionGranularity, wordPairGranularity, tempFile):
	salaryDictionary = SalaryDistribution(inputPath, distributionGranularity)
	salaryDictionary.parse()
	test = WordPair("Podium", "Stripe")
	test.initializeNewValues(salaryDictionary)
	with open(tempFile, 'w') as dataDump:
		dataDump.write(test.configure())
	with open(tempFile, 'r') as reReading:
		for line in reReading:
			try:
				check = WordPair.fromFileString(line)
				
				print check.configure()
				check.increment(11256, 3, 0.75)
				print ("~~~~~~~~")
				print check.configure()
			except NameError:
				continue
	
def jobTest(inputPath):
	jobList=[]
	with open(inputPath, 'rb') as rawData:
		reader = csv.reader(rawData, delimiter=",")
		for row in reader:
			jobList.append(Job(rawJob(row)))
	return jobList
	
#runningAverage("../data/Train_rev1.csv", "company", "averages/companyAverages.csv")

#set_printoptions(threshold='nan')
#plotFrequency("../data/Train_rev1.csv", 50)

#standardizeSalaryFiles("usefulData/50GrainedFrequencies.csv","usefulData/50GrainedFrequencies.csv",50)

'''This is a standard gambit of tests for the major data structures in this neck of the woods
if you change things, make sure that these methods still work and don't break,
might move to real pytests, but probably not'''
wordTest("usefulData/50GrainedFrequencies.csv", 50, 2000, "testDictionaryData.txt")
#wordPairTest("usefulData/50GrainedFrequencies.csv", 50, 2000, "testDictionaryData.txt")
#jobTest("../data/Train_rev1_sample.csv")
