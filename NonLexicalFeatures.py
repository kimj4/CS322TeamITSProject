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


###WEIGHTING METHODS EXPLANATION####
#The following two methods calculate weights for probabilities.
#There are two broad assumptions: Longer sentences are more likely to be upspeak, and upspeak sentences have higher average lengths than downspeak sentences.
#A sentence that is longer than the longest upspeak found in the corpus is automatically classified as upspeak.
#A sentence shorter than the shortest upspeak in the corpus is automatically classified as not-upspeak.
#A sentence longer than longest downspeak in corpus is automatically classified as not-downspeak.
#A sentence shorter than shortest downspeak in corpus is automatically classified as downspeak. 

#The weighting calculation itself assumes a distribution centered around the average length. A sentence that matches average length of upspeak or downspeak
#has a corresponding weight of 1. 
#For upspeak, as sentence length approaches the longest upspeak in the corpus, the weight grows to infinity.
#As sentence length approaches shortest upspeak length in the corpus, the weight shrinks linearly to 0.
#For downspeak, as sentence length approaches shortest downspeak in the corpus, weight grows to infinity.
#As sentence length approaches longest downspeak in the corpus, weight shrinks linearly to 0.

def sentenceWeighterUpspeak(sentence, ngramprobability):
    maxUpspeak = getMaxUpspeakSentenceLength(corpus) #FIX THIS- CORPUS IS JUST A PLACEHOLDER
    minUpspeak = getMinUpspeakSentenceLength(corpus)
   
    averageUpspeak = getAverageUpspeakSentenceLength(corpus)
    


    sentenceLength = len(word_tokenize(sentence)) #get length of whole sentence that you just input

    #first we calculate our upspeak weighting modifier
    upspeakWeight = 1
    #the further away to  the right (longer) from downspeak length, the more likely it's upspeak.

    if (sentenceLength > averageUpspeak) and (sentenceLength < maxUpspeak): #longer sentences are more likely to be upspeak
        upspeakWeight = maxUpspeak/(maxUpspeak - sentenceLength)
    #elif (sentenceLength > maxUpspeak):
     #   print("This sentence is almost certainly upspeak")
      #      return
    elif (sentenceLength < averageUpspeak) and (sentenceLength >= minUpspeak):
        upspeakWeight = (abs(sentenceLength-MinUpspeak))/averageUpspeak
    elif (sentenceLength < minUpspeak)
        print ("This sentence is almost certainly not upspeak")
            return

            

    #if sentence is not clearly one or other, return the weighted calculation
    ngramprobability = ngramprobability * upspeakWeight
    return ngramprobability

def sentenceWeighterDownspeak(sentence, ngramprobability):
    minDownspeak = getMinDownspeakSentenceLength(corpus)
    maxDownspeak = getMinDownspeakSentenceLength(corpus)
    averageDownspeak = getAverageDownspeakSentenceLength(corpus)
    #now we calculate downspeak weighting

    downspeakWeight = 1
    if (sentenceLength > averageDownspeak) and (sentenceLength < maxDownspeak): #longer sentences are less likely to be downspeak
        downspeakWeight = (maxDownspeak-sentenceLength)/maxDownspeak
    elif (sentenceLength < averageDownspeak) and (sentenceLength < minDownspeak):
        downspeakWeight = averageDownspeak/(sentenceLength - minDownspeak)
    elif (sentenceLength > maxDownspeak): #sentence is almost certainly not downspeak
        print("this sentence is almost certainly not downspeak")
        return
    #add a case for less than minimum downspeak? Then the output may just be "too little information to tell either way..."

    ngramprobability = ngramprobability * downspeakWeight
    return ngramprobability

    
print (str(getAverageUpspeakEmailLength("exampleCorpus.json")))
print (str(getAverageDownspeakEmailLength("exampleCorpus.json")))  
print(str(getMinDownspeakSentenceLength("exampleCorpus.json")))
print(str(getAverageDownspeakSentenceLength("exampleCorpus.json")))      
print(str(getAverageUpspeakSentenceLength("exampleCorpus.json")))      