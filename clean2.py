#New cleaning script
import csv  #csv module
import re
#Setting field size limit to 1mb, else we get field size to large error
csv.field_size_limit(1000000) 

#The set of stopwords, will be used to detect non-english articles and to remove stop words

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

        #Unfortunately it seems spanish and english share some stopwords, so I use another method for removing spanish articles by checking for "á"    
        if spanish != -1:
            continue

        #If there is less than 5 stopwords in the article it is probably not english,
        #I use the continue statement so that this article does not reach writerow function to our new csv
        if stopword_counter <= 5:
            continue

        #Write rows that pass tests to new cleaned csv
        dictWriter.writerow(row)

    File.close()


def secondPassCleanse(fileInn, fileOut, stopWords):
    
    File = open(fileInn, "r", encoding = "utf8")

    #Initiate our file to a ordered dictionary
    dictReader = csv.DictReader(File)
    
    #Opening up writer for spitting out new csv file
    dictWriter = csv.DictWriter(open(fileOut, "w", encoding="utf8"), fieldnames=["id","title","author","text","label"])
    dictWriter.writeheader()
    
    for row in dictReader:
        article = row["text"]
        #Seperate article to distinct words, returns a list of words
        single_words = article.split(" ")
        new_article = ""
        
        for word in single_words:
            
            single_word = word
            #Breaks every word into an individual letter, if it is something other than a letter we take it out.
            for char in single_word:
                #print(char)
                is_alpha = char.isalpha()
                if is_alpha == False:
                    single_word = single_word.replace(char, " ")
            #print(single_word)
            #Put every word to lowercase
            single_word = single_word.lower()
            
            #if word length is 0 or 1, then we continue since we dont want it
            if len(single_word) <= 1:
                continue


            #Checking for stopwords in the text if current word is stopword we continue since we dont want it in the new article text
            if single_word in stopWords:
                continue
            
            new_article = new_article + single_word + " "
        """
        Hopefully when we get here there are only words in article but no ".", ",", "-" and so on.
        This regex matches matches with every non-english letter, So if the result is something else than None
        it means that we got a hit, we dont want those articles so we skip them. We only want English! The regex is the ASCI table
        """
        if re.search("[^\x00-\x7F…]", new_article) != None:
            continue
        #print(new_article)
        row["text"] = new_article
        #print(article + "***************************************************************")
        dictWriter.writerow(row)

    File.close()
        

        