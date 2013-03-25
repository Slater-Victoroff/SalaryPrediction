from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer,HashingVectorizer
from sklearn import linear_model
import csv
from rawJob import rawJob
import numpy as np
from time import time
import os
import matplotlib.pyplot as plt
from itertools import izip

def LoadData(filePath):
	reader = csv.reader(open(filePath))
	jobList = []
	for i,row in enumerate(reader):
		if i > 0:
			jobList.append(rawJob(row))
	return jobList

def getTargets(data,start,end):
	targets = []
	for i in xrange(start,end):
		job = jobData[i].data
		targets.append(np.log(float(job['salaryNormalized'])))
	return np.array(targets)

def getTests(data,start,end):
	targets = []
	tests = []
	for i in xrange(start,end):
		job = data[i].data
		tests.append(job['title'] + ' ' + job['description'])
	tests = vect.transform(np.array(tests))
	return tests

t0 = time()
# os.system("taskset -p 0xff %d" % os.getpid())
jobData = LoadData('Train_rev1.csv')
trainNum = 230000
testNum = 7500
titles = []
sals = []
compHash = {}
locHash = {}
for i in xrange(1,trainNum):
	job = jobData[i].data
	titles.append(job['title'] + ' ' + job['description'])
	sals.append(np.log(float(job['salaryNormalized'])))

vect = TfidfVectorizer(min_df=1,ngram_range=(1,2))
X = vect.fit_transform(np.array(titles))

print "done in %fs" % (time() - t0)
print "n_samples: %d, n_features: %d" % X.shape

# Alpha of 0.08 is best so far.
# Sweep alphas
alphas = np.logspace(-2,0,20)
for alpha in alphas:
	rr = linear_model.Ridge(alpha = alpha)
	print 'fitting'
	rr.fit(X,np.array(sals))
	tests = getTests(jobData,trainNum,trainNum+testNum)
	targets = np.exp(getTargets(jobData,trainNum,trainNum+testNum))
	print 'predicting'
	guesses = np.exp(rr.predict(tests))
	MAE = np.abs(targets-guesses).sum()/guesses.size
	print alpha,MAE

# Predict for validation
validData = LoadData('Valid_rev1.csv')
ids = [validData[i].data['id'] for i in xrange(len(validData))]
validTests = getTests(validData,0,len(validData))
predictions = np.exp(rr.predict(validTests))

# Write to CSV
with open('SKLearnPredictionsRidgeBiGrams.csv','wb') as fOut:
    out = csv.writer(fOut)
    for row in izip(ids,predictions):
        out.writerow(row)

print time()-t0
