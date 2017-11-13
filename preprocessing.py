import LanguageModelMulti
import json

PREFIX = 3

with open('hash/word_' + str(PREFIX) + '.txt', 'w') as fb:
    word_json = LanguageModelMulti.getPrefixWordDictFromPrefixLength(PREFIX)
    json.dump(word_json, fb, indent=2)

with open('hash/key_' + str(PREFIX) + '.txt', 'w') as fb:
    key_json = LanguageModelMulti.getStaticMultiAlphaDictFromPrefixLength(PREFIX)
    json.dump(key_json, fb, indent=2)
