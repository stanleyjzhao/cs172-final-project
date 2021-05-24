import re
import os
import zipfile
import sys
from math import sqrt
from parsing import get_term_key
from parsing import get_term_val
from parsing import get_main_key
from parsing import get_main_val
from parsing import get_doc_key
from parsing import get_doc_val
from parsing import get_map
from parsing import get_termInfo

term_key_list = get_term_key()
term_val_list = get_term_val()

main_key_list = get_main_key()
main_val_list = get_main_val()

doc_key_list = get_doc_key()
doc_val_list = get_doc_val()

map = get_map()

termInfo = get_termInfo()

def getTermID(word):
    for term in term_val_list:
        if word == term:
            return term_key_list[term_val_list.index(word)]

def getDocID(document):
    for doc in doc_val_list:
        if document == doc:
            return doc_key_list[doc_val_list.index(document)]

def getTermFromID(termID):
    return term_key_list[termID - 1]

def checkForItem(docID, termID):
    keys = map.keys()
    if docID in keys:
        for item in map[docID]:
            # print(item)
            if item[0] == termID:
                return True
    return False

def cosSim(qWeights, dWeights):
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(len(qWeights)):
        numerator += (qWeights[i] * dWeights[i])
        denominator1 += (qWeights[i])
        denominator2 += (dWeights[i])
    denominator = denominator1 * denominator2
    denominator = sqrt(denominator)
    if denominator != 0:
        cosSim = numerator / denominator
    else:
        cosSim = 0
    return cosSim