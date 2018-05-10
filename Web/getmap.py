from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import unirest


with open('./concretenouns') as f: 
    words = f.readlines()
wordList = [word.strip('\n') for word in words]


def getAsso(word): 
    response = unirest.post("https://twinword-word-associations-v1.p.mashape.com/associations/",
        headers={
            "X-Mashape-Key": "YOUR_API_KEY",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        params={
            "entry": word
        }
    )
    return response.body
def getType(word): 
    if "-" in word: 
        word.replace('-', ' ')
    response = getAsso(word)
    assoList = []
    if 'associations_array' in response: 
        assoList = response['associations_array']
    typeList = getTypeList(word)
    assoTypeList = []
    for asso in assoList: 
        assoTypeList.extend(getTypeList(asso))
    for assoType in assoTypeList: 
        if assoType in typeList: 
            typeList.append(assoType)
    return mostCommon(typeList)
def getTypeList(word): 
    response = unirest.get("https://wordsapiv1.p.mashape.com/words/" + word,
        headers={
            "X-Mashape-Key": "YOUR_API_KEY",
            "Accept": "application/json"
        }
    )
    typeList = []
    if 'results' not in response.body: 
        return 'NaN'
    for result in response.body['results']: 
        if 'typeOf' in result: 
            typeList.extend(result['typeOf'])
    for i in range(len(typeList)): 
        typeList[i] = typeList[i].split(' ')[-1]
    return typeList
def mostCommon(lst): 
    return max(set(lst), key=lst.count)
def getStem(word): 
    ps = PorterStemmer()
    return ps.stem(word)
def getTypeDict(): 
    typeDict = {}
    pBar = progressbar.ProgressBar()
    for word in pBar(wordList): 
        typeDict[getStem(word)] = getType(word)
    return typeDict

stemList = [getStem(word) for word in wordList]
