'''
EmailProcessor.py
Does everything that involves ngram analysis.
'''

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
    newTestSet = []
    numTrainingSentences = round(len(sentences) * trainingRatio)
    for i in range(0, numTrainingSentences):
        # select a random sentence, pop it from the testSet, push it on the trainingSet
        randSentence = random.choice(testSet)
        trainingSet.append(randSentence.copy())
        testSet.remove(randSentence)
    for i in range(0, len(testSet)):
        newTestSet.append(dict(testSet[i].copy()))
    return (trainingSet, newTestSet)

def createNgram(N, sentences):
    '''
    N -- 1 for unigram, 2 for bigram, ...
    sentences -- a list of sentences to create ngrams on ([sentence] for a single
               sentence)
    Returns a dictionary of ngrams and their counts of the form
        {'first ngram': 2, 'second ngram': 29, ...}
    '''
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

def getBayesianSetBalanced(thread_name, thread_number, total_thread_count):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    data = []

    num_files_to_include = 625
    start = 0
    num_threads = total_thread_count
    num_files_to_include = math.ceil((1.0 * num_files_to_include) / total_thread_count)
    start = num_files_to_include * (thread_number - 1)

    cur_count = 0;
    directory_name = 'output'
    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            if int(filename.split('.')[0]) >= start:
                input_file_name = directory_name + '/' +filename
                with open(input_file_name, 'r') as f:
                    tempdata = json.load(f)
                    data.extend(tempdata)
                cur_count += 1
        if cur_count == num_files_to_include:
            break
                # print(len(data))

    fromJeb, toJeb = divideEmailsBySender(data)
    toJeb = toJeb[:len(fromJeb)]


    # these are all json objects, need to merge their bodies.
    fromJebTraining, fromJebTest = dataSplit(.7, fromJeb)
    toJebTraining, toJebTest = dataSplit(.7, toJeb)
    return (fromJebTraining, toJebTraining, fromJebTest, toJebTest)

def getNgramsBalanced(thread_name, thread_number, total_thread_count):
    '''
    Build sets of ngrams but use only as many nonjeb emails as there are jeb
    emails.
    '''
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    data = []

    num_files_to_include = 625
    start = 0
    num_threads = total_thread_count
    num_files_to_include = math.ceil((1.0 * num_files_to_include) / total_thread_count)
    start = num_files_to_include * (thread_number - 1)

    cur_count = 0;
    directory_name = 'output'
    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            if int(filename.split('.')[0]) >= start:
                input_file_name = directory_name + '/' +filename
                with open(input_file_name, 'r') as f:
                    tempdata = json.load(f)
                    data.extend(tempdata)
                cur_count += 1
        if cur_count == num_files_to_include:
            break
                # print(len(data))

    fromJeb, toJeb = divideEmailsBySender(data)
    toJeb = toJeb[:len(fromJeb)]


    # these are all json objects, need to merge their bodies.
    fromJebTraining, fromJebTest = dataSplit(.7, fromJeb)
    toJebTraining, toJebTest = dataSplit(.7, toJeb)

    print(str(len(fromJebTest)))

    # list of sentences that's ready for n-gram model creation
    fromJebTrainingCorpus = prepareEmailsForNGram(fromJebTraining)
    toJebTrainingCorpus = prepareEmailsForNGram(toJebTraining)

    # ngram models are created! (for now these are unigram counts)
    fromUnigram = createNgram(1, fromJebTrainingCorpus)
    toUnigram = createNgram(1, toJebTrainingCorpus)

    fromBigram = createNgram(2, fromJebTrainingCorpus)
    toBigram = createNgram(2, toJebTrainingCorpus)

    #return (fromUnigram, toUnigram, from)
    print(str(thread_name) + ' is done!')
    return (fromUnigram, fromBigram, toUnigram, toBigram, fromJebTest, toJebTest)

def runAndGet(thread_name, thread_number, total_thread_count):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    data = []

    num_files_to_include = 625
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

    #return (fromUnigram, toUnigram, from)
    print(str(thread_name) + ' is done!')
    return (fromUnigram, fromBigram, toUnigram, toBigram)

def getAllModels():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

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
    print('Hey, do something else')

if __name__ == '__main__':
    main()

print('\n\n\n')
