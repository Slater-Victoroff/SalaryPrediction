class TestRawJob:
	
	def __init__(self, parsedRow):
		values = [string.strip().lower() for string in parsedRow]
		keys = ["Id", "Title", "Description", "Raw Location", "Normalized Location",
				"Contract Type", "Contract Time", "Company", "Category", "Source"]
		self.data = dict(zip(keys, values))
