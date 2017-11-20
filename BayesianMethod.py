#import simplebayes
import EmailProcessor
import json
import sys
import cProfile
import _thread as thread
# import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from nltk import sent_tokenize
from nltk import tokenize


#bayes = simplebayes.SimpleBayes()

# def bayesianLearn(emailCorpus): #pass in email corpus filename as string
# 	with open(emailCorpus) as json_data:
# 		emails = json.load(json_data)
# 		for email in emails:
# 			if (email.get("to") == "Jeb Bush"):#if goes to Jeb Bush, then upspeak.
# 				 sentences = sent_tokenize(email.get("body")) #get the body text and tokenize it into sentences.
# 				 for sentence in sentences:
# 				 	#bayes.train("upspeak", sentence)
# 			elif (email.get("from") == "Jeb Bush"): #if from Jeb Bush, downspeak
# 				sentences = sent_tokenize(email.get("body"))
# 				for sentence in sentences:
# 					#bayes.train("downspeak", sentence)

def bayesianTrain():
	for type in ['Upspeak', 'Downspeak']:
		with open('models/bayesian' + type + 'TrainingCorpus.json', 'r') as fp:
			trainingData = json.load(fp)
			for emailDict in trainingData:
				sentences = tokenize.sent_tokenize(emailDict['body'])
				for sentence in sentences:
					print(sentence)
					#bayes.train(type.lower(), sentence)

	for type in ['Upspeak', 'Downspeak']:
		with open('models/bayesian' + type + 'TestingCorpus.json', 'r') as fp:
			testData = json.load(fp)
			for emailDict in testData:
				sentences = tokenize.sent_tokenize(emailDict['body'])
				for sentence in sentences:
					print(sentence)
					#print(bayes.score(sentence))



def bayesianUpspeakAnalysis(sentence):
	print("bayes score for this sentence is " + bayes.score(sentence))

def main():
	# makeFromScratch = False;
	makeFromScratch = True;

	if makeFromScratch:
		cpu_count =  multiprocessing.cpu_count()
		# cpu_count = 16
		pool = multiprocessing.Pool( cpu_count )
		tasks = []
		tNum = 0
		max_t = cpu_count
		while tNum < max_t:
			tNum += 1
			tasks.append( (str(tNum), tNum, cpu_count) )
		results = []
		for t in tasks:
			results.append( pool.apply_async( EmailProcessor.getBayesianSetBalanced, t ) )

		r = []
		for result in results:
			r.append(result.get())

		fromJebTraining = []
		toJebTraining = []
		fromJebTest = []
		toJebTest = []

		for result in r:
			for i in range(4):
				if i == 0:
					fromJebTraining.append(result[i])
				elif i == 1:
					toJebTraining.append(result[i])
				elif i == 2:
					fromJebTest.append(result[i])
				elif i == 3:
					toJebTest.append(result[i])

 		# upspeakUnigramModel = mergeGrams(toUnigrams)
		# upspeakBigramModel = mergeGrams(toBigrams)
		# downspeakUnigramModel = mergeGrams(fromUnigrams)
		# downspeakBigramModel = mergeGrams(fromBigrams)

		downspeakTrainingCorpus = [item for sublist in fromJebTraining for item in sublist]
		upspeakTrainingCorpus = [item for sublist in toJebTraining for item in sublist]

		downspeakTestingCorpus = [item for sublist in fromJebTest for item in sublist]
		upspeakTestingCorpus = [item for sublist in toJebTest for item in sublist]

		with open('models/bayesianDownspeakTrainingCorpus.json', 'w') as fp:
			json.dump(downspeakTrainingCorpus, fp, indent = 4)
		with open('models/bayesianUpspeakTrainingCorpus.json', 'w') as fp:
			json.dump(upspeakTrainingCorpus, fp, indent = 4)
		with open('models/bayesianDownspeakTestingCorpus.json', 'w') as fp:
			json.dump(downspeakTestingCorpus, fp, indent = 4)
		with open('models/bayesianUpspeakTestingCorpus.json', 'w') as fp:
			json.dump(upspeakTestingCorpus, fp, indent = 4)

		bayesianTrain()

if __name__ == '__main__':
	main()
