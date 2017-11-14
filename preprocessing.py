from LanguageModelMulti import *
import json

PREFIXS = [0]

for PREFIX in PREFIXS:
    print "start: " + str(PREFIX)
    print "set word"
    with open('hash/word_' + str(PREFIX) + '.txt', 'w') as fb:
        word_dict = {}
        if PREFIX == 0:
            word_dict = getWordsFromMultiAlphaPrefix([], 0)
        else:
            word_dict = LanguageModelMulti.getPrefixWordDictFromPrefixLength(PREFIX, 0)
        word_json = json.dumps(word_dict, indent=2, ensure_ascii=False)
        fb.write(word_json)

    print "set key"
    with open('hash/key_' + str(PREFIX) + '.txt', 'w') as fb:
        key_json = {}
        if PREFIX == 0:
            key_json = getMultiAlphasFromMultiAlphaPrefix([], ancDict.keys())
        else:
            key_json = LanguageModelMulti.getStaticMultiAlphaDictFromPrefixLength(PREFIX)
        json.dump(key_json, fb, indent=2)
