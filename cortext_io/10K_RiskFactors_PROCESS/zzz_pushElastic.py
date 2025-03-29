#!/usr/bin/env python3
"""
CORTEXT Elasticsearch Data Pusher

This script extracts processed CORTEXT analysis data from the SQLite database
and pushes it to an Elasticsearch instance for storage, indexing, and retrieval.
It organizes the data into a structured document with sections for sentences,
phenomena, and associated Wikipedia content.
"""

import sqlite3
from elasticsearch6 import Elasticsearch
from datetime import datetime
import sys
import re


# Default values for document tag and recipient email
# These will be used if no command-line arguments are provided
tag = "event_test"
email = "temp email"  # TODO: Replace with a default email or remove hardcoded value

# Try to get document tag and recipient email from command-line arguments
try:
    tag = sys.argv[1]
    email = sys.argv[2]
except Exception as e:
    print("Missing Identity or Email")

# Format the tag for display by replacing underscores with spaces
tag = re.sub("_", " ", tag)


# Connect to the CORTEXT SQLite database
conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")
c = conn.cursor()

# Check database encoding
c.execute('pragma encoding')

# Query to retrieve all relevant data for Elasticsearch indexing
# This joins multiple tables to get a complete view of the document analysis:
# - Document metadata (DOC_SUMMARY)
# - Sentence data with sentiment scores (SENT_SUMMARY)
# - Phenomena identified in the text (PHEN_SUMMARY)
# - Associated Wikipedia content (WIKI_SEARCH)
c.execute("""SELECT DISTINCT d.identity, s.*, p.*, w.*
FROM DOC_SUMMARY d 
JOIN SENT_SUMMARY s ON d.doc_id = s.doc_id 
JOIN PHEN_SUMMARY p ON s.sent_id = p.sent_id
JOIN WIKI_SEARCH w ON p.phen_id = w.phen_id
WHERE w.wiki_summary IS NOT NULL""")


# Commented out code for debugging/development purposes
# This would print the first row of data to verify the query results
# print(c.fetchall()[0])
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

# Helper function to get unique items from a list while preserving order
# This is used to deduplicate data before sending to Elasticsearch
def get_unique(numbers):
    s = []
    for d in numbers:
        if d not in s:
            s.append(d)
    return s
    
    # Alternative implementation that was commented out
    #list_of_unique_numbers = []
    #unique_numbers = set(numbers)
    #for number in unique_numbers:
    #    list_of_unique_numbers.append(number)
    #return list_of_unique_numbers

# Initialize data structures to hold the extracted information
identities = []      # Document identities
sentences = []       # Sentence data with sentiment vectors
phens = []           # Phenomena identified in the text
wikis = []           # Wikipedia content (full objects)
wiki_blues = []      # Wikipedia search terms only
#print(unique_sentences)
#print(unique_phens)
#print(unique_wikis)


# Process each row from the database query
for row in c.fetchall():
    # Extract sentence data with sentiment vectors
    sentences_data = { 
            "sentence": row[5],
            "warm_vector": [row[6], row[7], row[8]],
            "cold_vector": [row[9], row[10], row[11]]
            }

    # Extract Wikipedia data
    # Note: There are two identical blocks for wikis_data - this appears redundant
    # The second one (wikis_data2) is only used in the exception handler
    wikis_data = {
            "wiki_search_content": row[21],
            "wiki_url": row[22].encode("ascii", "ignore").decode("utf-8"),
            "wiki_summary": row[23].encode("ascii", "ignore").decode("utf-8")
            }
    
    wikis_data2 = {
            "wiki_search_content": row[21],
            "wiki_url": row[22].encode("ascii", "ignore").decode("utf-8"),
            "wiki_summary": row[23].encode("ascii", "ignore").decode("utf-8")
            }
    
    # Add the Wikipedia search term to the list
    wiki_blues.append(row[21])

    # Add data to the respective lists
    identities.append(row[0])
    sentences.append(sentences_data)
    phens.append(row[18])
    
    # Try to add the Wikipedia data, with fallback handling for encoding issues
    try:
        wikis.append(wikis_data)
    except Exception as e:
        print(e)
        if(e is not None):
            try:
                wikis.append(wikis_data2)
            except Exception as e:
                print(e)


# Deduplicate the data
unique_sentences = get_unique(sentences)
unique_phens = get_unique(phens)
unique_wikis = get_unique(wikis)
unique_wiki_blues = get_unique(wiki_blues)

# Get the unique document identity
unique_identity = get_unique(identities)

# Connect to Elasticsearch
# TODO: Consider using environment variables or a config file for these credentials
# TODO: Update with actual Elasticsearch endpoint and credentials
es = Elasticsearch(["endpoint"], http_auth=('username', 'password'))


# Create a structured document for Elasticsearch indexing
event_data = {
        "@timestamp": datetime.now().isoformat(),
        "tag": tag,
        "email": email,
        "identity": {
                "timestamp": str(datetime.now().isoformat()), 
                "tag": tag,  
                "email": email,
                "first_sentence": unique_identity[0]
                },
        "sentences": unique_sentences,
        "phen": unique_phens,
        "wiki_blues": unique_wiki_blues,
        "wiki": unique_wikis
        }

# Index the document in Elasticsearch
res = es.index(index="cortext_event", body=event_data, doc_type='_doc')
print(res['result'])

# Note: This script has several security and code quality issues that should be addressed:
# 1. Hardcoded credentials for Elasticsearch
# 2. Limited error handling for database and Elasticsearch operations
# 3. Redundant code for handling Wikipedia data
# 4. No validation of data before sending to Elasticsearch
# 5. No logging of indexing activity
