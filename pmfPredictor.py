from rawJob import rawJob
from Job import Job
import csv
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.kde import gaussian_kde
from time import clock
import random
import nltk
from operator import itemgetter
import string
from itertools import izip

def LoadData(filePath):
	reader = csv.reader(open(filePath))
	jobList = []
	for i,row in enumerate(reader):
		if i > 0:
			jobList.append(rawJob(row))
	return jobList

def ToDict(l):
	lD = defaultdict(list)
	for key,value in l:
		lD[key].append(value)
	return lD

def Normalize(a):
	return np.array(a)/np.sum(a)

def Gaussian(vals,mu,sigma):
	num = np.exp(-(np.power(mu-vals,2)/(2*sigma*sigma)))
	denom = np.sqrt(2*np.pi)*sigma
	return num/denom

# Calcs bandwidth using Silverman's rule
def BWEstimator(data,salSTD):
	n = np.array(data).size
	std = np.std(data)
	if std == 0: # Deal with single data points
		std = salSTD
	return 1.06*std*np.power(n,(-1.0/5))

def shuffle(array):
    random.shuffle(array)
    return array

def CDF(pmf):
	cdf = np.cumsum(pmf)
	return cdf

# My implementation of gaussian KDE using uniform prior
def Update(hypo,x,data,salSTD):
	sigma = BWEstimator(data,salSTD)
	for datum in data:
		like = Gaussian(x,datum,sigma)
		hypo += like*100 #Bullshit value feel free to tweak
	hypo = Normalize(hypo)
	return hypo

# Using the scipy guassian KDE implementation
def SCIPYPMF(data,x):
	pdf = gaussian_kde(data)
	pmf = pdf(x)
	return Normalize(pmf)

def PMFD(d,x,bins,salSTD):
	for key in d:
		data = d[key]
		priors = Normalize(np.ones(bins))
		d[key] = Update(priors,x,data,salSTD)
	return d

def GetWordPMF(words,titles,bins):
	wordPMF = np.ones(bins)
	for word in words:
		pmf = titles[word]
		if pmf != []:
			wordPMF = wordPMF*pmf
	# wordPMF = Normalize(wordPMF)
	return wordPMF

def wordFreq(words):
	d = defaultdict(int)
	for word in words:
		d[word] += 1
	return d

def getWords(job,field,sal):
	jobWords = nltk.word_tokenize(job.data[field])
	jobWords = [word.translate(string.maketrans("",""), string.punctuation) for word in jobWords]
	return [(word,sal) for word in jobWords if word != '']

def getWordsOnly(job,field):
	jobWords = nltk.word_tokenize(job.data[field])
	jobWords = [word.translate(string.maketrans("",""), string.punctuation) for word in jobWords]
	return [word for word in jobWords if word != '']

def stats(a):
	mean = np.mean(np.exp(a))
	std = np.std(a)
	return mean,std

def processData(trainNum):
	salaries = []
	locations = []
	companies = []
	titles = []
	for i in xrange(1,trainNum):
		job = jobData[i]
		sal = np.log(float(job.data['salaryNormalized']))
		locations.append((job.data['normalizedLocation'],sal))
		companies.append((job.data['company'].lower(),sal))
		salaries.append(sal)
		titles.extend(getWords(job,'title',sal))
	locs = ToDict(locations)
	comps = ToDict(companies)
	titles = ToDict(titles)
	return salaries,locs,comps,titles

def trainData(sals,locs,comps,titles,salSTD,x):
	bins = x.size
	locs = PMFD(locs,x,bins,salSTD)
	comps = PMFD(comps,x,bins,salSTD)
	titles = PMFD(titles,x,bins,salSTD)
	return locs,comps,titles

def test(filePath,locs,comps,titles,mean,x):
	bins = x.size
	testData = LoadData(filePath)
	ids = []
	predictions = []
	for job in testData:
		jobID = job.data['id']
		guess = predict(job,locs,comps,titles,mean,x)
		predictions.append(guess)
		ids.append(jobID)
	with open('pmfPredict.csv','wb') as fOut:
	    out = csv.writer(fOut)
	    for row in izip(ids,predictions):
	        out.writerow(row)


def predict(job,locs,comps,titles,mean,x):
	bins = x.size
	locPMF = locs[job.data['normalizedLocation']]
	comPMF = comps[job.data['company'].lower()]
	words = getWordsOnly(job,'title')
	wordPMF = GetWordPMF(words,titles,bins)
	if all(pmf != [] for pmf in (locPMF,comPMF,wordPMF)):
		merged = Normalize(locPMF*comPMF*wordPMF)
		# Guess the mean of posterior distribution
		guess = np.exp(np.average(x,weights=merged))
	else:
		guess = mean
	return guess

start = clock()
jobData = LoadData('Train_rev1.csv')
trainNum = len(jobData)
bins = 200
print 'data loaded'
salaries,locs,comps,titles = processData(trainNum)
meanSal,salSTD = stats(salaries)
print 'data prepped'
x = np.linspace(min(salaries),max(salaries),bins)
locs,comps,titles = trainData(salaries,locs,comps,titles,salSTD,x)
print 'data trained'
test('Valid_rev1.csv',locs,comps,titles,meanSal,x)
print 'predicted'
