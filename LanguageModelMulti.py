import json
import time
import re

ancFile = open('ANC-all-count.txt')
ancDict = {}

multiAlphas = ['bit', 'aflx', 'hs', 'moq', 'gpuy', 'cjkr', 'nwz', 'dev']

class AlphaFreq:
    alpha = ""
    freq = 0

    def __init__(self, alpha, freq=0):
        self.alpha = alpha
        self.freq = freq

class MultiAlphaFreq:
    multiAlpha = ""
    freq = 0

    def __init__(self, multiAlpha, freq=0):
        self.multiAlpha = multiAlpha
        self.freq = freq

#return a list of word which starts with the given prefix.
#the order is not sorted.
def getWordsFromPrefix(prefix, wordList):
    words = []
    for word in wordList:
        if word.startswith(prefix):
            words.append(word)
    return words

#return list of word which starts with the given prefix.
#the order of list is sorted by freq of the word.
def getWordsFromPrefixSorted(prefix, wordList):
    words = getWordsFromPrefix(prefix, wordList)
    def cmpWord(word1, word2):
        return cmp(ancDict[word1], ancDict[word2])
    def cmpWordByPrefixLength(word1, word2):
        if len(word1) == len(word2):
            return 0
        elif len(word1) == len(prefix):
            return 1
        elif len(word2) == len(prefix):
            return -1
        else:
            return 0
    words = sorted(words, cmp=cmpWord, reverse=True)
    words = sorted(words, cmp=cmpWordByPrefixLength, reverse=True)
    return words

#return list of AlphaFreq object list.
#each AlphaFreq has single alphabet character and freq of startswith(prefix+alpha).
#the order is not sorted.
def getAlphaFreqsFromPrefix(prefix, wordList):
    words = getWordsFromPrefix(prefix, wordList)
    alphaFreqs = []
    for i in range(26):
        alphaFreq = AlphaFreq(chr(ord('a') + i))
        alphaFreqs.append(alphaFreq)
        for word in words:
            if word.startswith(prefix + alphaFreq.alpha):
                alphaFreq.freq += ancDict[word]
    return alphaFreqs

#return list of alphabet.
#the order of list is sorted by freq of startswith(prefix+alpha).
def getAlphasFromPrefix(prefix, wordList):
    def cmpAlphaFreqs(alphaFreq1, alphaFreq2):
        return cmp(alphaFreq1.freq, alphaFreq2.freq)
    sortedAlphaFreqs = sorted(getAlphaFreqsFromPrefix(
        prefix, wordList), cmp=cmpAlphaFreqs, reverse=True)
    return map(lambda alphaFreq: alphaFreq.alpha, sortedAlphaFreqs)

#
def getMultiAlphaFreqsFromMultiAlphaPrefix(multiAlphaPrefix, wordList):
    multiAlphaFreqs = []

    prefixes = getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix)

    for multiAlpha in multiAlphas:
        multiAlphaFreq = MultiAlphaFreq(multiAlpha, 0)
        for prefix in prefixes:
            alphaFreqs = getAlphaFreqsFromPrefix(prefix, wordList)
            for alpha in multiAlpha:
                multiAlphaFreq.freq += alphaFreqs[ord(alpha) - ord('a')].freq
        multiAlphaFreqs.append(multiAlphaFreq)

    return multiAlphaFreqs

#
def getMultiAlphasFromMultiAlphaPrefix(multiAlphaPrefix, wordList):
    def cmpMultiAlphaFreqs(multiAlphaFreq1, multiAlphaFreq2):
        return cmp(multiAlphaFreq1.freq, multiAlphaFreq2.freq)

    sortedMultiAlphaFreqs = sorted(getMultiAlphaFreqsFromMultiAlphaPrefix(
        multiAlphaPrefix, wordList), cmp=cmpMultiAlphaFreqs, reverse=True)

    return map(lambda multiAlphaFreq: multiAlphaFreq.multiAlpha, sortedMultiAlphaFreqs)

