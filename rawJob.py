class rawJob:
	'''This is a class for interacting directly with the data provided
	by the competition csv file'''
	def __init__(self, rawString):
		values = [string.strip() for string in rawString.split(",")]
		categories = ["id", "title", "description", "rawLocation", "normalizedLocation",
						"contractType", "contractTime", "company", "category",
						"salaryRaw", "salaryNormalized","sourceName"]
		self.data = dict(zip(categories, values))
		
