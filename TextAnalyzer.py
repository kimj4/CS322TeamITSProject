import EmailProcessor
import json

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
        return


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
    sentenceMLE = 1;
    totalUpspeakNMinusOneGrams = sum(upspeakNMinusOneGramModel.values())
    totalUpspeakNGrams = sum(upspeakNGramModel.values())


    topThreeUpspeakProbs = {}
    # right now, only calculates upspeak MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        if N > 1:
            # CHECK IF THIS STILL WORKS
            if key.split(' ')[-2] == '<s>':
                sentenceMLE = sentenceMLE * (upspeakNMinusOneGramModel['<s>'] / totalUpspeakNMinusOneGrams) * sentenceNGrams[key]
            elif key in upspeakNGramModel.keys():
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                sentenceMLE = sentenceMLE * (upspeakNGramModel[key] / upspeakNMinusOneGramModel[prevGram]) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001
        else:
            if key in upspeakNGramModel.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                sentenceMLE = sentenceMLE * (upspeakNgramModel[key] / totalUpspeakNgrams) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001

    upspeakSentenceMLE = sentenceMLE

    sentenceMLE = 1
    totalDownspeakNMinusOneGrams = sum(downspeakNMinusOneGramModel.values())
    totalDownspeakNGrams = sum(downspeakNGramModel.values())

    # right now, only calculates downspeak MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                # CHECK TO SEE IF THIS IS CORRECT
                sentenceMLE = sentenceMLE * (downspeakNMinusOneGramModel['<s>'] / totalDownspeakNMinusOneGrams) * sentenceNGrams[key]
            elif key in downspeakNGramModel.keys():
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                sentenceMLE = sentenceMLE * (downspeakNGramModel[key] / downspeakNMinusOneGramModel[prevGram]) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001
        else:
            if key in downspeakNGramModel.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                sentenceMLE = sentenceMLE * (downspeakNGramModel[key] / totalDownspeakNGrams) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001

    print('upspeak MLE is ', upspeakSentenceMLE)
    print('downspeak MLE is ', sentenceMLE)
    return sentenceMLE

def main():
    modelTuple = EmailProcessor.getAllModels()
    with open('models/upspeakUnigramModel.json', 'r') as fp:
        upspeakUnigramModel = json.load(fp)
    print(upspeakUnigramModel)
    print(type(upspeakUnigramModel))
    print(calculateMLE(2, 'Please clap'))

if __name__ == '__main__':
    main()
