from word import Word
from wordPair import WordPair
import re

class Job:
	'''This class should be similar to the rawJob, but replacing the
	raw data fields with ones we feel to be more useful for the actual
	prediction, the title and description fields at least should
	be replaced by lists of words and wordpairs'''
	def __init__(self, rawJob, wordPattern = r'^([a-zA-Z\']+)$', filteredCharacters = "'"):
		'''Just storing basic information for now'''
		self.wordPattern = wordPattern
		self.filteredCharacters = filteredCharacters
		self.titleWords = self.cleanString(rawJob.data["title"])
		self.titleWordPairs = self.wordsToWordPairs(self.titleWords)
		self.descriptionWords = self.cleanString(rawJob.data["description"])
		self.descriptionWordPairs = self.wordsToWordPairs(self.descriptionWords)
		self.salary = float(rawJob.data["salaryNormalized"])
		self.location = rawJob.data["normalizedLocation"]
		self.company = rawJob.data["company"]

	def cleanString(self, string):
		'''Takes a list, parses it down to words according to the word pattern,
		then removes the characters in filteredCharacters. Returns the string
		as a list of words'''
		return [word.replace(self.filteredCharacters, "") for word in
						string.lower().split(" ") if re.match(self.wordPattern, word)]	
						
	def wordsToWordPairs(self, words):
		wordPairs = [WordPair(words[i-1], words[i]) for i in range(1,len(words))]
		return wordPairs

