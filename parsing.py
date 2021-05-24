import re
import os
import zipfile
import sys

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
termIndexMap = {}
docIndexMap = {}
termIndexMapCount = 1
docIndexCount = 1
map = {}
termInfo = {}


with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
# allfiles = allfiles[0:1]
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
        # Creates a list of stopwords
        stop_file = open("stopwords.txt", "r")
        temp_stopwords = stop_file.readlines()
        stopwords = []
        for word in temp_stopwords:
            stopwords.append(word.replace("\n", ""))

        stop_file.close()
        

        
        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            text = text.lower()
            # Regex removes punctuation
            text = re.sub(r'[^\w\s]','',text)
            text = text.split()
            # Nested loops remove stop-words
            for term in stopwords:
                for word in text:
                    if word == term:
                        text.remove(word)

            # step 2 - create tokens 
            #Add document ID and name to docIndexMap
            docIndexMap[docIndexCount] = docno

            locationCount = 1
            for word in text:
                if word not in termIndexMap.values():
                    termIndexMap[termIndexMapCount] = word
                    termIndexMapCount += 1
            
                key_list = list(termIndexMap.keys())
                val_list = list(termIndexMap.values())
                position = val_list.index(word)
                newEntry = tuple([key_list[position], docIndexCount, locationCount])
                locationCount += 1
                
                if docIndexCount in map.keys():
                    map[docIndexCount].append(newEntry)
                else:
                    map[docIndexCount] = [newEntry]

            docIndexCount += 1 

main_key_list = list(termInfo.keys())
main_val_list = list(termInfo.values())

doc_key_list = list(docIndexMap.keys())
doc_val_list = list(docIndexMap.values())

def get_term_key():
    return key_list

def get_term_val():
    return val_list

def get_main_key():
    return main_key_list

def get_main_val():
    return main_val_list

def get_doc_key():
    return doc_key_list

def get_doc_val():
    return doc_val_list

def get_map():
    return map

def get_termInfo():
    return termInfo