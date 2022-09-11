
# MODULE to find Target of the phish from Twitter report text

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time

def find_phish_target(tweet_text):

  with open('targets.txt') as f: # A list of pre-defined targets
    targets = [line.rstrip('\n') for line in f]
  while("" in targets) :
    targets.remove("")

  #print(targets)

  stop_words = set(stopwords.words('english'))
  word_tokens = word_tokenize(tweet_text)
    
  tokenized_terms = [w for w in word_tokens if not w.lower() in stop_words]
    
  tokenized_terms = []
    
  for w in word_tokens:
      if w not in stop_words:
          tokenized_terms.append(w)

  tokenized_terms = [i.lower() for i in tokenized_terms]

  for i in targets:
    j=0
    while j<len(tokenized_terms):

      if i in tokenized_terms[j]:
        target=i
        return target
      j=j+1
    

# DEBUG

#find_phish_target("Another one.@RevokeCash @wallet_guard @Sunrise_WTF @MetaMaskSupport")


    
     
