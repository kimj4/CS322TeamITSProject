import EmailProcessor
import json
import sys
import cProfile
import _thread as thread
# import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

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

def mergeGrams(list_of_grams):
    merged = {}
    for gram in list_of_grams:
        for key, val in gram.items():
            if key in merged:
                merged[key] += gram[key]
            else:
                merged[key] = gram[key]
    return merged

def main():
    #modelTuple = EmailProcessor.getAllModels()
    # modelTuple = EmailProcessor.runAndGet()
    # thread.start_new_thread( EmailProcessor.runAndGet, ("1",) )
    # thread.start_new_thread( EmailProcessor.runAndGet, ("2",) )
    # thread.start_new_thread( EmailProcessor.runAndGet, ("3",) )
    # thread.start_new_thread( EmailProcessor.runAndGet, ("4",) )
    # thread.start_new_thread( EmailProcessor.runAndGet, ("6",) )
    # EmailProcessor.runAndGet('6')
    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     future1 = executor.submit(EmailProcessor.runAndGet, '1')
    #     future2 = executor.submit(EmailProcessor.runAndGet, '2')
    #     future3 = executor.submit(EmailProcessor.runAndGet, '3')
    #     future4 = executor.submit(EmailProcessor.runAndGet, '4')
    #     future5 = executor.submit(EmailProcessor.runAndGet, '5')
    #     future6 = executor.submit(EmailProcessor.runAndGet, '6')
    #     future7 = executor.submit(EmailProcessor.runAndGet, '7')
    #     future8 = executor.submit(EmailProcessor.runAndGet, '8')
    #     r1 = future1.result()
    #     r2 = future2.result()
    #     r3 = future3.result()
    #     r4 = future4.result()
    #     r5 = future5.result()
    #     r6 = future6.result()
    #     r7 = future7.result()
    #     r8 = future8.result()
    # print('here')

    pool = multiprocessing.Pool( multiprocessing.cpu_count() )
    tasks = []
    tNum = 0
    max_t = 4
    while tNum < max_t:
        tNum += 1
        tasks.append( (str(tNum),) )
    results = []
    for t in tasks:
        results.append( pool.apply_async( EmailProcessor.runAndGet, t ) )

    r = []
    for result in results:
        r.append(result.get())

    fromUnigrams = []
    fromBigrams = []
    toUnigrams = []
    toBigrams = []
    for result in r:
        for i in range(4):
            if i == 0:
                fromUnigrams.append(result[i])
            elif i == 1:
                fromBigrams.append(result[i])
            elif i == 2:
                toUnigrams.append(result[i])
            elif i == 3:
                toBigrams.append(result[i])

    # fromUnigrams = [r1[0], r2[0], r3[0], r4[0], r5[0], r6[0], r7[0], r8[0]]
    # fromBigrams = [r1[1], r2[1], r3[1], r4[1], r5[1], r6[1], r7[1], r8[1]]
    # toUnigrams = [r1[2], r2[2], r3[2], r4[2], r5[2], r6[2], r7[2], r8[2]]
    # toBigrams = [r1[3], r2[3], r3[3], r4[3], r5[3], r6[3], r7[3], r8[3]]

    upspeakUnigramModel = mergeGrams(toUnigrams)
    upspeakBigramModel = mergeGrams(toBigrams)
    downspeakUnigramModel = mergeGrams(fromUnigrams)
    downspeakBigramModel = mergeGrams(fromBigrams)

    with open('models/upspeakUnigramModel.json', 'w') as f:
        json.dump(upspeakUnigramModel, f)
    with open('models/upspeakBigramModel.json', 'w') as f:
        json.dump(upspeakBigramModel, f)
    with open('models/downspeakUnigramModel.json', 'w') as f:
        json.dump(downspeakUnigramModel, f)
    with open('models/downspeakBigramModel.json', 'w') as f:
        json.dump(downspeakUnigramModel, f)



    # with open('models/upspeakUnigramModel.json', 'r') as fp:
    #     upspeakUnigramModel = json.load(fp)
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
    # cProfile.run('main()')
