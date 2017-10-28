import nltk.data
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint
import random
import copy
from decimal import *
import csv
import operator
import collections

nltk.download('punkt')

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
               sentnece)
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

def main():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    fp = open("exampleCorpus.txt", 'r', encoding='UTF-8', errors='ignore')

    data = fp.read()
    print(data)
    sentences = sentence_splitter.tokenize(data)


    numSentences = len(sentences)
    numWords = 0
    wordDict = {}

    modifiedSentences = []

    for sentence in sentences:
        # get rid of end-of-sentence punctuation so that they won't be
        #  counted as words
        sentence = sentence[:-1]
        sentence = sentence.lower()
        modifiedSentences.append(sentence)
        tokenized_text = nltk.word_tokenize(sentence)
        for word in tokenized_text:
            numWords += 1
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1

    sentences = modifiedSentences

    seventyThirty = dataSplit(.7, sentences)

    gramDict = {}
    total1Grams = 0

    # first create the ngram models
    for i in range(1, 2):
        trainingGrams = createNgram(i, seventyThirty[0])
        gramDict[str(i) + "gram"] = trainingGrams

    pprint.pprint(gramDict)


if __name__ == '__main__':
    main()