#
def getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix):
    prefixes = ['']

    for multiAlpha in multiAlphaPrefix:
        tempMultiInputs = []
        for multiInput in prefixes:
            for alpha in multiAlpha:
                tempMultiInputs.append(multiInput + alpha)
        prefixes = tempMultiInputs

    return prefixes

#
def getMultiAlphaDictFromPrefixLength(prefixLength):
    staticMultiAlphaDict = {}

    prefixes = [[]]
    for i in range(prefixLength):
        tempPrefixes = []
        for prefix in prefixes:
            for multiAlpha in multiAlphas:
                tempPrefixes.append(prefix + [multiAlpha])
        prefixes = tempPrefixes

    for prefix in prefixes:
        staticMultiAlphaDict[json.dumps(prefix)] = getMultiAlphasFromMultiAlphaPrefix(prefix, ancDict.keys())

    return staticMultiAlphaDict

# return word list using multiAlphaPrefix
# return list size would be wordsLength. If 0, return all list.
# input: multiAlphaPrefix list. ex) ['bit', 'dev', 'hs']
# output: words list ordered by freq. ex) ['best', 'test', 'behind']
def getWordsFromMultiAlphaPrefix(multiAlphaPrefix, wordsLength = 5):
    prefixes = getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix)

    words = []
    for prefix in prefixes:
        words += getWordsFromPrefix(prefix, ancDict.keys())

    def cmpWord(word1, word2):
        return cmp(ancDict[word1], ancDict[word2])
    def cmpWordByPrefixLength(word1, word2):
        if len(word1) == len(word2):
            return 0
        elif len(word1) == len(prefix):
            return 1
        elif len(word2) == len(prefix):
            return -1
        else:
            return 0
    words = sorted(words, cmp=cmpWord, reverse=True)
    words = sorted(words, cmp=cmpWordByPrefixLength, reverse=True)

    if wordsLength > 0 and len(words) > wordsLength:
        words = words[0 : wordsLength]

    return words

# return dictionary whose key is multiAlphaPrefix(json), whose value is corresponding word list
# input: prefixLength in natural number. ex) 3
# output: dictionary. ex) {("['bit','dev','hs']":['best','test,'behind']), ... }
def getPrefixWordDictFromPrefixLength(prefixLength, wordsLength = 5):
    prefixWordDict = {}

    prefixes = [[]]
    for i in range(prefixLength):
        tempPrefixes = []
        for prefix in prefixes:
            for multiAlpha in multiAlphas:
                tempPrefixes.append(prefix + [multiAlpha])
        prefixes = tempPrefixes

    for prefix in prefixes:
        prefixWordDict[json.dumps(prefix)] = getWordsFromMultiAlphaPrefix(prefix, wordsLength)

    return prefixWordDict

