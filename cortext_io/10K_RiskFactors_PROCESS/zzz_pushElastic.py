import sqlite3
from elasticsearch6 import Elasticsearch
from datetime import datetime
import sys
import re


tag = "event_test"
email = "temp email" #Replace Me

try:
    tag = sys.argv[1]
    email = sys.argv[2]
except Exception as e:
    print("Missing Identity or Email")
tag = re.sub("_"," ",tag)



conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")

c = conn.cursor()

c.execute('pragma encoding')

c.execute("""SELECT DISTINCT d.identity, s.*, p.*, w.*
FROM DOC_SUMMARY d 
JOIN SENT_SUMMARY s ON d.doc_id = s.doc_id 
JOIN PHEN_SUMMARY p ON s.sent_id = p.sent_id
JOIN WIKI_SEARCH w ON p.phen_id = w.phen_id
WHERE w.wiki_summary IS NOT NULL""")



#print(c.fetchall()[0])
'''
for row in c.fetchall():
    event_data = {
        "@timestamp" : datetime.now().isoformat(),
	"identity" : row[0],
	"sent_id" : row[1],
	"sent_order" : row[3],
	"sent_content" : row[5],
	"warm_ex" : row[6],
	"warm_ep" : row[7],
	"warm_s" : row[8],
	"cold_ex" : row[9],
        "cold_ep" : row[10],
	"cold_s" : row[11],
	"phen_id" : row[12],
        "syn_id" : row[14],
	"subj_summary_id" : row[15],
	"concept_id" : row[16],
	"phen" : row[18],
	"wiki_search_id" : row[19],
	"wiki_search_content" : row[21],
	"wiki_url" : row[22],
	"wiki_summary" : row[23]
    }
    break
print(event_data)
'''
def get_unique(numbers):
    s = []
    for d in numbers:
        if d not in s:
            s.append(d)
    return s
    
    #list_of_unique_numbers = []



    #unique_numbers = set(numbers)

    #for number in unique_numbers:
    #    list_of_unique_numbers.append(number)

    #return list_of_unique_numbers

identities = []
sentences = []
phens = []
wikis = []
wiki_blues = []


for row in c.fetchall():
    sentences_data = { 
            "sentence" : row[5],
            "warm_vector" : [row[6],row[7],row[8]],
            "cold_vector" :  [row[9],row[10],row[11]]
            }

    wikis_data = {
            "wiki_search_content" : row[21],
            "wiki_url" : row[22].encode("ascii","ignore").decode("utf-8"),
            "wiki_summary" : row[23].encode("ascii","ignore").decode("utf-8")
            }
    
    wikis_data2 = {
            "wiki_search_content" : row[21],
            "wiki_url" : row[22].encode("ascii","ignore").decode("utf-8"),
            "wiki_summary" : row[23].encode("ascii","ignore").decode("utf-8")
            }
    wiki_blues.append(row[21])

    identities.append(row[0])
    sentences.append(sentences_data)
    phens.append(row[18])
    try:
        wikis.append(wikis_data)
    except Exception as e:
        print(e)
        if(e is not None):
            try:
                wikis.append(wikis_data2)
            except Exception as e:
                print(e)


unique_sentences = get_unique(sentences)
unique_phens = get_unique(phens)
unique_wikis = get_unique(wikis)
unique_wiki_blues = get_unique(wiki_blues)
#print(unique_sentences)
#print(unique_phens)
#print(unique_wikis)


unique_identity = get_unique(identities)

# IP Address of Elastic Search

#es = Elasticsearch(["endpoint"], http_auth=('username', 'password'))
es = Elasticsearch(["endpoint"], http_auth=('username', 'password'))


# Create a dictionary containing the event data

event_data = {
        "@timestamp" : datetime.now().isoformat(),
        "tag" : tag,
        "email" : email,
        "identity" : {
                "timestamp" : str(datetime.now().isoformat()), 
                "tag" : tag,  
                "email" : email,
                "first_sentence" : unique_identity[0]
                },
        "sentences" : unique_sentences,
        "phen" : unique_phens,
        "wiki_blues" : unique_wiki_blues,
        "wiki" : unique_wikis
        }

res = es.index(index="cortext_event", body=event_data, doc_type='_doc')
print(res['result'])


