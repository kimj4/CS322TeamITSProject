import json
import simplebayes
from nltk import sent_tokenize

bayes = simplebayes.SimpleBayes()

def bayesianLearn(emailCorpus): #pass in email corpus filename as string
	with open emailCorpus as json_data:
		emails = json.load(json_data)
		for email in emails:
			if (email.get("to") == "Jeb Bush"):#if goes to Jeb Bush, then upspeak.
				 sentences = sent_tokenize(email.get("body")) #get the body text and tokenize it into sentences.
				 for sentence in sentences:
				 	bayes.train("upspeak", sentence)
			elif (email.get("from") == "Jeb Bush"): #if from Jeb Bush, downspeak
				sentences = sent_tokenize(email.get("body"))
				for sentence in sentences:
					bayes.train("downspeak", sentence)

def bayesianUpspeakAnalysis(sentence):
	print "bayes score for this sentence is " + bayes.score(sentence)