# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
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
# print(map)

termInfo = get_termInfo()

# print(len(sys.argv))
# if not(len(sys.argv) == 3 or len(sys.argv) == 5): 
#     raise ValueError('Please provide a query, either --term TERM or --doc DOCNAME or both.')

# FIXME: print distinct terms (optional), auto-uppercase the document argument
# if sys.argv[1] == '--doc' and len(sys.argv) <= 3:
#     sys.argv[2] = sys.argv[2].upper()
#     print("Listing for document: ", sys.argv[2])
#     docID = 0
#     termCount = 0
#     for docname in doc_val_list:
#         if sys.argv[2] == docname:
#             position = doc_val_list.index(docname)
#             docID = doc_key_list[position]
#     print("DOCID: ", docID)

#     for entry in map:
#         if entry[1] == docID:
#             termCount += 1 
#     print("Total terms: ", termCount)
# # FIXME: stem term
# elif sys.argv[1] == '--term' and len(sys.argv) <= 3:
#     print("Listing for term: ", sys.argv[2])
#     termID = 0
#     for term in term_val_list:
#         if(sys.argv[2] == term):
#             position = term_val_list.index(term)
#             termID = term_key_list[position]
#     print("TERMID: ", termID)
#     # print(termInfo[termID])
#     print("Number of documents containing term: ", termInfo[termID][0][1])
#     print("Term frequency in corpus: ", termInfo[termID][0][0])
# # FIXME: auto-uppercase doc argument, create valuerror outputs for incorrect inputs
# elif (sys.argv[1] == '--doc' and sys.argv[3] == '--term') or (sys.argv[1] == '--term' and sys.argv[3] == '--doc'):
#     if sys.argv[1] == '--doc' and sys.argv[3] == '--term':
#         print("Please put your query in the order --term TERM --doc DOCNAME")
#         sys.exit()
#     termID = 0 
#     docID = 0
#     sys.argv[4] = sys.argv[4].upper()
#     print("Listing for term: ", sys.argv[2])
#     print("In document: ", sys.argv[4])
#     for term in term_val_list:
#         if(sys.argv[2] == term):
#             position = term_val_list.index(term)
#             termID = term_key_list[position]
#     print("TERMID: ", termID)
#     for docname in doc_val_list:
#         if sys.argv[4] == docname:
#             position = doc_val_list.index(docname)
#             docID = doc_key_list[position]
#     print("DOCID: ", docID)

#     smallList = termInfo[termID][0][2].items()
#     newTuple = ()
#     for key,freq in smallList:
#        if key == docID:
#            newTuple = (key,freq)
#     # print(newTuple)

#     print("Term frequency in document: ", newTuple[1][0])
#     print("Positions: ", newTuple[1][1])

def getTermID(word):
    for term in term_val_list:
        # print(term)
        if word == term:
            # print(term_key_list[term_val_list.index(word)])
            # print(term)
            return term_key_list[term_val_list.index(word)]

def getDocID(document):
    for doc in doc_val_list:
        if document == doc:
            # print(doc_key_list[doc_val_list.index(document)])
            # print(doc)
            return doc_key_list[doc_val_list.index(document)]

def getTermFromID(termID):
    # print(len(term_key_list))
    # print(termID)
    return term_key_list[termID - 1]

def checkForItem(docID, termID):
    for item in map:
        # print(item[0])
        if item[1] > docID:
            return False
        if item[1] == docID:
            # print("found matching doc")
            if item[0] == termID:
                # print("returning true")
                return True
    return False

def cosSim(qWeights, dWeights):
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(len(qWeights)):
        numerator += qWeights[i] * dWeights[i]
        denominator1 += (qWeights[i] ** 2)
        denominator2 += (dWeights[i] ** 2)
    denominator = denominator1 * denominator2
    denominator = sqrt(denominator)
    cosSim = numerator / denominator
    # print(cosSim)
    return cosSim