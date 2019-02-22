#Main pythin script. Author: Isak Steingrimsson
import csv
import pandas
import numpy
import clean2 as cleanse #Cleaning script
from nltk.corpus import stopwords

#Setting field size limit to 1mb, else we get field size to large error
csv.field_size_limit(1000000) 

#The set of stopwords, will be used to detect non-english articles and to remove stop words
stopWords = set(stopwords.words("english"))

#cleanse.firstPassCleanse("dataset/train.csv", "out.csv", stopWords)


cleanse.secondPassCleanse("out.csv", "out2.csv", stopWords)