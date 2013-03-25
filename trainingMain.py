from training import MoneyMaker, StochasticGrammar
import cProfile
import atexit

trainingData = "../data/Train_rev1.csv"
salaryProbability = "usefulData/50GrainedFrequencies.csv"
distributionGranularity = 50
dataGranularity = 1475

grammar = StochasticGrammar("usefulData/2000GrainedWordData.txt", "usefulData/2000GrainedWordPairData.txt")
try:
	grammar.parse()
except NameError:
	pass

trainer = MoneyMaker(trainingData, salaryProbability, distributionGranularity, dataGranularity, grammar)
print "Starting Training"

trainer.train()
