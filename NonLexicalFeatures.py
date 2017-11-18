import json

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def getAverageUpspeakEmailLength(emailCorpus): #will get the length of the body of emails in a given email corpus. Length is in terms of word count.
    emailCounter = 0
    lengthCounter = 0
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        
        for elem in emails:
            if (elem.get("to") == "Jeb Bush"): #if the email is to Jeb
                bodyText = elem.get("body")
                wordTokens = word_tokenize(bodyText) #returns list of word tokens in the bodyText
                wordCount = len(wordTokens)
                lengthCounter = lengthCounter + wordCount
                emailCounter += 1
        
        averageEmailLength = lengthCounter/emailCounter
        
        return averageEmailLength
    
def getAverageDownspeakEmailLength(emailCorpus): #length of average emails from Jeb
    emailCounter = 0
    lengthCounter = 0
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        
        for elem in emails:
            if (elem.get("from") == "Jeb Bush"): #if the email is from Jeb
                bodyText = elem.get("body")
                wordTokens = word_tokenize(bodyText) #returns list of word tokens in the bodyText
                wordCount = len(wordTokens)
                lengthCounter = lengthCounter + wordCount
                emailCounter += 1
        
        averageEmailLength = lengthCounter/emailCounter
        
        return averageEmailLength


def getAverageUpspeakSentenceLength(emailCorpus): #length of average sentence in emails to Jeb.
    sentCounter = 0
    totalLength = 0
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        

        for elem in emails:
            if (elem.get("to") == "Jeb Bush"): #if the email is to Jeb
                bodyText = elem.get("body")
                sentTokens = sent_tokenize(bodyText)
                for sentence in sentTokens:
                    totalLength = totalLength + len(word_tokenize(sentence))
                    sentCounter += 1
        
        averageSentenceLength = totalLength/sentCounter
        
        return averageSentenceLength
    
def getAverageDownspeakSentenceLength(emailCorpus): #length of average sentence in emails from Jeb
    sentCounter = 0
    totalLength = 0
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        

        for elem in emails:
            if (elem.get("from") == "Jeb Bush"): #if the email is from Jeb
                bodyText = elem.get("body")
                sentTokens = sent_tokenize(bodyText)
                for sentence in sentTokens:
                    totalLength = totalLength + len(word_tokenize(sentence))
                    sentCounter += 1
        
        averageSentenceLength = totalLength/sentCounter
        
        return averageSentenceLength



def getMaxUpspeakSentenceLength(emailCorpus): #Returns maximum length of a sentence which is upspeak across the corpus.
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        maxSentLength = 0
        for elem in emails:
            if (elem.get("to") == "Jeb Bush"): #if the email is to Jeb
                bodyText = elem.get("body")
                sentTokens = sent_tokenize(bodyText) #returns list of sentence tokens in the bodyText
                for sentence in sentTokens:
                    if len(word_tokenize(sentence)) > maxSentLength:
                        maxSentLength = len(word_tokenize(sentence))
        
        return maxSentLength
    
def getMinUpspeakSentenceLength(emailCorpus): #Returns minimum length of a sentence which is upspeak across the corpus.
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        minSentLength = 10000000
        for elem in emails:
            if (elem.get("to") == "Jeb Bush"): #if the email is to Jeb
                bodyText = elem.get("body")
                sentTokens = sent_tokenize(bodyText) #returns list of sentence tokens in the bodyText
                for sentence in sentTokens:
                    if len(word_tokenize(sentence)) < minSentLength:
                        minSentLength = len(word_tokenize(sentence))
        
        return minSentLength

def getMaxDownspeakSentenceLength(emailCorpus): #Returns maximum length of a sentence which is downspeak across the corpus.
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        maxSentLength = 0
        for elem in emails:
            if (elem.get("from") == "Jeb Bush"): #if the email is to Jeb
                bodyText = elem.get("body")
                sentTokens = sent_tokenize(bodyText) #returns list of sentence tokens in the bodyText
                for sentence in sentTokens:
                    if len(word_tokenize(sentence)) > maxSentLength:
                        maxSentLength = len(word_tokenize(sentence))
        
        return maxSentLength
    
def getMinDownspeakSentenceLength(emailCorpus):#Returns minimum length of a sentence which is downspeak across the corpus.
    with open (emailCorpus) as json_data:
        emails = json.load(json_data) #opens our email corpus, which is a list of emails bodies.
        minSentLength = 10000000
        for elem in emails:
            if (elem.get("from") == "Jeb Bush"): #if the email is to Jeb
                bodyText = elem.get("body")
                sentTokens = sent_tokenize(bodyText) #returns list of sentence tokens in the bodyText
                for sentence in sentTokens:
                    if len(word_tokenize(sentence)) < minSentLength:
                        minSentLength = len(word_tokenize(sentence))
        
        return minSentLength



    
print (str(getAverageUpspeakEmailLength("exampleCorpus.json")))
print (str(getAverageDownspeakEmailLength("exampleCorpus.json")))  
print(str(getMinDownspeakSentenceLength("exampleCorpus.json")))
print(str(getAverageDownspeakSentenceLength("exampleCorpus.json")))      
print(str(getAverageUpspeakSentenceLength("exampleCorpus.json")))      