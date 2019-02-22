#New cleaning script
import csv  #csv module
import re   #Regex module
from nltk.corpus import stopwords

#Setting field size limit to 1mb, else we get field size to large error
csv.field_size_limit(1000000) 



#The set of stopwords, will be used to detect non-english articles and to remove stop words
stopWords = set(stopwords.words("english"))
print(stopWords)

def firstPassCleanse(fileInn, fileOut, stopWords):

    File = open(fileInn, "r", encoding = "utf8")

    #Initiate our file to a ordered dictionary
    dictReader = csv.DictReader(File)

    #Opening up writer for spitting out new csv file
    dictWriter = csv.DictWriter(open(fileOut, "w", encoding="utf8"), fieldnames=["id","title","author","text","label"])
    dictWriter.writeheader()

    for row in dictReader:
        #article is a string of each text field
        article = row["text"]
        string_length = len(article)
        #This should get rid of empty fields
        if string_length < 20:
            continue

        stopword_counter = 0
        #Splitting each article into single words
        for word in article.split(" "):
            if word in stopWords:
                stopword_counter += 1

            spanish = word.find("á")
            if spanish != -1:
                break

        #Unfortunately iy seems spanish and english share some stopwords, so I use another method for removing spanish articles by checking for "á"    
        if spanish != -1:
            continue

        #If there is less than 25 stopwords in the article it is probably not english,
        #I use the continue statement so that this article does not reach writerow function to our new csv
        if stopword_counter <= 25:
            continue

        #Write rows that pass tests to new cleaned csv
        dictWriter.writerow(row)


def secondPassCleanse(fileInn, fileOut, stopWords):
    
    File = open(fileInn, "r", encoding = "utf8")

    #Initiate our file to a ordered dictionary
    dictReader = csv.DictReader(File)

    #Opening up writer for spitting out new csv file
    dictWriter = csv.DictWriter(open(fileOut, "w", encoding="utf8"), fieldnames=["id","title","author","text","label"])
    dictWriter.writeheader()
    
    for row in dictReader:
        article = row["text"]
        #print(article)
        for char in article:
            print(char)



        