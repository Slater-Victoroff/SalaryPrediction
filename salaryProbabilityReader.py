import csv
from string import Template

class SalaryDistribution:
	'''Basically just casts a salary file to a distribution
	of salaries in a hashmap form. The key should be the lower bound of 
	the range, and the value should be the frequency (in # of appearances).
	Every mapping should be lower bound inclusive, but upper bound exclusive'''
		
	def __init__(self, filePath, granularity, minimum=0, maximum=200000):
		self.rawData = {}
		self.cleanedData = {}
		self.inputPath = filePath
		self.granularity = granularity
		self.minimum = minimum
		self.maximum = maximum
			
	def averageDictionaryValue(self, dictionary, minimum, maximum):
		value = 0
		ticks = 0
		for key in dictionary.keys():
			if key<maximum and key>=minimum:
				value += dictionary[key]
				ticks += 1.0
		return value/ticks
		
	def parse(self):
		with open(self.inputPath, 'rb') as rawData:
			reader = csv.reader(rawData, delimiter=",")
			for row in reader:
				self.rawData[float(row[0])] = float(row[1])
		currentMin=self.minimum
		currentMax=self.granularity
		while currentMin<self.maximum:
			self.cleanedData[currentMin] = self.averageDictionaryValue(self.rawData, currentMin, currentMax)
			currentMin += self.granularity
			currentMax += self.granularity
			
	def fileDump(self, outputPath):
		with open(outputPath, 'w') as dataDump:
			form = Template('$key,$value\n')
			for entry in self.cleanedData.keys():
				dataDump.write(form.substitute(key=entry, value=self.cleanedData[entry]))
				
