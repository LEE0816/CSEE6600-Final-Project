from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import getmap
from google_images_download import google_images_download
import shutil, os
from progressbar import *

def searchImage(word):
    stopWords = set(stopwords.words('english'))
    index = 1
    pbar = ProgressBar()
    exams = []
    while 1:
        try:
            exams.append(wn.synset(word + '.a.' + str(index)).examples())
            index += 1
        except:
            if index == 1:
               exams.append(str(word)) 
            break

    choices = range(100)
    examOrig = ''

    print 'Extracting words...'
    for i in pbar(range(len(exams))):
        if i in choices:
            for example in exams[i]:
                examOrig += example + ' '
    if index == 1: 
        examOrig = exams[i]
    examTokens = word_tokenize(examOrig)
    examFilter = [w for w in examTokens if not w in stopWords]

    if index != 1: 
    	examFilter = [w for w in examTokens if not getmap.getStem(w) == getmap.getStem(word)]
    examFilter = list(set(examFilter))

    print 'Mapping keywords...'
    obj = ''
    objType = ''
    mapped = []
    pbar2 = ProgressBar()

    for i in pbar2(range(len(examFilter))):
        exam  = examFilter[i]
        if getmap.getStem(exam) in getmap.stemList:
            obj = exam
            objType = getmap.getType(exam)
            mapped.append(exam)

    print mapped
    searchword  = word + " " + obj + " as a " + objType
    


    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": searchword, "limit": 20, "print_urls": False, "metadata": False}
    response.download(arguments)
    # delete original folder
    shutil.rmtree("static/img/downloads")
    # move folder
    shutil.move("downloads", "static/img/downloads")


    fileIdx = 1
    for file in os.listdir('static/img/downloads/'+str(searchword)):   
        new_name = str(fileIdx) + file[-4:] 
        os.rename('static/img/downloads/'+str(searchword) + '/' + file, 'static/img/downloads/'+str(searchword) + '/' + new_name)
        fileIdx+=1



    L = []
    for root, dirs, files in os.walk("static/img/downloads"):
        for file in files:
            L.append(os.path.join(root, file))
    L.insert(0,[str(searchword)])
    return L












