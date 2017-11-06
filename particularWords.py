'''
Tries to find a set of words that appear often in one corpora and not in the
other.
'''
from pprint import pprint
import EmailProcessor

def find_particular_words(freq1, freq2, threshold):
    ''' inputs are dictionaries. keys are words, values are counts
        threshold is the ratio where the difference is significant'''

    particularWords = {}
    for key in freq1:
        if key in freq2:
            if (max(freq1[key], freq2[key]) / min(freq1[key], freq2[key])) > threshold:
                # if (wc1_ratio > wc2_ratio):
                #     if key not in corpus1_words:
                #         corpus1_words[key] =  word_count1[key]
                # else:
                #     if key not in corpus2_words:
                #         corpus2_words[key] = word_count2[key]
                particularWords[key] = (freq1[key], freq2[key])

    # for key in word_count2:
    #     if key in word_count1:
    #         count_sum = word_count1[key] + word_count2[key]
    #         wc1_ratio = word_count1[key] / count_sum
    #         wc2_ratio = word_count2[key] / count_sum
    #         if abs(wc1_ratio - wc2_ratio) > threshold:
    #             if (wc1_ratio > wc2_ratio):
    #                 if key not in corpus1_words:
    #                     corpus1_words[key] =  word_count1[key]
    #             else:
    #                 if key not in corpus2_words:
    #                     corpus2_words[key] = word_count2[key]
    # return (corpus1_words, corpus2_words)
    return particularWords

def getNGramFrequency(word_count):
    freq = {}
    total_word_count = sum(word_count.values())
    for key, val in word_count.items():
        freq[key] = val / total_word_count
    return freq



def main():
    fromUnigram, toUnigram = EmailProcessor.runAndGet()
    # print(sum(fromUnigram.values()))
    # print(sum(toUnigram.values()))

    fromFreq = getNGramFrequency(fromUnigram)
    toFreq = getNGramFrequency(toUnigram)



    a = find_particular_words(fromFreq, toFreq, 20)
    pprint(a)
    # print(b)


if __name__ == '__main__':
    main()
