#Script for cleaning the dataset of undesirables. Author: Isak Steingrimsson
import csv
import re #Importing the Regex module
import pandas
import numpy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#testFile = open("dataset/test.csv", "r", encoding = "utf8")
#testFileReader = csv.reader(testFile, delimiter = ",")

#Read csv file to a dataframe data-structure
df = pandas.read_csv("dataset/train.csv", encoding = "utf8")
print(df.shape)

vocabulary = open("Vocabulary.txt", "w")

#The set of all english stopwords
stopWords = set(stopwords.words("english"))

#Removes all rows where the text column is empty
df = df.dropna(subset = ["text"])  
print(df.shape)
"""
This next line of code filters out every entry from the text-column that
contains a letter/word not in the ASCI character set(set of characters used in American english).
The regex matches to every non-english character, but I have used the negation sign so that it is reversed.
It does not remove NaN fields, unsure if I should remove those rows or not.
"""
df = df[df["text"].str.contains("^[\x00-\x7F’‘”“—]+", regex = True, na = True)]

#Writes out a new cleaned dataset(csv file)
#clean_csv = df.to_csv(r"C:\Users\Isak\Documents\Skoli\INFO284\dataset\clean_train.csv")

count_row, count_columns = df.shape

#Function for removing stopwords from the dataframe, will inject it into df.apply function
   
#df = df["text"].apply()
#for article in range(0, count_row):
    #for word in stopWords:
        #df["text"].get.str.replace(word, "")
        #df["text"].str.replace(word, "")

        #if df.at[article, "text"] == str:
            #df[df.at[article, "text"].str.replace(word, "")]

article_text = df.get("text")

print(article_text)
print(df.shape)
#for art in range(0, count_row):
 #   print(df.at[art, "text"])
ppp = []
ppp += word_tokenize(str(df["text"]))

print(len(ppp))

for x in range(0, len(ppp)):
    vocabulary.write(ppp[x] + "\n")

vocabulary.close()
