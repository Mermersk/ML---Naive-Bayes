#Main python script. Author: Isak Steingrimsson
import csv
import pandas
import numpy
import time
import re
import math
import sys
import clean2 as cleanse #Cleaning script
#from nltk.corpus import stopwords
from collections import defaultdict

start = time.time()

#Setting field size limit to 1mb, else we get field size to large error
csv.field_size_limit(1000000) 

#The set of stopwords, will be used to detect non-english articles and to remove stop words
#stopWords = set(stopwords.words("english"))

#cleanse.firstPassCleanse("dataset/train.csv", "dataset/clean_train.csv", stopWords)

#cleanse.secondPassCleanse("dataset/clean_train.csv", "dataset/final_clean_train.csv", stopWords)

def createVocabulary():

    File = open("dataset/final_clean2_train.csv", "r", encoding = "utf8")
    dictReader = csv.DictReader(File)
    #Creating a new empty set. An set can not contain duplicates and is unordered
    word_set = set()
    #word_set.add("fg")
    vocab = open("Vocabulary.txt", "w", encoding = "utf8")

    for row in dictReader:
        article = row["text"]
        single_words = article.split(" ")

        for word in single_words:
            #Remove any before or trailing whitespaces
            stripped_word = word.strip()
            word_set.add(stripped_word)  

    for word in word_set:
        vocab.write(word + "\n")
            
    File.close()
    vocab.close()

#createVocabulary()

end = time.time()
#print("It took so many seconds: " + str(end - start))
"""
We will  nedd to estimate two sets of parameters from the train.csv
to build our classifier.

The first task is to calculate the prior probabilites of each class.
0 = is reliable news
1 = is unreliable news

To find this we need to count how many fake/real news article there are in the 
dataset and calulate how prevelant each is.
"""

#-------------------------------------------------------

#Paths to our dataset and vocabulary
csvFile = "dataset/final_clean_train.csv"
vocabularyFile = "Vocabulary.txt"

def calculatePriorProbabilities(csvPath):
    #Classes are fakeNews and realNews
    fakeNewsCount = 0.0
    realNewsCount = 0.0
    totalNewsCount = 0.0

    File = open(csvPath, "r", encoding = "utf8")
    #Initiate our file to a ordered dictionary
    dictReader = csv.DictReader(File)

    for row in dictReader:
        c = int(row["label"])
        #print(c)
        totalNewsCount = totalNewsCount + 1.0
        if (c == 0):
            realNewsCount = realNewsCount + 1.0
        if (c == 1):
            fakeNewsCount = fakeNewsCount + 1.0

    fakeNewsPrior = fakeNewsCount/totalNewsCount
    realNewsPrior = realNewsCount/totalNewsCount
    print("fakeNewsCount: %d  realNewsCount: %d totalNewsCount %d" %(fakeNewsCount, realNewsCount, totalNewsCount))
    print("fakeNewsPrior: %f  realNewsPrior: %f" %(fakeNewsPrior, realNewsPrior))
    return fakeNewsPrior, realNewsPrior

fakeNewsPrior, realNewsPrior = calculatePriorProbabilities(csvFile)
# P(y=0) = realNewsPrior
# P(y=1) = fakeNewsPrior


