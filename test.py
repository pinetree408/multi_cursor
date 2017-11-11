import LanguageModelMulti
import time
import json

input_data = ['bit', 'dev', 'hs']

start_time = time.time()
print( LanguageModelMulti.getStaticMultiAlphasFromPrefix(input_data))
print time.time() - start_time

start_time = time.time()
print( LanguageModelMulti.getWordsFromMultiAlphaPrefix(input_data))
print time.time() - start_time

start_time = time.time()
print(LanguageModelMulti.PREFIXLEN_THREE[json.dumps(input_data)])
print time.time() - start_time
