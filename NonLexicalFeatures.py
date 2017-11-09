import json

from nltk.tokenize import word_tokenize

def getAverageUpspeakLength(emailCorpus): #will get the length of the body of emails in a given email corpus. Length is in terms of word count.
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
    
def getAverageDownspeakLength(emailCorpus): #length of average emails from Jeb
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
    
    
print (str(getAverageUpspeakLength("exampleCorpus.json")))
print (str(getAverageDownspeakLength("exampleCorpus.json")))        