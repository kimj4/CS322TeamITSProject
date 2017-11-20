import EmailProcessor
import json
import sys
import cProfile
import _thread as thread
# import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from nltk import tokenize

def calculateAllMLEs(N, sentence):
    '''
    calculates the minimum likelihood estimate on sample sentences for given model
    '''
    if N == 1:
        nMinusOnePrefix = 'Uni'
        nPrefix = 'Uni'
    elif N == 2:
        nMinusOnePrefix = 'Uni'
        nPrefix = 'Bi'
    elif N == 3:
        nMinusOnePrefix = 'Bi'
        nPrefix = 'Tri'
    else:
        print("Model not available. Please pick an N value between 1 and 3.")
        return 0


    upspeakNMinusOneModelFile = 'models/upspeak' + nMinusOnePrefix + 'gramModel.json'
    downspeakNMinusOneModelFile = 'models/downspeak' + nMinusOnePrefix + 'gramModel.json'
    upspeakNModelFile = 'models/upspeak' + nPrefix + 'gramModel.json'
    downspeakNModelFile = 'models/downspeak' + nPrefix + 'gramModel.json'

    with open(upspeakNMinusOneModelFile, 'r') as fp:
        upspeakNMinusOneGramModel = json.load(fp)
    with open(downspeakNMinusOneModelFile, 'r') as fp:
        downspeakNMinusOneGramModel = json.load(fp)
    with open(upspeakNModelFile, 'r') as fp:
        upspeakNGramModel = json.load(fp)
    with open(downspeakNModelFile, 'r') as fp:
        downspeakNGramModel = json.load(fp)


    sentenceNGrams = EmailProcessor.createNgram(N, [sentence])

    print("\n##### upspeak MLE ######")
    calculateMLEWithPhrases(N, upspeakNGramModel, upspeakNMinusOneGramModel, sentenceNGrams)
    print("\n##### downspeak MLE ######")
    calculateMLEWithPhrases(N, downspeakNGramModel, downspeakNMinusOneGramModel, sentenceNGrams)
    return

def calculateMLEWithPhrases(N, nGramModel, nMinusOneGramModel, sentenceNGrams):
    '''

    '''
    sentenceMLE = 1;
    totalNMinusOneGrams = sum(nMinusOneGramModel.values())
    totalNGrams = sum(nGramModel.values())

    topThreeProbs = {}
    minTopThreeProb = 0
    unkCount = 0
    knownCount = 0

    # right now, only calculates MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        #print ('currently looking at {}'.format(key))
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                probability = nMinusOneGramModel['<s>'] / totalNMinusOneGrams
            elif key in nGramModel.keys():
                knownCount += 1
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                probability = nGramModel[key] / nMinusOneGramModel[prevGram]
            else:
                probability = 0.000001# (1 / totalNMinusOneGrams)

            sentenceMLE = sentenceMLE * probability * sentenceNGrams[key]
            # check if probability is greater than the min of the threee greatest stored probabilities
            if probability > minTopThreeProb:
                maxEntryLessThanProbability = minTopThreeProb
                for probKey, probValue in topThreeProbs.items():
                    if probKey > maxEntryLessThanProbability and probKey < probability:
                        maxEntryLessThanProbability = probKey

                topThreeProbs[probability] = key

                if len(topThreeProbs) > 3:
                    topThreeProbs.pop(min(topThreeProbs, key=topThreeProbs.get), None)
        else:
            if key in nGramModel.keys():
                sentenceMLE = sentenceMLE * (nGramModel[key] / totalNgrams) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * (1 / totalNMinusOneGrams) * sentenceNGrams[key]
    print("MLE", sentenceMLE)
    print("Highest-probability phrases: ")
    for string in topThreeProbs.values():
        print(string)
    return sentenceMLE

def calculateMLE(N, nGramModel, nMinusOneGramModel, sentenceNGrams):
    '''

    '''
    sentenceMLE = 1;
    totalNMinusOneGrams = sum(nMinusOneGramModel.values())
    totalNGrams = sum(nGramModel.values())

    topThreeProbs = {}
    minTopThreeProb = 0
    unkCount = 0
    knownCount = 0

    # right now, only calculates MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        #print ('currently looking at {}'.format(key))
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                probability = nMinusOneGramModel['<s>'] / totalNMinusOneGrams
            elif key in nGramModel.keys():
                knownCount += 1
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                probability = nGramModel[key] / nMinusOneGramModel[prevGram]
            else:
                probability = 0.000001# (1 / totalNMinusOneGrams)

            sentenceMLE = sentenceMLE * probability * sentenceNGrams[key]
            # check if probability is greater than the min of the threee greatest stored probabilities
            if probability > minTopThreeProb:
                maxEntryLessThanProbability = minTopThreeProb
                for probKey, probValue in topThreeProbs.items():
                    if probKey > maxEntryLessThanProbability and probKey < probability:
                        maxEntryLessThanProbability = probKey

                topThreeProbs[probability] = key

                if len(topThreeProbs) > 3:
                    topThreeProbs.pop(min(topThreeProbs, key=topThreeProbs.get), None)
        else:
            if key in nGramModel.keys():
                sentenceMLE = sentenceMLE * (nGramModel[key] / totalNgrams) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * (1 / totalNMinusOneGrams) * sentenceNGrams[key]

    return sentenceMLE


def mergeGrams(list_of_grams):
    '''
    merges dictionaries of ngrams from the training data that were
    found and returned during multiprocessing

    returns dictionary of ngrams, where the value is the frequency of the key
    '''
    merged = {}
    for gram in list_of_grams:
        for key, val in gram.items():
            if key in merged:
                merged[key] += gram[key]
            else:
                merged[key] = gram[key]
    return merged

