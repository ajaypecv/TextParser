from helper_functions import Rcv1Doc
import glob, os
import string
from stemming.porter2 import stem
import math
from Task1 import parse_rcv1v2
from helper_functions import read_stop_words

#stop_words = open('common-english-words.txt', 'r') 
#read_stop_words = [line.strip() for line in stop_words.readlines()]

#print("Current Working Directory:", os.getcwd())

rcvdoc = Rcv1Doc()
os.chdir('..')
curr_path = os.getcwd() #getting current path
print("Current Working Directory:", curr_path)

input_path = curr_path+'//RCV1v2' # setting the path

rcv_collection = parse_rcv1v2(input_path, read_stop_words())
os.chdir(curr_path)

def my_df(coll):
    df = {}
    for rcvdoc in coll.items():
        # Accessing the Rcv1 object
        rcvdocWords = rcvdoc[1]
        index_dic = rcvdocWords.get_terms()

        for term in index_dic.keys():
            try:
                df[term] += 1
            except KeyError:
                df[term] = 1
    return (df)

def my_tfidf(rcvdoc, df, ndocs):
    tfidf = {}
    for rcv_docs in rcvdoc.items():
        rcvdocWords = rcv_docs[1]  # RCV1 object
        index_dic = rcvdocWords.get_terms()
        docID = rcv_docs[0]
        weight = {}
        sum = 0
        for k, v in index_dic.items():
            f_id = v
            df_i = df[k]
            sum += ((1 + math.log10(f_id)) * math.log10(ndocs / df_i)) ** 2
        denominator = math.sqrt(sum)
        for k, v in index_dic.items():
            f_td = v
            d_ft = df[k]
            numerator = (1 + math.log10(f_td)) * math.log10(ndocs / d_ft)

            weight[k] = numerator / denominator
        tfidf[docID] = weight
    return (tfidf)

def main_tfidf():
    tfidf_ = my_tfidf(rcv_collection, df, 25)
    file = open("Ajay Krishnan Chelora Veetil_Q2.txt", "w")
    for key, value in tfidf_.items():

        # Sorting the dictionary in descending order of tfidf
        new_dict = {k: v for k, v in sorted(value.items(), key=lambda item: item[1], reverse=True)}


        out = dict(list(new_dict.items())[0:20])

        # writing into the text
        file.write("Document " + str(key) + " contains " + str(len(new_dict)) + " terms. \n")
        for k, v in out.items():
            file.write(k + ":" + str(v) + "\n")
        file.write("\n")
    file.close()

df = my_df(rcv_collection)
y = {k: v for k, v in sorted(df.items(), key=lambda item: item[1], reverse=True)}
file = open("Ajay Krishnan Chelora Veetil_Q2.1.txt", "w")
file.write(
    "There are " + str(len(rcv_collection)) + " documents in this data set and contains " + str(len(df)) + " terms \n")
file.write("The following are the terms’ document-frequency: \n")
for k, v in y.items():
    file.write(k + ":" + str(v) + "\n")
file.close()

# TASK 2
main_tfidf()

