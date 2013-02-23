import re
# Slightly modified from Stack Overflow
parsePattern = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
class rawJob:
	'''This is a class for interacting directly with the data provided
	by the competition csv file'''
	def __init__(self, rawString):
		values = [string.strip() for string in parsePattern.split(rawString)]
		# Clean up since I don't know regex well enough
		values = [val for val in values if val != ',' and val != ' ' and val != '']
		for i,value in enumerate(values):
			if value == ',,':
				values[i] = None
		categories = ["id", "title", "description", "rawLocation", "normalizedLocation",
						"contractType", "contractTime", "company", "category",
						"salaryRaw", "salaryNormalized","sourceName"]
		self.data = dict(zip(categories, values))
		
