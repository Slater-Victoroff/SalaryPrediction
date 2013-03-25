from salaryProbabilityReader import SalaryDistribution
from word import Word
from wordPair import WordPair
from Job import Job
from rawJob import rawJob

import csv
import operator
import math

class MoneyMaker:
	
	def __init__(self, trainingDataPath, salaryProbabilityPath, distributionGranularity, 
					dataGranularity, grammar, dropOffWidth = 0, stepDown = 0,
					increment = 5.0):
		self.salaryData = SalaryDistribution(salaryProbabilityPath, distributionGranularity)
		self.salaryData.parse()
		self.trainingDataPath = trainingDataPath
		self.dataGranularity = dataGranularity
		self.stochasticGrammar = grammar
		#print self.stochasticGrammar.wordData['surrey'].values[8000]
		#print self.stochasticGrammar.wordData['limited'].values[8000]
		#print self.stochasticGrammar.wordData['experience'].values[8000]
		#self.stochasticGrammar.wordData['surrey'].increment(8250, 0, 0)
		#self.stochasticGrammar.wordData['experience'].increment(8250, 0, 0)
		#print self.stochasticGrammar.wordData['surrey'].values[8000]
		#print self.stochasticGrammar.wordData['limited'].values[8000]
		#print self.stochasticGrammar.wordData['experience'].values[8000]
		self.dropOffWidth = dropOffWidth
		self.stepDown = stepDown
		self.increment = increment
		dummy = Word("", self.dataGranularity)
		dummy.initializeNewValues(self.salaryData)
		self.initialValue = dummy.values
			
	def closestValue(self, value, values):
		'''Right now basically brute force, which I don't like, but
		the value dictionary should be fairly small, still this code is
		going to run a lot, so speeding this up would be good'''
		downIncrement = value - self.dataGranularity
		for entry in values:
			if entry <= value and entry >= downIncrement:
				return entry
		return None
		
	def addWordEncounter(self, word):
		if word not in self.stochasticGrammar.wordData:
			newWord = Word(word, self.dataGranularity)
			newWord.initializeValues(self.initialValue)
			self.stochasticGrammar.wordData[word] = newWord
			return True
		return False
			
	def addWordPairEncounter(self, wordPair):
		'''wordPair should be a tuple of word1, word2'''
		if wordPair not in self.stochasticGrammar.wordPairData:
			newWordPair = WordPair(wordPair[0], wordPair[1], self.dataGranularity)
			newWordPair.initializeValues(self.initialValue)
			self.stochasticGrammar.wordPairData[wordPair] = newWordPair
			return True
		return False
			
	def jobIncrement(self, job, tolerance = 0.1):
		for word in job.wordList:
			self.addWordEncounter(word)
		for wordPair in job.wordPairList:
			self.addWordPairEncounter(wordPair)
		totalValue = self.expectedValue(job)
		maxLikelihood = max(totalValue.iteritems(), key=operator.itemgetter(1))[0]
		currentValue = totalValue[maxLikelihood]
		valueOfTruth = totalValue[self.closestValue(float(job.salary), self.initialValue)]
		difference = currentValue - valueOfTruth
		if difference > tolerance:
			individualChange = difference/float((len(job.wordList)+len(job.wordPairList)))
			print "Difference: "
			change = abs(job.salary - maxLikelihood)
			print change
		for wordTest in job.wordList:
			currentWord = self.stochasticGrammar.wordData[wordTest]
			currentWord.increment(job.salary, increment=0.5)
		for wordPairTest in job.wordPairList:
			currentWordPair = self.stochasticGrammar.wordPairData[wordPairTest]
			currentWordPair.increment(job.salary, increment=0.5)
		return abs(job.salary - maxLikelihood)
			
	def expectedValue(self, job):
		'''Assumes that every word and wordPair in the job is already
		accounted for in the grammar object'''
		value = {}
		for key in self.initialValue:
			term = 0.0
			try:
				for word in job.wordList:
					term += self.stochasticGrammar.wordData[word].values[key]
				for wordPair in job.wordPairList:
					term += self.stochasticGrammar.wordPairData[wordPair].values[key]
			except KeyError:
				pass
			value[key] = term
		return value
		
	def train(self):
		with open(self.trainingDataPath, 'rb') as trainingData:
			reader = csv.reader(trainingData, delimiter=",")
			counter = 0.
			miss = 0.
			maes = []
			for row in reader:
				counter += 1
				job = Job(rawJob(row))
				change = self.jobIncrement(job)
				miss += change
				print counter
				del job
				if counter%1000 == 0.0:
					maes.append(miss/counter)
					print maes
			print maes
		self.stochasticGrammar.dump()
		
class StochasticGrammar:
	def __init__(self, wordPath, wordPairPath):
		self.wordData = {}
		self.wordPairData = {}
		self.wordPath = wordPath
		self.wordPairPath = wordPairPath
	
	def parse(self):
		with open(self.wordPath, 'r') as wordSource:
			for line in wordSource:
				currentWord = Word.fromFileString(line)
				self.wordData[currentWord.text] = currentWord
		with open(self.wordPairPath, 'r') as wordPairSource:
			for line in wordPairSource:
				currentWordPair = WordPair.fromFileString(line)
				self.wordPairData[currentWordPair.text] = currentWordPair
				
	def dump(self):
		with open(self.wordPath, 'w') as wordDump:
			for entry in self.wordData.keys():
				wordDump.write(self.wordData[entry].configure())
		with open(self.wordPairPath, 'w') as wordPairDump:
			for entry in self.wordPairData.keys():
				wordPairDump.write(self.wordPairData[entry].configure())
				
		
	
