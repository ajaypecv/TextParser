# TASK 1
from helper_functions import Rcv1Doc
import glob, os
import string
from stemming.porter2 import stem
import math
from helper_functions import read_stop_words

"""
The helper_functions has been imported.
This contains the necessary requirements for TASK 1.1
"""
# Creating object to call Rcv1Doc class
rcvdoc = Rcv1Doc()

def parse_rcv1v2(inputpath, stop_words):
    rcv_collection = {}
    os.chdir(inputpath)
    for document in glob.glob("*.xml"):
        document = open(document, "r")
        file = document.readlines()
        document.close()

        # creating an empty list to store all words in the document
        words = []

        # parsing the document content
        # Here we take only content between the words <text> and </text> in the xml file
        text_lines = [line.strip("</p>\n") for line in file if line.startswith("<p>")]

        # TOKENIZATION
        # Word is defined as any sequence of alphabetic characters, terminated by a space or special character,
        # with everything converted to lower-case and has length 2
        for line in text_lines:
            line = line.translate(str.maketrans('', '', string.digits))  # removing numeric characters
            line = line.translate(
                str.maketrans(string.punctuation, ' ' * len(string.punctuation)))  # removing punctuation

            for term in line.split():
                words.append(term)

        # creating RCV1Words object
        rcv1Doc = Rcv1Doc()
        # adding terms
        rcv1Doc.addTerm(words, stop_words)

        # setting the document length for each word
        rcv1Doc.set_doc_len(len(words))
        # maps document id's to its objects easy for indexing documents with ID as key.
        rcv_collection[rcv1Doc.getdocID(file)] = rcv1Doc

    return (rcv_collection)


def parse_query(query0, stop_words):
    # Tokenization
    # Removing punctuation marks and numeric characters.
    rcv_line = query0.translate(str.maketrans('', '', string.digits))
    rcv_line = rcv_line.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

    # Splitting the query terms
    words = rcv_line.split()

    # creating RCV1Words object to get the frequency of index terms
    rcvdoc = Rcv1Doc()
    rcvdoc.addTerm(words, stop_words)
    return (rcvdoc.get_terms())

def main_path(input_path,stop_words):
    file = open("Ajay Krishnan Chelora Veetil_Q1.txt", "w")
    collection = parse_rcv1v2(input_path, stop_words)
    for rcv in collection.items():
        docID = rcv[0]

        # Accessing the Rcv1Words object
        rcv1Doc = rcv[1]
        index_dic = rcv1Doc.get_terms()  # dictionary with term: frequency

        # Sorting the dictionary in descending order of frequency
        new_dict = dict(sorted(index_dic.items(), key=lambda item: item[1], reverse=True))

        # getting document length
        doclen = rcv1Doc.get_doc_len()

        # Writing into the text file
        file.write("Document " + docID + " contains " + str(len(index_dic.values())) +
                   " indexing terms and have total " + str(doclen) + " words\n")
        for (k, v) in new_dict.items():
            file.write(k + ": " + str(v) + "\n")
        file.write("\n")
    file.close()
    
    
curr_path = os.getcwd() #getting current path
print("THE CURRENT DIRECTORY IS "+ curr_path)
data_path = os.path.join(curr_path, 'RCV1v2')
print("DATA PATH IS "+data_path)
collection = parse_rcv1v2(data_path, read_stop_words())
os.chdir(curr_path)
main_path(data_path,read_stop_words())    

