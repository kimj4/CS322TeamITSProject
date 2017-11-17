import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from pprint import pprint
import random
import copy
from decimal import *
import csv
import operator
import collections
import json
# import talon
# from talon.signature.bruteforce import extract_signature
# from talon import quotations
import math
import os


nltk.download('punkt')
print('\n\n\n')

def dataSplit(trainingRatio, sentences):
    ''' splits up the data into training and test sets where trainingRatio
        is some proportion '''
    # make a copy so that the original sentences is not changed
    testSet = copy.deepcopy(sentences)
    trainingSet = []
    numTrainingSentences = round(len(sentences) * trainingRatio)
    for i in range(0, numTrainingSentences):
        # select a random sentence, pop it from the testSet, push it on the trainingSet
        randSentence = random.choice(testSet)
        trainingSet.append(randSentence)
        testSet.remove(randSentence)
    return (trainingSet, testSet)

def createNgram(N, sentences):
    '''
    N -- 1 for unigram, 2 for bigram, ...
    sentences -- a list of sentences to create ngrams on ([sentence] for a single
               sentence)
    Returns a dictionary of ngrams and their counts of the form
        {'first ngram': 2, 'second ngram': 29, ...}
    '''
    # TODO: check if we should be passing in sentences as cleaned up sequences of words
    # sentences, testSet are lists of sentences

    nGrams = {}
    endOfGram = N - 1

    for sentence in sentences:
        if (N > 1):
            sentence = ('<s> ' * (N - 1)) + sentence + ' </s>'
        else:
            sentence = '<s> ' + sentence + ' </s>'
        sentenceList = sentence.split(' ')
        while endOfGram < (len(sentenceList)):
            s = ' '
            curNgram = sentenceList[endOfGram - N + 1: endOfGram + 1]
            curNgram = s.join(curNgram)
            if (curNgram in nGrams):
                nGrams[curNgram] += 1
            else:
                nGrams[curNgram] = 1
            endOfGram += 1
        endOfGram = N - 1
    return nGrams

def calculateMLE(sentence, N, trainingAndTestSets):
    '''
    calculates the minimum likelihood estimate on sample sentences for a model
    trained on the training set in trainingAndTestSets

    sentences -- sentence that needs the MLE
    N -- the N in N-gram
    trainingAndTestSets -- a tuple containing a division of the corpus
    '''
    # create the model on the training set
    trainingNGrams = createNgram(N, trainingAndTestSets[0])

    # create the counts for n-1
    trainingNMinusOneGrams = createNgram(N - 1, trainingAndTestSets[0])

    oneGram = createNgram(1, trainingAndTestSets[0])
    oneGramTotal = sum(oneGram.values())

    probabilityDict = {}
    for key, value in trainingNGrams.items():
        prevGram = " ".join(key.split(' ')[:-1])
        if  prevGram in trainingNMinusOneGrams:
            probabilityDict[key] = trainingNGrams[key] / trainingNMinusOneGrams[prevGram]


    # get the count to get the probability
    totalNGrams = sum(trainingNGrams.values())

    sentenceMLE = 1;
    testNGrams = createNgram(N, [sentence])
    for key, value in testNGrams.items():
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                sentenceMLE = sentenceMLE * (oneGram['<s>'] / oneGramTotal) * testNGrams[key]
            elif key in probabilityDict.keys():
                # print('n-gram found')
                sentenceMLE = sentenceMLE * probabilityDict[key] * testNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001
        else:
            if key in probabilityDict.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                sentenceMLE = sentenceMLE * probabilityDict[key] * testNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001

    return sentenceMLE


def calculatePerplexity(N, trainingAndTestSets):
    ''' trainingAndTestSets: (list of training sentences, list of test setences)
        Calculates the average perplexity of sentences in the test set'''

    gramDict = {}
    total1Grams = 0

    # first create the ngram models
    for i in range(1, N + 1):
        trainingGrams = createNgram(i, trainingAndTestSets[0])
        gramDict[str(i) + "gram"] = trainingGrams
        if (i == 1):
            # if we want to calculate the perplexity of unigrams, we need the
            #  total number of unigrams
            total1Grams = sum(gramDict['1gram'].values())


    # stores the perplexity of sentences so they can be averaged later
    sentencePerplexityList = []
    # so calculate perplexity for each sentence
    for sentence in trainingAndTestSets[1]:
        sentencePerplexityList.append(calculateSentencePerplexity(N, sentence, gramDict, total1Grams))
    perplexity = sum(sentencePerplexityList) / len(sentencePerplexityList)
    return perplexity