def runOnTestSet(N=2):
    '''
    classifies sentences in the test set as upspeak or downspeak based on
    which MLE is higher

    prints confusion matrix of the results

    returns nothing
    '''

    resultsDict = {'predictedDownspeakActualDownspeak': 0,
                   'predictedDownspeakActualUpspeak': 0,
                   'predictedUpspeakActualUpspeak': 0,
                   'predictedUpspeakActualDownspeak': 0}

    if N == 1:
        nMinusOnePrefix = 'Uni'
        nPrefix = 'Uni'
    elif N == 2:
        nMinusOnePrefix = 'Uni'
        nPrefix = 'Bi'
    elif N == 3:
        nMinusOnePrefix = 'Bi'
        nPrefix = 'Tri'
    else:
        print("Model not available. Please pick an N value between 1 and 3.")
        return 0


    upspeakNMinusOneModelFile = 'models/upspeak' + nMinusOnePrefix + 'gramModel.json'
    downspeakNMinusOneModelFile = 'models/downspeak' + nMinusOnePrefix + 'gramModel.json'
    upspeakNModelFile = 'models/upspeak' + nPrefix + 'gramModel.json'
    downspeakNModelFile = 'models/downspeak' + nPrefix + 'gramModel.json'

    with open(upspeakNMinusOneModelFile, 'r') as fp:
        upspeakNMinusOneGramModel = json.load(fp)
    with open(downspeakNMinusOneModelFile, 'r') as fp:
        downspeakNMinusOneGramModel = json.load(fp)
    with open(upspeakNModelFile, 'r') as fp:
        upspeakNGramModel = json.load(fp)
    with open(downspeakNModelFile, 'r') as fp:
        downspeakNGramModel = json.load(fp)

    for type in ['upspeak', 'downspeak']:
        with open('models/' + type + 'TestCorpus.json', 'r') as fp:
            testData = json.load(fp)
            for emailDict in testData:
                sentences = tokenize.sent_tokenize(emailDict['body'])
                for sentence in sentences:
                    sentenceNGrams = EmailProcessor.createNgram(N, [sentence])
                    upspeakMLE = calculateMLE(N, upspeakNGramModel, upspeakNMinusOneGramModel, sentenceNGrams)
                    downspeakMLE = calculateMLE(N, downspeakNGramModel, downspeakNMinusOneGramModel, sentenceNGrams)
                    if (upspeakMLE > downspeakMLE):
                        if (type == 'upspeak'):
                            resultsDict['predictedUpspeakActualUpspeak'] += 1
                        else:
                            resultsDict['predictedUpspeakActualDownspeak'] += 1
                    elif (upspeakMLE < downspeakMLE):
                        if (type == 'downspeak'):
                            resultsDict['predictedDownspeakActualDownspeak'] += 1
                        else:
                            resultsDict['predictedDownspeakActualUpspeak'] += 1
                    # else:
                    #     print(upspeakMLE)
                    #     print(downspeakMLE)

    print(resultsDict)



def main():
    '''
    currently runs testing on test corpus with dynamically-generated training corpus,
    calling getNgramsBalanced() in EmailProcessor
    '''
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
            results.append( pool.apply_async( EmailProcessor.getNgramsBalanced, t ) )

        r = []
        for result in results:
            r.append(result.get())

        fromUnigrams = []
        fromBigrams = []
        toUnigrams = []
        toBigrams = []

        downspeakTraining = []
        upspeakTraining = []

        for result in r:
            for i in range(6):
                if i == 0:
                    fromUnigrams.append(result[i])
                elif i == 1:
                    fromBigrams.append(result[i])
                elif i == 2:
                    toUnigrams.append(result[i])
                elif i == 3:
                    toBigrams.append(result[i])
                elif i == 4:
                    downspeakTraining.append(result[i])
                elif i == 5:
                    upspeakTraining.append(result[i])


        upspeakUnigramModel = mergeGrams(toUnigrams)
        upspeakBigramModel = mergeGrams(toBigrams)
        downspeakUnigramModel = mergeGrams(fromUnigrams)
        downspeakBigramModel = mergeGrams(fromBigrams)

        downspeakTrainingCorpus = [item for sublist in downspeakTraining for item in sublist]
        upspeakTrainingCorpus = [item for sublist in upspeakTraining for item in sublist]

        # downspeakTrainingCorpus = mergeGrams(downspeakTraining)
        # upspeakTraningCorpus = mergeGrams(upspeakTraining)

        with open('models/downspeakTestCorpus.json', 'w') as fp:
            json.dump(downspeakTrainingCorpus, fp, indent = 4)
        with open('models/upspeakTestCorpus.json', 'w') as fp:
            json.dump(upspeakTrainingCorpus, fp, indent = 4)

        with open('models/upspeakUnigramModel.json', 'w') as f:
            json.dump(upspeakUnigramModel, f)
        with open('models/upspeakBigramModel.json', 'w') as f:
            json.dump(upspeakBigramModel, f)
        with open('models/downspeakUnigramModel.json', 'w') as f:
            json.dump(downspeakUnigramModel, f)
        with open('models/downspeakBigramModel.json', 'w') as f:
            json.dump(downspeakBigramModel, f)

    if len(sys.argv) > 1:
        param = sys.argv[1]
        if len(param) > 0:
            if param[-1] in '!?.':
                param = param[:-1]
            calculateAllMLEs(2, str(param))
    else:
        runOnTestSet()
    #
    #     param = sys.argv[1]
    #     if len(param) > 0:
    #         if param[-1] in '!?.':
    #             param = param[:-1]
    #         print(calculateAllMLEs(2, str(param)))
    # else:
    #     print(calculateAllMLEs(2, 'I wanted to ask you to give your recommendation to my friend'))

if __name__ == '__main__':
    main()
    # cProfile.run('main()')
