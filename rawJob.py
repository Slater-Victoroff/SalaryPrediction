class rawJob:
	def __init__(self, rawString):
		values = [string.strip() for string in rawString.split(",")]
		categories = ["id", "title", "description", "rawLocation", "normalizedLocation",
						"contractType", "contractTime", "company", "category",
						"salaryRaw", "salaryNormalized","sourceName"]
		self.data = dict(zip(categories, values))
		
