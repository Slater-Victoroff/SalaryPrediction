from string import Template

class Word:
	def __init__(self, word, granularity, valuesFormat=Template("$key,$value;"), values={}):
		self.text = word.lower()
		self.values = values
		self.valueTemplate = valuesFormat
		self.granularity = granularity
		
	@classmethod
	def fromFileString(cls, fileLine):
		if len(fileLine) > 5:
			text = fileLine[1:fileLine.find(" ")]
			messyValues = fileLine[(fileLine.find("{")+1):-3]
			listOfKVPairs = messyValues.split(",")
			values = {}
			for pair in listOfKVPairs:
				if len(pair) > 1:
					terms = pair.split(": ")
					try:
						values[float(terms[0])] = float(terms[1])
					except IndexError:
						print pair
			minimum = min(values)
			copy = values
			copy.pop(minimum)
			granularity = min(copy) - minimum
			valueTemplate = Template("$key,$value;")
			return cls(text, granularity, valueTemplate, values)
		else:
			raise NameError("fileLine")
			return None
		
	def initializeNewValues(self, salaryProbabilities, minimum=0.0, 
						maximum=210000, minimumFrequency=0.05):
		currentMinimum=minimum
		currentMaximum=self.granularity
		while currentMinimum<maximum:
			self.values[currentMinimum] = self.averageDictionaryValue(salaryProbabilities.cleanedData, currentMinimum, currentMaximum)
			if self.values[currentMinimum] == 0:
				self.values[currentMinimum] = minimumFrequency
			currentMinimum += self.granularity
			currentMaximum += self.granularity
			
	def initializeValues(self, values):
		self.values = values
				
	def averageDictionaryValue(self, dictionary, minimum, maximum):
		value = 0
		ticks = 0
		for key in dictionary:
			if key<maximum and key>=minimum:
				value += dictionary[key]
				ticks += 1.0
		if ticks == 0:
			return 0
		return value/ticks
		
	def configure(self):
		form = "<" + self.text + " "
		form += str(self.values)
		form +=">\n"
		return form
		
	def increment(self, centerValue, increment = 1.0, steps = 4, stepDown = 0.75):
		'''Adds a total of increment to the bins within steps of the actual
		center value. Currently the falloff is stepdDown^(i^2)'''
		totalUp = 0.0
		steppedUp = []
		sortedValues = sorted(self.values.keys())
		center = self.closestValue(centerValue) 
		if center is None:
			print "Center Values Is:"
			print centerValue
			pass
		centerIndex = sortedValues.index(center)
		leftOffset = centerIndex
		leftSteps = min(leftOffset, steps)
		rightOffset = abs(centerIndex - len(sortedValues)-1)
		rightSteps = min(rightOffset,steps)
		for i in range(0,leftSteps):
			totalUp += (stepDown**((i+1)*(i+1)))
		for i in range(0,rightSteps):
			totalUp += (stepDown**((i+1)*(i+1)))
		centerStep = increment/totalUp
		self.values[center] += centerStep
		steppedUp.append(center)
		#Left step up
		for i in range(0,leftSteps):
			index = centerIndex - (i+1)
			step = totalUp*(stepDown**((i+1)*(i+1)))
			self.values[sortedValues[index]] += step
			steppedUp.append(sortedValues[index])
			
		#Right step up
		for i in range(0,rightSteps):
			index = centerIndex + (i+1)
			step = totalUp*(stepDown**((i+1)*(i+1)))
			self.values[sortedValues[index]] += step
			steppedUp.append(sortedValues[index])
		
		numberNotTouched = len(sortedValues) - len(steppedUp)
		decrement = totalUp/numberNotTouched	
		for entry in sortedValues:
			if entry not in steppedUp:
				self.values[entry] -= decrement
	
	def closestValue(self, value): 
		'''Right now basically brute force, which I don't like, but
		the value dictionary should be fairly small, still this code is
		going to run a lot, so speeding this up would be good'''
		downIncrement = value - self.granularity-1 
		#Added 1 to avoid edge cases
		for entry in self.values:
			if entry <= value and entry >= downIncrement:
				return entry
		return None
		
		
