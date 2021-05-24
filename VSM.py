import re
import os
import zipfile
import sys
from parsing import get_term_key
from parsing import get_term_val
from parsing import get_main_key
from parsing import get_main_val
from parsing import get_doc_key
from parsing import get_doc_val
from parsing import get_map
from parsing import get_termInfo
from read_index import getTermID
from read_index import getDocID
from read_index import getTermFromID
from read_index import checkForItem
from read_index import cosSim

term_key_list = get_term_key()
term_val_list = get_term_val()

main_key_list = get_main_key()
main_val_list = get_main_val()

doc_key_list = get_doc_key()
doc_val_list = get_doc_val()

map = get_map()
termInfo = get_termInfo()
queryDict = {}
cosSimDict = {}

queryfile = ""
outputfile = ""

if not(len(sys.argv) == 3): 
    raise ValueError("Please run with two file names in the format 'python3 VSM.py query_list.txt output_file.txt'")
queryfile = sys.argv[1]
outputfile = sys.argv[2]

stop_file = open("stopwords.txt", "r")
temp_stopwords = stop_file.readlines()
stopwords = []
for word in temp_stopwords:
    stopwords.append(word.replace("\n", ""))
stop_file.close()

query_list = open(queryfile, 'r')
lines = query_list.readlines()
# Populates queryDict where key = query number and val = each word of query 
for line in lines:
    line = re.sub("[^0-9a-zA-Z ]+", "", line)
    line = line.lower()
    word_list = line.split()
    word_list = [i for i in word_list if i not in stopwords] # Source of this line: https://www.techiedelight.com/remove-all-occurrences-item-list-python/
    queryDict[word_list[0]] = word_list[1:]

for query in queryDict:
    for docNum in doc_key_list:
        viewList = []
        qWeights = []
        dWeights = []
        for word in queryDict[query]:
            if word not in viewList:
                viewList.append(word)
                qWeights.append(1)
                if checkForItem(docNum, getTermID(word)):
                    dWeights.append(1)
                else:
                    dWeights.append(0)
        if docNum in map.keys():
            for entry in map[docNum]:
                word = getTermFromID(entry[0])
                if word not in viewList:
                    viewList.append(word)
                    dWeights.append(1)
                    qWeights.append(0)
        intcosSim = cosSim(qWeights, dWeights)
        if (query in cosSimDict):
            cosSimDict[query].append(intcosSim)
        else:
            cosSimDict[query] = [intcosSim]

fileOut = open(outputfile, "w")

for entry in cosSimDict:
    maxValues = {}
    for i in range(10):
        maxVal = 0
        maxIndex = 0
        for val in cosSimDict[entry]:
            if val > maxVal:
                maxVal = val
                maxIndex = cosSimDict[entry].index(val)
        if maxVal == 0:
            break
        line = str(entry) + " Q0 " + str(doc_val_list[doc_key_list.index(maxIndex + 1)]) + " " + str(i + 1) + " " + str(maxVal) + " Exp\n"
        fileOut.write(line)
        cosSimDict[entry].remove(maxVal)
fileOut.close()