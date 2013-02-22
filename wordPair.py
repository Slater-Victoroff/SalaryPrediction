class WordPair:
	def __init__(self, word1, word2):
		self.word1 = word1
		self.word2 = word2
		self.value = (word1.value + word2.value)/2.0
