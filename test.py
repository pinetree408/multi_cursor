import LanguageModelMulti
import time
import json

def get_maximum_word_length():
    with open('static/mackenzie.js', 'r') as fb:
        read_lines = fb.readlines()
        maximum = 0
        for line in read_lines:
            words = line.split(' ')
            for word in words:
                if len(word) > maximum:
                    maximum = len(word)
        print maximum

input_data = ['bit', 'dev', 'hs']

start_time = time.time()
print( LanguageModelMulti.getWordsFromMultiAlphaPrefix( ['bit', 'dev']))
print time.time() - start_time
