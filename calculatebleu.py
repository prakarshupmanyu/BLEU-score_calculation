from __future__ import division
import sys, os, codecs, operator, math

def readInputFiles():
	if not len(sys.argv) == 3:
		print "Please provide 2 file names - one for training data and one for labels"
		sys.exit()
	candidateFile = sys.argv[1]
	referenceFile = sys.argv[2]

	if not os.path.isfile(candidateFile):
		print "Please check whether file file exists or not"
		sys.exit()

	candidateText = codecs.open(candidateFile, 'r', 'utf-8')
	candidateTextContent = candidateText.readlines()
	references = []
	if os.path.isfile(referenceFile):
		referenceText = codecs.open(referenceFile, 'r', 'utf-8')
		references.append(referenceText.readlines())
	elif os.path.isdir(referenceFile):
		for root, dirs, files in os.walk(referenceFile):
			for f in files:
				referenceText = codecs.open(os.path.join(root, f), 'r', 'utf-8')
				references.append(referenceText.readlines())
	return candidateTextContent, references

# Function to create a dictionary of unique n grams as keys and their number of occurances in a sentence as the value
def getNgramsCount(words, n):
	numNgrams = len(words) - n + 1
	ngramsCount = {}
	for i in range(numNgrams):
		ngram = ' '.join(words[i:i+n])
		if ngram in ngramsCount:
			ngramsCount[ngram] += 1
		else:
			ngramsCount[ngram] = 1
	return ngramsCount, numNgrams

# Function that will count the number of candidate n grams that also appear in the reference text (for a sentence)
def getClippedCount(ngCandCount, ngRefCounts):
	clippedCount = 0
	for ng in ngCandCount:
		maxRefCount = 0
		for ngRefCount in ngRefCounts:
			if ng in ngRefCount:
				maxRefCount = max(maxRefCount, ngRefCount[ng])
		clippedCount += min(maxRefCount, ngCandCount[ng])
	return clippedCount

def bestMatchLength(refLengths, numCandWords):
	minDiff = sys.maxint
	bestMatchLen = 0
	for refLen in refLengths:
		if abs(numCandWords - refLen) < minDiff:
			minDiff = abs(numCandWords - refLen)
			bestMatchLen = refLen
	return bestMatchLen

def calculateBrevPenalty(c, r):
	if c > r:
		return 1
	else:
		return math.exp(1 - (float(r)/c))

# Function to calculate modified n gram precision for a corpus.
def getModifiedNgramPrecicion(candText, references, n):
	clippedCount = 0
	numCandNgrams = 0
	c = 0
	r = 0
	for i in range(len(candText)):
		sCandWords = candText[i].lower().strip().split()
		ngCandCount, numNgrams = getNgramsCount(sCandWords, n)
		numCandNgrams += numNgrams
		c += len(sCandWords)
		refCounts = []
		refLengths = []
		for ref in references:
			sRefWords = ref[i].lower().strip().split()
			ngRefCount, numNgrams = getNgramsCount(sRefWords, n)
			refCounts.append(ngRefCount)
			refLengths.append(len(sRefWords))
		clippedCount += getClippedCount(ngCandCount, refCounts)
		r += bestMatchLength(refLengths, len(sCandWords))
	brevPenalty = calculateBrevPenalty(c, r)
	if clippedCount == 0:
		precision = 0
	else:
		precision = clippedCount/numCandNgrams
	return precision, brevPenalty

def getGeometricMean(precisions):
	return (reduce(operator.mul, precisions)) ** (1.0/len(precisions))

def getBlueScore(candText, references):
	modifiedNgramsPrecisions = []
	brevPenalty = 1
	for n in range(4):
		mngPrecision, brevPenalty = getModifiedNgramPrecicion(candText, references, n+1)
		modifiedNgramsPrecisions.append(mngPrecision)
	blueScore = getGeometricMean(modifiedNgramsPrecisions) * brevPenalty
	return blueScore

def outputScore(score):
	print score
	outputFile = open('bleu_out.txt', 'w')
	outputFile.write(str(score))
	outputFile.close()

def main():
	candText, references = readInputFiles()
	blueScore = getBlueScore(candText, references)
	outputScore(blueScore)

main()
