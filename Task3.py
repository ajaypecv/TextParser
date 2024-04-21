"""
This contains all the requirements for Task 3
helper_functions and functions from Task1 and Task2 has been imported as needed.
"""


from helper_functions import Rcv1Doc
import glob, os
import string
from stemming.porter2 import stem
import math
from Task1 import parse_rcv1v2
from Task1 import parse_query
from helper_functions import read_stop_words
from Task2 import my_df

rcvdoc = Rcv1Doc()
#os.chdir('..')
curr_path = os.getcwd() #getting current path
print("Current Working Directory:", curr_path)

input_path = curr_path+'//RCV1v2' # setting the path

rcv_collection = parse_rcv1v2(input_path, read_stop_words())
os.chdir(curr_path)
df = my_df(rcv_collection)
def avg_length(coll):
    
    total_length = 0
    for rcv_docs in coll.items():
        rcvdocwords=rcv_docs[1]
        rcvdoc_len=rcvdocwords.get_doc_len()
        total_length+=rcvdoc_len
    
    avgdoc_len=total_length/len(coll)
    return(avgdoc_len)


# TASK 3.2

def my_bm25(coll,q,df):
    
    query_parse = parse_query(q, read_stop_words())
    
    bm25_score={}
    
    for docs in coll.items():
        rcv_words = docs[1]
        rcv_dict = rcv_words.get_terms()
        N = len(coll)
        docID=docs[0]
        
        dl = rcv_words.get_doc_len()
        avdl = avg_length(coll)
        k1 = 1.2
        k2 = 100
        b = 0.75
        K = k1*((1-b) + (b*dl/avdl))
        
        
        bm25 = 0
        
        for term,freq in query_parse.items():
            if term in rcv_dict.keys():
                ni=df[term]
                fi=rcv_dict[term]
                qfi=query_parse[term]
                
                first_term = (N-ni+0.5)/(ni+0.5)
                second_term = ((k1 + 1)*fi)/(K + fi)
                third_term = ((k2 + 1)*qfi)/(k2 + qfi)
                product = first_term*second_term*third_term
                bm25 += math.log(product,2)
        
        bm25_score[docID] = bm25
    return(bm25_score)

# TASK 3.3

def bm25_main(coll):
    
    query = ["The British-Fashion Awards","Rocket attacks","Broadcast Fashion Awards","stock market" ]
    
    file = open("Ajay Krishnan Chelora Veetil_Q3.txt","w")
    
    file.write("Average Document length for this collection is:" + str(avg_length(coll))+"\n")
    
    for q in query:
        bm25_score = my_bm25(coll,q,df)
        len_dict = {}
        
        for rcv in coll.items():
            rcvdocwords = rcv[1]
            rcv_len = rcvdocwords.get_doc_len()
            len_dict[rcv[0]]=rcv_len
            
        new_dict = {k: v for k, v in sorted(bm25_score.items(), key=lambda item: item[1], reverse = True)}
        
        top = dict(list(new_dict.items())[0:6])
        
        
        file.write("The query is "+ q +"\n")
        file.write("The following are the BM25 score for each document \n")
        for k,v in top.items():
            file.write("Document ID: " + k + ", Doc Length: " + str(len_dict[k]) + "--" + "BM25 Score:" + str(v) + "\n")
        
        file.write("\n")
    file.close()
    
    
bm25_main(rcv_collection)