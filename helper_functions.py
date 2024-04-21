import glob, os
import string
from stemming.porter2 import stem
import math

class Rcv1Doc:
    def __init__(self):
        self.docID = ""
        self.terms = {}
        self.doc_len = 0

    # method to get the document ID of the given file
    def getdocID(self, file):
        docid_line = [line.split() for line in file if line.startswith("<newsitem")]

        for terms in docid_line[0]:
            if terms.startswith("itemid"):
                docID = terms.strip('"itemid=')
        self.docID = docID
        return (docID)

    def addTerm(self, words, stop_words):
        for word in words:

            # Converting terms to lower case and applying porter2 stemming algorithm
            word = stem(word.lower())

            if len(word) > 2 and word not in stop_words:
                try:
                    self.terms[word] += 1
                except KeyError:
                    self.terms[word] = 1
        return (self.terms)

    def get_terms(self):
        return (self.terms)

    ##Updating as per question 3.1
    # To get the present value of doc_len
    def get_doc_len(self):
        return (self.doc_len)

    # To mutate doc_len value
    def set_doc_len(self, doc_len):
        self.doc_len = doc_len

    def get_terms(self):
        return (self.terms)
    

def read_stop_words():
    # __file__ is the path to the current file.
    # os.path.dirname(__file__) gives the directory in which this file is located.
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Now you join the directory with the file name to get its full path.
    stop_words_file_path = os.path.join(current_dir, 'common-english-words.txt')
    
    with open(stop_words_file_path, 'r') as file:
        stop_words = [line.strip() for line in file.readlines()]

    return stop_words