def calculateSentencePerplexity(N, sentence, gramDict, total1Grams):
    '''
    Calculates the perplexity for a single sentence

    N -- the N in N-grams
    sentence -- a string (which should be a sentence)
    gramDict -- a dictionary containing the training n-grams counts
    total1Grams -- number of unigrams for calculating perplexity with unigrams
    '''
    sentenceNgrams = createNgram(N, [sentence])
    sentenceProbability = 1

    for ngram, count in sentenceNgrams.items():
        if (N == 1):
            # unigram probability = this unigram count / all unigram count
            ngramProbability = count / total1Grams
        else:
            # ngram probability = this ngram count / this n-1gram count
            # make the n-1gram by popping off the last word in ngram
            prevGram = ngram.split(' ')[:-1]
            prevGram = ' '.join(prevGram)

            prevGramCount = 0
            if prevGram in gramDict[str(N - 1) + "gram"]:
                prevGramCount = gramDict[str(N - 1) + "gram"][prevGram]
            else:
                # special case for handling something like <s> <s> I
                #  just use the <s> count from unigrams
                if prevGram.split(' ')[-1] == "<s>":
                    prevGramCount = gramDict["1gram"]['<s>']

            # if there's no prevGramCount, there will be no ngram count because
            # that sequence of words never appears in the training set

            if ngram in gramDict[str(N) + "gram"]:
                trainingCount = gramDict[str(N) + "gram"][ngram]
                ngramProbability = trainingCount / prevGramCount
            else:
                # arbitary small probability if the ngram is not in the training set
                ngramProbability = 0.000001

        sentenceProbability = Decimal(sentenceProbability * Decimal(ngramProbability))
        sentencePerplexity = (1 / sentenceProbability) ** Decimal(1 / (len(sentence)))
    return sentencePerplexity

def _processEmail(email):
    '''
    processes email before sentence-tokenization. Does body extraction
    through talon (get rid of signature and email chain junk (theoretically))
    '''
    #talon.init() # this throws a warning. This package may be depreciated
    # reply = quotations.extract_from(email, 'text/plain')
    # reply = quotations.extract_from_plain(email)
    # text, signature = extract_signature(email)

    return text

def _processEmails(emailsList):
    ''' just does the email processing for a list of emailsList '''
    processedEmails = []
    for email in emailsList:
        processedEmails.append(_processEmail(email))
    return processedEmails

def _processSentences(sentencesList):
    ''' manipulates sentences to a format suitable for n-gram modeling
        remove unnecessary whitespace
        remove some punctuation

        sentencesList = a list of strings
    '''
    newSentences = []
    for s in sentencesList:
        # when removing, replace with a whitespace, and check later for double
            # white space

        # remove unnecessary whitespace
        newS = s.replace('\n', ' ')

        # remove some Symbols
        disallowedSymbols = '!@#$%^&*()_=+[]\{\}<>,/?\|`~:;'
        for sym  in disallowedSymbols:
            newS = newS.replace(sym, ' ')


        # remove end-of-sentence punctuation
        # TODO: consider cases like "what?!"
        if len(newS) > 0:
            if newS[-1] in '!?.':
                newS = newS[:-1]

        newS = newS.replace('  ', ' ')
        # lowercase all words
        newS = newS.lower()
        newSentences.append(newS)
    return newSentences

def divideEmailsBySender(jsonObj):
    ''' divide the json object into two, where one is for all emails sent by
        Jeb Bush and the other is all received '''
    fromJeb = []
    toJeb = []
    for e in jsonObj:
        if 'jeb' in  e['from'].lower():
            fromJeb.append(e)
        else:
            toJeb.append(e)
    return (fromJeb, toJeb)

def _mergeBodies(emails):
    bodies = []
    for e in emails:
        bodies.append(e['body'])
    return bodies

def prepareEmailsForNGram(emails):
    ''' takes in email json objects and outputs a list of processed sentences'''
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    # a list of bodies
    bodies = _mergeBodies(emails)

    #bodies = _processEmails(bodies)

    # a list of sentences contained in all bodies
    rawSentences = []
    for body in bodies:
        rawSentences.extend(sentence_splitter.tokenize(body))

    # a list of cleaned sentences contained in all BrowardTimes
    cleanedSentences = _processSentences(rawSentences)

    return cleanedSentences

