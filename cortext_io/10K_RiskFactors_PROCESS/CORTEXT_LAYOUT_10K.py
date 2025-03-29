"""
CORTEXT Layout Generator for 10-K Risk Factors

This script generates a comprehensive CSV report from the CORTEXT database, which includes
sentences from financial documents, extracted phenotypes (key phrases or concepts), and
their associated Wikipedia summaries.

The script first retrieves Wikipedia summaries for the most frequent search terms, then
joins data from multiple database tables to create a structured report that links
sentences, phenotypes, and Wikipedia information.

Usage:
    python CORTEXT_LAYOUT_10K.py <size>
    
    where <size> is the number of Wikipedia summaries to retrieve (e.g., 20)
"""

import Wiki_Summary  # For retrieving Wikipedia summaries
import sqlite3       # For database operations
import wikipedia     # For Wikipedia API access
import urllib        # For URL handling
import os            # For file system operations
import csv           # For CSV file operations
import sys           # For command-line arguments


try:
    # Retrieve Wikipedia summaries for the most frequent search terms
    # The number of summaries is specified as a command-line argument
    Wiki_Summary.wikiSummary(int(sys.argv[1]))

    # Connect to the CORTEXT database
    conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")
    c = conn.cursor()

    # Execute a SQL query that joins three tables:
    # - WIKI_SEARCH: Contains Wikipedia search results and summaries
    # - PHEN_SUMMARY: Contains extracted phenotypes (key phrases or concepts)
    # - SENT_SUMMARY: Contains sentences from the financial documents
    #
    # The query retrieves:
    # - Sentence ID and content
    # - Phenotype ID and text
    # - Wikipedia summary, URL, and search term
    #
    # Results are ordered by phenotype ID
    c.execute("""
        SELECT DISTINCT 
            s.sent_id, s.sent_content, p.phen_id, p.phen, 
            w.WIKI_SUMMARY, w.url, w.wiki_search_content
        FROM WIKI_SEARCH AS w
        JOIN PHEN_SUMMARY AS p
            ON w.phen_id = p.phen_id
        JOIN SENT_SUMMARY as s
            ON p.sent_id = s.sent_id
        ORDER BY p.phen_id ASC
    """)
    
    # Change to the database directory
    os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
    
    # Write the results to a CSV file
    with open('000_cortext_io.csv', 'w', newline='\n', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        
        # Write the header row
        csv_writer.writerow([
            "SENT_ID", "SENT_CONTENT", "PHEN_ID", "PHEN", 
            "WIKI_SUMMARY", "WIKI_URL", "WIKI_SEARCH_CONTENT"
        ])

        # Write each data row
        for row in c.fetchall():
            try:
                csv_writer.writerow([
                    int(row[0]),  # SENT_ID
                    row[1],       # SENT_CONTENT
                    int(row[2]),  # PHEN_ID
                    row[3],       # PHEN
                    row[4],       # WIKI_SUMMARY
                    row[5],       # WIKI_URL
                    row[6]        # WIKI_SEARCH_CONTENT
                ])
            except:
                print("Single Bad Phen")  # Log error for problematic rows

except Exception as e:
    # Handle errors, particularly missing command-line arguments
    print("Make sure to enter a size of report! For instance: ~ py 2_CORTEXT_LAYOUT.py 20")
    print(e)