def countWords(csvPath, vocabularyPath):
 
    vocabularyFile = open(vocabularyPath, "r", encoding = "utf8") 
    #Read in each word from the vocabulary, vocabWords is a list of the words. Use read + splitlines so i dont get newline \n
    #Make a set out of the vocabulary(usefull for later)
    vocabWords = vocabularyFile.read().splitlines()
    vocabSet = set(vocabWords)
    #print(len(vocabWords))
    
    #Read in the dataset
    File = open(csvPath, "r", encoding = "utf8")
    dictReader = csv.DictReader(File)
    
    """
    wordsCount is a dictionary containing 2 other default-dictionaries. The key to access either one of these default-dictionaries
    is 0 or 1. These represent articles either in the realnews class 0 or fakenews class 1.
    Defaultdict is different from regular dictionary in that if you set/lookup with a key that is nonexistant it will give you a
    default value, the result from the anonymous function, which in this case is 0. This means it will never raise an keyError.
    """
    wordsCount = {
        0: defaultdict(lambda: 0),
        1: defaultdict(lambda: 0),
        2: defaultdict(lambda: 0),
        3: defaultdict(lambda: 0)
    }
    wordsTotal = defaultdict(lambda: 0)

    for row in dictReader:
        #print(row["title"])
        #c stands for Class, either 0 or 1
        c = int(row["label"])
        #print("Label: y=%s" % c)
        articleWords = set(row["text"].split(" "))
        #Intersection will leaves with only the words that are both in articleWords and in the vocabulary, this makes it easy to calculate how often it appears
        articleVocab = articleWords.intersection(vocabSet)
        #print("Article words in vocabulary: %s" % len(articleVocab))
        #print("Words: " + " ".join(articleVocab))
        for w in articleVocab:
            """
            wordsCount is how often the words appear in either class 0 or 1.
            c = 0 or 1, w = a one word string(the word) as a key and value as number of times it appears.

            index 2 and 3 are for how many words are in the articles where w word appears. 2 is where label is 0(realnews), 3 is where label is 1(fakenews)
            """
            wordsCount[c][w] += 1
            if c == 0:
                wordsCount[2][w] += len(articleWords)
                print(w + "  " + str(wordsCount[2][w]))
            if c == 1:
                wordsCount[3][w] += len(articleWords) 
                print(w + "  " + str(wordsCount[3][w]))
            #wordsTotal is how often w word appears in all of the dataset, key = string, value = int
            wordsTotal[w] += 1
    debugword = "multinational"
    #print("How often word appears in article with label 1: " + str(wordsCount[1][debugword]) + "   How often word appears with no regards to label: " + str(wordsTotal[debugword]))
    #print("How many words are in articles where the word is and has label 1: " + str(wordsCount[3][debugword]) + "How many words are in articles where the word is and has label 0: " + str(wordsCount[2][debugword]))
    
    return wordsCount, vocabSet

wordsCount, vocabSet = countWords(csvFile, vocabularyFile)
#print(len(wordsCount[3])) 

def createVocabularyWithProbabilities(wordsCount, vocabSet):
    vocab = open("VocabularyWithProb.txt", "w", encoding = "utf8")   

    for word in vocabSet:
        #print(word)
        #print("appears with label 0: " + str(wordsCount[0][word]))
        #print("appears with label 1: " + str(wordsCount[1][word]))
        #print("size of articles where word appears with label 0: " + str(wordsCount[2][word]))
        #print("size of articles where word appears with label 1: " + str(wordsCount[3][word]))

        if wordsCount[0][word] > 0:
            probA = wordsCount[0][word] / wordsCount[2][word]
        else:
            probA = 0.0

        if wordsCount[1][word] > 0:
            probB = wordsCount[1][word] / wordsCount[3][word]
        else:
            probB = 0.0
            

        vocab.write(word + "\n" + str(probA) + "\n" + str(probB) + "\n")
    vocab.close()
        



#createVocabularyWithProbabilities(wordsCount, vocabSet)

#Function to multiply many numbers together, expected input is list of floats.
def product(l):
    r = 1.0
    for v in l:
        #obs: temporary "fix", I think it should be multiplication, see my text hand in.
        r += v
    return r


def bayes(text):
    # Calculates P(y=1|text), that is how likely given text is fake news.
    vocabFile = open("vocabularyWithProb.txt", "r", encoding = "utf8")
    vocabWords = vocabFile.read().splitlines()
    textWords = text.split(" ")

    relevantWords = []
    relevantWordsP0 = []
    relevantWordsP1 = []
    
    #print(textWords)
    #print(vocabWords)
    for textWord in textWords:
        if textWord in vocabWords:
            print(textWord)
            #Geting index of word in vocab, index + 1 = P(0), index + 2 = P(1)
            vocabIndex = vocabWords.index(textWord)
            relevantWords.append(textWord)
            relevantWordsP0.append(float(vocabWords[vocabIndex + 1]))
            relevantWordsP1.append(float(vocabWords[vocabIndex + 2]))
            
    print(relevantWords, relevantWordsP0, relevantWordsP1)
    #print(product(relevantWordsP0))

    #probA and probB are the prpbabilities of all relevant words multiplied together.
    probA = product(relevantWordsP1)
    probB = product(relevantWordsP0)
    #print(probA, probB)
    a = probA * fakeNewsPrior
    b = probB * realNewsPrior
    
    #print(product([0.00023453, 0.00000056, 0.00000459495, 0.0034564, 0.00003455]))
    bayerFinal = a/(a+b)
    print("Result of the classifier(P(1)): " + str(bayerFinal))

    #return a/(a+b)
bayes(sys.argv[1])
#def calculateErrorRate():
