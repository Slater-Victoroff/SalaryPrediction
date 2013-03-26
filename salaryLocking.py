import json
import numpy

class SalaryLocker:
	
	def __init__(self, filePath):
		fileData = []
		with open(filePath, 'rb') as data:
			for line in data:
				fileData.append(line)
			self.salaries = numpy.array(json.loads(fileData[0]))
			self.frequencies = numpy.array(json.loads(fileData[1]))
			
	def unweightedSalaryLock(self, initialValue):
		index = (numpy.abs(self.salaries - initialValue)).argmin()
		return self.salaries[index]
		
	def weightedSalaryLock(self, initialValue):
		firstIndex = (numpy.abs(self.salaries - initialValue)).argmin()
		if (self.salaries[firstIndex] - initialValue) > 0:
			secondIndex = firstIndex-1
		else:
			secondIndex = firstIndex+1
		numerator = float(self.frequencies[firstIndex])
		denominator = float(self.frequencies[secondIndex])
		firstWeight = numerator/denominator
		matchRatio = float(numpy.abs(self.salaries[firstIndex]-initialValue))/float(numpy.abs(self.salaries[secondIndex]-initialValue))
		if matchRatio == 0:
			return self.salaries[firstIndex]
		if firstWeight/matchRatio >= 1:
			return self.salaries[firstIndex]
		else:
			return self.salaries[secondIndex]
		
def unweightedSalaryLock(initialSalary, filePath):
	with open(filePath, 'rb') as data:
		print len(data)
			
			

salaryFileLocation = "usefulData/Salaries.json"
locker = SalaryLocker(salaryFileLocation)
print locker.unweightedSalaryLock(15492)
print locker.weightedSalaryLock(15492)