def runAndGet(thread_name, thread_number, total_thread_count):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    # fp = open("exampleCorpus.json", 'r', encoding='UTF-8', errors='ignore')
    data = []

    num_files_to_include = 360
    start = 0
    num_threads = total_thread_count
    num_files_to_include = num_files_to_include // total_thread_count
    start = num_files_to_include * (thread_number - 1)



    cur_count = 0;
    directory_name = 'output'
    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            if int(filename.split('.')[0]) >= start:

                print(str(thread_name))
                input_file_name = directory_name + '/' +filename
                with open(input_file_name, 'r') as f:
                    tempdata = json.load(f)
                    data.extend(tempdata)
                cur_count += 1
        if cur_count == num_files_to_include:
            break
                # print(len(data))

    fromJeb, toJeb = divideEmailsBySender(data)

    # these are all json objects, need to merge their bodies.
    fromJebTraining, fromJebTest = dataSplit(.7, fromJeb)
    toJebTraining, toJebTest = dataSplit(.7, toJeb)

    # list of sentences that's ready for n-gram model creation
    fromJebTrainingCorpus = prepareEmailsForNGram(fromJebTraining)
    toJebTrainingCorpus = prepareEmailsForNGram(toJebTraining)

    # ngram models are created! (for now these are unigram counts)
    fromUnigram = createNgram(1, fromJebTrainingCorpus)
    toUnigram = createNgram(1, toJebTrainingCorpus)

    fromBigram = createNgram(2, fromJebTrainingCorpus)
    toBigram = createNgram(2, toJebTrainingCorpus)

    # with open('models/downspeakBigramModel.json', 'w') as fp:
    #     json.dump(fromBigram, fp)
    # with open('models/downspeakUnigramModel.json', 'w') as fp:
    #     json.dump(fromUnigram, fp)
    # with open('models/upspeakBigramModel.json', 'w') as fp:
    #     json.dump(toBigram, fp)
    # with open('models/upspeakUnigramModel.json', 'w') as fp:
    #     json.dump(toUnigram, fp)
    # should be able to calculate MLE or something here, but fromJebTest and
    #  toJebTest bodies need to be extracted

    #return (fromUnigram, toUnigram, from)
    print(str(thread_name) + ' is done!')
    return (fromUnigram, fromBigram, toUnigram, toBigram)

def getAllModels():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    # fp = open("exampleCorpus.json", 'r', encoding='UTF-8', errors='ignore')

    with open("emails.json", 'r') as f:
        data = json.load(f)

    fromJeb, toJeb = divideEmailsBySender(data)

    # these are all json objects, need to merge their bodies.
    fromJebTraining, fromJebTest = dataSplit(.7, fromJeb)
    toJebTraining, toJebTest = dataSplit(.7, toJeb)

    # list of sentences that's ready for n-gram model creation
    fromJebTrainingCorpus = prepareEmailsForNGram(fromJebTraining)
    toJebTrainingCorpus = prepareEmailsForNGram(toJebTraining)
    bigramModels = getNgramModels(2, fromJebTrainingCorpus, toJebTrainingCorpus)
    unigramModels = getNgramModels(1, fromJebTrainingCorpus, toJebTrainingCorpus)
    with open('models/downspeakBigramModel.json', 'w') as fp:
        json.dump(bigramModels[0], fp)
    with open('models/downspeakUnigramModel.json', 'w') as fp:
        json.dump(unigramModels[0], fp)
    with open('models/upspeakBigramModel.json', 'w') as fp:
        json.dump(bigramModels[1], fp)
    with open('models/upspeakUnigramModel.json', 'w') as fp:
        json.dump(unigramModels[1], fp)

def getNgramModels(N, fromJebTrainingCorpus, toJebTrainingCorpus):


    # ngram models are created! (for now these are unigram counts)
    fromNGram =  createNgram(N, fromJebTrainingCorpus)
    toNGram =  createNgram(N, toJebTrainingCorpus)

    # should be able to calculate MLE or something here, but fromJebTest and
    #  toJebTest bodies need to be extracted
    return (fromNGram, toNGram)

def main():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    # fp = open("exampleCorpus.json", 'r', encoding='UTF-8', errors='ignore')

    with open("emails.json", 'r') as f:
        data = json.load(f)

    fromJeb, toJeb = divideEmailsBySender(data)

    # these are all json objects, need to merge their bodies.
    fromJebTraining, fromJebTest = dataSplit(.7, fromJeb)
    toJebTraining, toJebTest = dataSplit(.7, toJeb)

    # list of sentences that's ready for n-gram model creation
    fromJebTrainingCorpus = prepareEmailsForNGram(fromJebTraining)
    toJebTrainingCorpus = prepareEmailsForNGram(toJebTraining)

    # ngram models are created! (for now these are unigram counts)
    fromNGram =  createNgram(1, fromJebTrainingCorpus)
    toNGram =  createNgram(1, toJebTrainingCorpus)

    # should be able to calculate MLE or something here, but fromJebTest and
    #  toJebTest bodies need to be extracted
    print("It worked")
    return (fromNGram, toNGram)



if __name__ == '__main__':
    main()

print('\n\n\n')
