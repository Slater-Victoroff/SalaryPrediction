class WordPair:
	def __init__(self, string1, string2):
		'''Should be initialized just from text, the wordpair will be
		disjointed from the words themselves'''
		self.word1 = string1.lower()
		self.word2 = string2.lower()
