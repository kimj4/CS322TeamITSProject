import EmailProcessor
import json

def calculateMLE(N, sentence):
    '''
    calculates the minimum likelihood estimate on sample sentences for given model
    '''

    with open('models/upspeakUnigramModel.json', 'r') as fp:
        upspeakUnigramModel = json.load(fp)
    with open('models/downspeakUnigramModel.json', 'r') as fp:
        downspeakUnigramModel = json.load(fp)
    with open('models/upspeakBigramModel.json', 'r') as fp:
        upspeakBigramModel = json.load(fp)
    with open('models/downspeakBigramModel.json', 'r') as fp:
        downspeakBigramModel = json.load(fp)


    sentenceNGrams = EmailProcessor.createNgram(N, [sentence])
    sentenceMLE = 1;
    totalUpspeakUnigrams = sum(upspeakUnigramModel.values())

    # right now, only calculates upspeak MLE, specific to bigrams/unigrams
    for key, value in sentenceNGrams.items():
        if N > 1:
            if key.split(' ')[-2] == '<s>':
                sentenceMLE = sentenceMLE * (upspeakUnigramModel['<s>'] / totalUpspeakUnigrams) * sentenceNGrams[key]
            elif key in upspeakBigramModel.keys():
                # print('n-gram found')
                # calculating P(w1 w2 | w1)
                prevGram = " ".join(key.split(" ")[:-1])
                sentenceMLE = sentenceMLE * (upspeakBigramModel[key] / upspeakUnigramModel[prevGram]) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001
        else:
            if key in upspeakBigramModel.keys():
                # print('n-gram found')
                # print(str(probabilityDict[key]))
                sentenceMLE = sentenceMLE * (upspeakUnigramModel[key] / totalUpspeakUnigrams) * sentenceNGrams[key]
            else:
                sentenceMLE = sentenceMLE * 0.000001


    return sentenceMLE

def main():
    modelTuple = EmailProcessor.getAllModels()
    with open('models/upspeakUnigramModel.json', 'r') as fp:
        upspeakUnigramModel = json.load(fp)
    print(upspeakUnigramModel)
    print(type(upspeakUnigramModel))
    calculateMLE(2, 'Please get in touch soon')

if __name__ == '__main__':
    main()
