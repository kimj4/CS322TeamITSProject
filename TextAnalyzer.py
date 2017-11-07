import EmailProcessor
import json

def calculateMLE(sentence, model):
    '''
    calculates the minimum likelihood estimate on sample sentences for given model
    '''

    sentenceMLE = 1;
    testNGrams = createNgram(N, [sentence])
    for key, value in testNGrams.items():
        # if N > 1:
        #     if key.split(' ')[-2] == '<s>':
        #         sentenceMLE = sentenceMLE * (oneGram['<s>'] / oneGramTotal) * testNGrams[key]
        #     elif key in probabilityDict.keys():
        #         # print('n-gram found')
        #         sentenceMLE = sentenceMLE * probabilityDict[key] * testNGrams[key]
        #     else:
        #         sentenceMLE = sentenceMLE * 0.000001
        # else:
        if key in probabilityDict.keys():
            # print('n-gram found')
            # print(str(probabilityDict[key]))
            sentenceMLE = sentenceMLE * probabilityDict[key] * testNGrams[key]
        else:
            sentenceMLE = sentenceMLE * 0.000001

    return sentenceMLE

def main():
    modelTuple = EmailProcessor.getAllModels()
    with open('models/upspeakUnigramModel.json', 'r') as fp:
        upspeakUnigramModel = json.load(fp)
    print(upspeakUnigramModel)
    print(type(upspeakUnigramModel))

if __name__ == '__main__':
    main()
