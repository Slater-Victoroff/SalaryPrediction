from string import Template

class Word:
	def __init__(self, word, granularity, valuesFormat=Template("$key,$value")):
		self.text = word
		self.values = {}
		self.valueTemplate = valuesFormat
		self.granularity = granularity
		
	def initializeValues(self, salaryProbabilities, minimum=0, 
						maximum=200000, minimumFrequency=1.0):
		currentMinimum=minimum
		currentMaximum=self.granularity
		while currentMinimum<maximum:
			self.values[currentMinimum] = self.averageDictionaryValue(salaryProbabilities, currentMinimum, currentMaximum)
			if self.values[currentMinimum] == 0:
				self.values[currentMinimum] = minimumFrequency
			currentMinimum += self.granularity
			currentMaximum += self.granularity
				
	def averageDictionaryValue(self, dictionary, minimum, maximum):
		value = 0
		ticks = 0
		for key in dictionary.keys():
			if key<maximum and key>=minimum:
				value += dictionary[key]
				ticks += 1.0
		return value/ticks
		
	def format(self):
		form = "<" + self.text + " {"
		for entry in self.values.keys():
			form += self.valueTemplate.substitute(key=entry, value=self.values[entry])
		form +="}>"
		return form
		
	def increment(self, centerValue, dropOffWidth, stepDown):
		'''This method is made for training of the word model,
		Every time you find a particular word used, this method should
		be called on the word, there will be a similar method in the wordpair file.
		This method will increment the bin containing the centerValue by 1, and
		will look left and right n spaces where n is the dropOffWidth, and increment
		each bin in the dropOffWidth by stepDown^n. Every other bin will be equally
		stepped down to make sure that there is no net change of the word value. 
		Eventually this should be optimized so that every bin is changed so that 
		the reduction increases with difference from the centerValue'''
		stepUp = 1
		start = self.closestValue(centerValue) 
		self.values[start] += 1
		improved = [start]
		for i in range(1,dropOffWidth+1):
			addition = stepDown^(i)
			try:
				self.values[start-(i*self.granularity)] += addition
				stepUp += addition
				improved.append(start-(i*self.granularity))
			except KeyError:
				continue
			try:
				self.values[start+(i*self.granularity)] += addition
				stepUp += addition
				improved.append(start+(i*self.granularity))
			except KeyError:
				continue
		toReduce = []
		for entry in self.values.keys():
			if entry not in improved:
				toReduce.append(entry)
		stepDown = stepUp/len(toReduce)
		for confirmedReduction in toReduce:
			self.values[confirmedReduction] -= stepDown
	
	def closestValue(self, value):
		'''Right now basically brute force, which I don't like, but
		the value dictionary should be fairly small, still this code is
		going to run a lot, so speeding this up would be good'''
		downIncrement = value - self.granularity
		for entry in self.values:
			if entry <= value and entry >= downIncrement:
				return entry
		return None
		
		