# return word list and multiAlphaFreq list from prefix.
# hybrid method used: for prefix length 1~3, use hashed file data.
#                     for prefix length >3, use 3-hashed file data and produce next.
def getWordsAndMultiAlphaFreqsFromMultiAlphaPrefixHybrid(multiAlphaPrefix, wordsLength = 5):
    if len(multiAlphaPrefix) == 0:
        return word_0, key_0
    if len(multiAlphaPrefix) == 1:
        return word_1[json.dumps(multiAlphaPrefix)], key_1[json.dumps(multiAlphaPrefix)]
    if len(multiAlphaPrefix) == 2:
        return word_2[json.dumps(multiAlphaPrefix)], key_2[json.dumps(multiAlphaPrefix)]
    if len(multiAlphaPrefix) == 3:
        return word_3[json.dumps(multiAlphaPrefix)], key_3[json.dumps(multiAlphaPrefix)]

    ts = time.time()
    wordFiltered = word_3[json.dumps(multiAlphaPrefix[:3])]

    # this line take O(8^prefixLength)
    # the time may be reduced using another hashing file 
    prefixes = getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix)
    #print('1:' + str(time.time()-ts))

    # produce words
    words = []
    for prefix in prefixes:
        for word in wordFiltered:
            if word.startswith(prefix):
                words.append(word)
    #print('2:' + str(time.time()-ts))

    # produce multiAlphaFreqs
    multiAlphaFreqs = []
    for multiAlpha in multiAlphas:
        multiAlphaFreq = MultiAlphaFreq(multiAlpha, 0)
        multiAlphaFreqs.append(multiAlphaFreq)

    for prefix in prefixes:
        alphaFreqs = getAlphaFreqsFromPrefix(prefix, wordFiltered)
        for multiAlpha in multiAlphas:
            for alpha in multiAlpha:
                multiAlphaFreq.freq += alphaFreqs[ord(alpha) - ord('a')].freq
    #print('3:' + str(time.time()-ts))

    # sort and cut words
    def cmpWord(word1, word2):
        return cmp(ancDict[word1], ancDict[word2])
    words = sorted(words, cmp=cmpWord, reverse=True)
    if wordsLength > 0 and len(words) > wordsLength:
        words = words[0 : wordsLength]
    #print('4:' + str(time.time()-ts))

    # sort and make to list multiAlphaPrefix
    def cmpMultiAlphaFreqs(multiAlphaFreq1, multiAlphaFreq2):
        return cmp(multiAlphaFreq1.freq, multiAlphaFreq2.freq)
    multiAlphaFreqs = sorted(multiAlphaFreqs, cmp=cmpMultiAlphaFreqs, reverse=True)
    #print('5:' + str(time.time()-ts))

    return words, map(lambda multiAlphaFreq: multiAlphaFreq.multiAlpha, multiAlphaFreqs)

'''
def getMultiAlphaFreqsFromMultiAlphaPrefix(multiAlphaPrefix):
    multiAlphaFreqs = []

    prefixes = getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix)

    for multiAlpha in multiAlphas:
        multiAlphaFreq = MultiAlphaFreq(multiAlpha, 0)
        for prefix in prefixes:
            alphaFreqs = getAlphaFreqsFromPrefix(prefix)
            for alpha in multiAlpha:
                multiAlphaFreq.freq += alphaFreqs[ord(alpha) - ord('a')].freq
        multiAlphaFreqs.append(multiAlphaFreq)

    return multiAlphaFreqs
'''
for line in ancFile.readlines():
    lines = line.split( '\t')
    word = lines[0]
    freq = int( lines[3])

    chk = 1

    if not re.match(r"^[a-z]+$", word):
        continue

    if word in ancDict.keys():
        ancDict[word] += freq
    else:
        ancDict[word] = freq

    if len( ancDict) == 15000:
        break

mackenzieFile = file('static/js/corpus/mackenzie.js')
filteredMackenzieFile = file('static/js/corpus/mackenzie_filtered.js', 'w')
filteredMackenzie = []
wordNotIn = []

filteredMackenzieFile.write('var mackenzies = [\n')

for line in mackenzieFile.readlines():
    if '[' in line or ']' in line:
        continue
    lines = line.replace('"', '').replace(',', '').lower().split()
    chk = 1
    for word in lines:
        if word not in ancDict.keys():
            chk = 0
            wordNotIn.append(word)
            break
    if chk == 1:
        filteredMackenzie.append(line)
        filteredMackenzieFile.write(line)

filteredMackenzieFile.write('];')
mackenzieFile.close()
filteredMackenzieFile.close()

'''
print(ancDict.keys())
print(filteredMackenzie)
print(len(filteredMackenzie))
print(wordNotIn)
'''

print "load json object"
key_0 = json.load( open( 'hash/key_0.txt'))
key_1 = json.load( open( 'hash/key_1.txt'))
key_2 = json.load( open( 'hash/key_2.txt'))
key_3 = json.load( open( 'hash/key_3.txt'))
word_0 = json.loads(open( 'hash/word_0.txt').read().decode('cp1252'))
word_1 = json.loads(open( 'hash/word_1.txt').read().decode('cp1252'))
word_2 = json.loads(open( 'hash/word_2.txt').read().decode('cp1252'))
word_3 = json.loads(open( 'hash/word_3.txt').read().decode('cp1252'))
print "done"
