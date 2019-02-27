#Main pythin script. Author: Isak Steingrimsson
import csv
import pandas
import numpy
import time
import re
import clean2 as cleanse #Cleaning script
from nltk.corpus import stopwords

start = time.time()

#Setting field size limit to 1mb, else we get field size to large error
csv.field_size_limit(1000000) 

#The set of stopwords, will be used to detect non-english articles and to remove stop words
stopWords = set(stopwords.words("english"))

cleanse.firstPassCleanse("dataset/train.csv", "dataset/clean_train.csv", stopWords)

cleanse.secondPassCleanse("dataset/clean_train.csv", "dataset/final_clean_train.csv", stopWords)

def createVocabulary():

    File = open("dataset/final_clean_train.csv", "r", encoding = "utf8")
    dictReader = csv.DictReader(File)
    #Creating a new empty set. An set can not contain duplicates and is unordered
    word_set = set()
    #word_set.add("fg")
    vocab = open("Vocabulary.txt", "w", encoding = "utf8")

    for row in dictReader:
        article = row["text"]
        single_words = article.split(" ")

        for word in single_words:
            stripped_word = word.strip()
            if len(stripped_word) <= 1:
                continue
            
            if stripped_word.isalpha() == False:
                continue

            #print(stripped_word + "\n")
            #vocab.write(stripped_word + "\n")
            word_set.add(stripped_word)
        #vocab.write("********************************" + "\n")

    for word in word_set:
        vocab.write(word + "\n")


    File.close()
    vocab.close()

createVocabulary()

end = time.time()
print("It took so many seconds: " + str(end - start))

def countWords():
    vocab = open("Vocabulary.txt", "r", encoding = "utf8")
    countedVocab = open("Counted_Vocabulary", "w", encoding = "utf8")

    #for word in vocab:
        #print(word)

    words = vocab.readlines()
    print(words)

    #for w in words:
        #print(w)

    vocab.close()

#countWords()