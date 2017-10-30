ancFile = open('ANC-all-count.txt')
ancList = []


class Anc:
    word = ""
    freq = 0

    def __init__(self, word, freq):
        self.word = word
        self.freq = freq


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


#return list of Anc object.
#each Anc has a word and freq of the word.
#the order of list is sorted by freq of the word.
def getAncsFromPrefix(prefix):
    ret = []
    for anc in ancList:
        if anc.word.startswith(prefix):
            ret.append(anc)
    return ret

#return list of word.
#the order of list is sorted by freq of the word.


def getWordsFromPrefix(prefix):
    ancs = getAncsFromPrefix(prefix)

    def cmpAnc(anc1, anc2):
        return cmp(anc1.freq, anc2.freq)
    ancs = sorted(ancs, cmp=cmpAnc, reverse=True)
    return map(lambda anc: anc.word, ancs)

#return lint of AlphaFreq object list.
#each AlphaFreq has single alphabet character and freq of startswith(prefix+alpha).
#the order is not sorted.


def getAlphaFreqsFromPrefix(prefix):
    ancs = getAncsFromPrefix(prefix)
    alphaFreqs = []
    for i in range(26):
        alphaFreq = AlphaFreq(chr(ord('a') + i))
        alphaFreqs.append(alphaFreq)
        for anc in ancs:
            if anc.word.startswith(prefix + alphaFreq.alpha):
                alphaFreq.freq += anc.freq
    return alphaFreqs

#return list of alphabet.
#the order of list is sorted by freq of startswith(prefix+alpha).


def getAlphasFromPrefix(prefix):
    def cmpAlphaFreqs(alphaFreq1, alphaFreq2):
        return cmp(alphaFreq1.freq, alphaFreq2.freq)
    sortedAlphaFreqs = sorted(getAlphaFreqsFromPrefix(
        prefix), cmp=cmpAlphaFreqs, reverse=True)
    return map(lambda alphaFreq: alphaFreq.alpha, sortedAlphaFreqs)

#


def getStaticMultiAlphaFreqsFromMultiAlphaPrefix(multiAlphaPrefix):
    multiAlphas = ['qwe', 'rtyu', 'iop', 'asd', 'fgh', 'jkl', 'zxc', 'vbnm']
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

#


def getStaticMultiAlphasFromPrefix(multiAlphaPrefix):
    def cmpMultiAlphaFreqs(multiAlphaFreq1, multiAlphaFreq2):
        return cmp(multiAlphaFreq1.freq, multiAlphaFreq2.freq)

    sortedMultiAlphaFreqs = sorted(getStaticMultiAlphaFreqsFromMultiAlphaPrefix(
        multiAlphaPrefix), cmp=cmpMultiAlphaFreqs, reverse=True)

    return map(lambda multiAlphaFreq: multiAlphaFreq.multiAlpha, sortedMultiAlphaFreqs)


def getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix):

    prefixes = ['']

    for multiAlpha in multiAlphaPrefix:
        tempMultiInputs = []
        for multiInput in prefixes:
            for alpha in multiAlpha:
                tempMultiInputs.append(multiInput + alpha)
        prefixes = tempMultiInputs

    return prefixes


def getWordsFromMultiAlphaPrefix(multiAlphaPrefix):

    prefixes = getPrefixesFromMultiAlphaPrefix(multiAlphaPrefix)

    ancs = []
    for prefix in prefixes:
        ancs += getAncsFromPrefix(prefix)

    def cmpAnc(anc1, anc2):
        return cmp(anc1.freq, anc2.freq)
    ancs = sorted(ancs, cmp=cmpAnc, reverse=True)
    return map(lambda anc: anc.word, ancs)

for line in ancFile.readlines():
    lines = line.split( '\t')
    word = lines[0]
    freq = int( lines[3])

    chk = 1
    for anc in ancList:
        if word == anc.word:
            anc.freq += freq
            chk = 0
            break

    if chk == 1:
        anc = Anc( lines[0], int( lines[3]))
        ancList.append( anc)

    if len( ancList) == 15000:
        break

#print( getStaticMultiAlphasFromPrefix( ['asd', 'qwe', 'rtyu', 'qwe']))
#print( getWordsFromMultiAlphaPrefix( ['asd', 'qwe', 'rtyu', 'qwe']))

#multiAlphas = ['qwe', 'rtyu', 'iop', 'asd', 'fgh', 'jkl', 'zxc', 'vbnm']

#print( getStaticMultiAlphasFromPrefix( ['asd', 'iop', 'asd', 'zxc']))
#print( getWordsFromMultiAlphaPrefix( ['asd', 'iop', 'asd', 'zxc']))
