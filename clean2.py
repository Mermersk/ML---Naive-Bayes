#New cleaning script
import csv  #csv module
import re   #Regex module
from nltk.corpus import stopwords

csv.field_size_limit(1000000)

File = open("dataset/train.csv", "r", encoding = "utf8")
FileReader = csv.reader(File, delimiter = ",")

dictReader = csv.DictReader(File)

w = csv.DictWriter(open("out.csv", "w", encoding="utf8"), fieldnames=["id","title","author","text","label"])
w.writeheader()

#print(FileReader.keys())

stopWords = set(stopwords.words("english"))
print(stopWords)

for row in dictReader:
    article = row["text"]
    string_length = len(article)
    if string_length < 20:
        continue

    stopword_counter = 0
    for word in row["text"].split(" "):
        if word in stopWords and word != "a":
            stopword_counter += 1

    if stopword_counter <= 50:
        continue

    w.writerow(row)
    
    #print(type(article))
    #print(len(article))

#for row in FileReader:
    #print(row[0:10])