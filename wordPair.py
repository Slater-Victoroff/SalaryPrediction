from string import Template

class WordPair:
	def __init__(self, string1, string2, granularity=1475, values={}, 
					valuesFormat=Template("$key,$value;"), minimumFrequency=0.05):
		'''Should be initialized just from text, the wordpair will be
		disjointed from the words themselves'''
		self.text = (string1.lower(), string2.lower())
		self.values = values
		self.granularity = granularity
		self.valuesFormat = valuesFormat
		
	@classmethod
	def fromFileString(cls, fileLine):
		if len(fileLine) > 5:
			hashSplit = fileLine.split("#")
			string1 = hashSplit[1]
			string2 = hashSplit[2]
			valueStrings = fileLine[(fileLine.find("{")+1):-3].split(",")
			values = {}
			for value in valueStrings:
				split=value.split(": ")
				values[float(split[0])] = float(split[1])
			minimum = min(values)
			copy = values
			copy.pop(minimum)
			granularity = min(copy) - minimum
			return cls(string1, string2, granularity, values)
		else:
			raise NameError(fileLine)
			return None
			
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
		'''Definition of the format that word pairs will be stored in,
		redundantly covered between this method and the fromFileString
		class construction method'''
		pairForm = Template("<#$Word1#$Word2#")
		form = pairForm.substitute(Word1=self.text[0], Word2=self.text[1])
		form += str(self.values)
		form +=">\n"
		return form
		
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

	def increment(self, centerValue, increment = 1.0, steps = 4, stepDown = 0.75):
		'''Currently the same as the method in word, might change it eventually
		after more testing is done on the efficacy of this'''
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
		downIncrement = value - self.granularity
		for entry in self.values:
			if entry <= value and entry >= downIncrement:
				return entry
		return None
