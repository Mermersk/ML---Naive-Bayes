#Main pythin script, so far not used at all. Author: Isak Steingrimsson
import csv
import pandas
import numpy
testFile = open("dataset/test.csv", "r", encoding = "utf8")
testFileReader = csv.reader(testFile, delimiter = ",")

#Read csv file to a dataframe data-structure
df = pandas.read_csv("dataset/test.csv", encoding = "utf8")
#print(df.head())
print(df.shape)

print(str(df.get("text")))
#def hello():
 #   t = 45
  #  strin = "hello world " + str(t)
   #return strin


#print(hello())

#with testFile as File:  
    #for row in testFileReader:
        #print(row)

#with open('dataset/test.csv') as File:
    #reader = csv.reader(File, delimiter=',')
    #for row in reader:
        #print(row)



