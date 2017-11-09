import EmailProcessor
import json
import sys

def calculateMLE(N, sentence):
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
    print(sentenceNGrams)
    upspeakSentenceMLE = 1;
    totalUpspeakNMinusOneGrams = sum(upspeakNMinusOneGramModel.values())
    totalUpspeakNGrams = sum(upspeakNGramModel.values())


    topThreeUpspeakProbs = {}
    minTopThreeUpspeakProb = 0
    # right now, only calculates upspeak MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        if N > 1:
            # CHECK IF THIS STILL WORKS
            if key.split(' ')[-2] == '<s>':
                probability = upspeakNMinusOneGramModel['<s>'] / totalUpspeakNMinusOneGrams
            elif key in upspeakNGramModel.keys():
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                probability = upspeakNGramModel[key] / upspeakNMinusOneGramModel[prevGram]
            else:
                probability = 0.000001

            upspeakSentenceMLE = upspeakSentenceMLE * probability * sentenceNGrams[key]
            # check if probability is greater than the min of the threee greatest stored probabilities
            if probability > minTopThreeUpspeakProb:
                maxEntryLessThanProbability = minTopThreeUpspeakProb
                for probKey, probValue in topThreeUpspeakProbs.items():
                    if probKey > maxEntryLessThanProbability and probKey < probability:
                        maxEntryLessThanProbability = probKey

                topThreeUpspeakProbs[probability] = key

                if len(topThreeUpspeakProbs) > 3:
                    topThreeUpspeakProbs.pop(min(topThreeUpspeakProbs, key=topThreeUpspeakProbs.get), None)
        else:
            if key in upspeakNGramModel.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                upspeakSentenceMLE = upspeakSentenceMLE * (upspeakNgramModel[key] / totalUpspeakNgrams) * sentenceNGrams[key]
            else:
                upspeakSentenceMLE = upspeakSentenceMLE * 0.000001 * sentenceNGrams[key]

    topThreeDownspeakProbs = {}
    minTopThreeDownspeakProb = 0
    downspeakSentenceMLE = 1
    totalDownspeakNMinusOneGrams = sum(downspeakNMinusOneGramModel.values())
    totalDownspeakNGrams = sum(downspeakNGramModel.values())

    # right now, only calculates downspeak MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                # CHECK TO SEE IF THIS IS CORRECT
                probability = (downspeakNMinusOneGramModel['<s>'] / totalDownspeakNMinusOneGrams)
                #downspeakSentenceMLE = downspeakSentenceMLE * probability * sentenceNGrams[key]
            elif key in downspeakNGramModel.keys():
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                probability = (downspeakNGramModel[key] / downspeakNMinusOneGramModel[prevGram])
                #downspeakSentenceMLE = downspeakSentenceMLE * probability * sentenceNGrams[key]
            else:
                probability = 0.000001
                #downspeakSentenceMLE = downspeakSentenceMLE * probability * sentenceNGrams[key]
            downspeakSentenceMLE = downspeakSentenceMLE * probability * sentenceNGrams[key]

            # check if probability is greater than the min of the threee greatest stored probabilities
            if probability > minTopThreeDownspeakProb:
                maxEntryLessThanProbability = minTopThreeDownspeakProb
                for probKey, probValue in topThreeDownspeakProbs.items():
                    if probKey > maxEntryLessThanProbability and probKey < probability:
                        maxEntryLessThanProbability = probKey

                topThreeDownspeakProbs[probability] = key

                if len(topThreeDownspeakProbs) > 3:
                    topThreeDownspeakProbs.pop(min(topThreeDownspeakProbs, key=topThreeDownspeakProbs.get), None)

        else:
            if key in downspeakNGramModel.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                downspeakSentenceMLE = downspeakSentenceMLE * (downspeakNGramModel[key] / totalDownspeakNGrams) * sentenceNGrams[key]
            else:
                downspeakSentenceMLE = downspeakSentenceMLE * 0.000001 * sentenceNGrams[key]

    print('upspeak MLE is ', upspeakSentenceMLE)
    print(topThreeUpspeakProbs)
    print('downspeak MLE is ', downspeakSentenceMLE)
    print(topThreeDownspeakProbs)

    return downspeakSentenceMLE

def main():
    #modelTuple = EmailProcessor.getAllModels()
    modelTuple = EmailProcessor.runAndGet()

    with open('models/upspeakUnigramModel.json', 'r') as fp:
        upspeakUnigramModel = json.load(fp)
    #print(upspeakUnigramModel)
    #print(type(upspeakUnigramModel))
    if len(sys.argv) > 1:
        param = sys.argv[1]
        if len(param) > 0:
            if param[-1] in '!?.':
                param = param[:-1]
            print(calculateMLE(2, str(param)))
    else:
        print(calculateMLE(2, 'I wanted to ask you to give your recommendation to my friend'))

if __name__ == '__main__':
    main()
