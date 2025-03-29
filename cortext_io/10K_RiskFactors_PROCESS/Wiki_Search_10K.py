"""
Wikipedia Search Module for CORTEXT

This module performs Wikipedia searches for relevant phenotypes extracted from documents.
It connects to the CORTEXT database, extracts phenotypes, filters them using the
cortextClass scoring mechanism, and then performs Wikipedia searches for the filtered
phenotypes. The search results are stored back in the database for later use.

The module also extracts the company name from the first sentence of a document
and updates the document identity in the database.
"""

import sqlite3
import wikipedia
import urllib
import os
import csv
import cortextClass


def wikiSearch():
    """
    Perform Wikipedia searches for relevant phenotypes.
    
    This function:
    1. Connects to the CORTEXT database
    2. Extracts the company name from the first sentence of a document
    3. Updates the document identity in the database
    4. Retrieves phenotypes from the database
    5. Writes them to a temporary file
    6. Uses the cortextClass module to score and filter the phenotypes
    7. For each clean phenotype, performs a Wikipedia search
    8. Stores the search results in the database
    
    Returns:
        None
    """
    # Connect to the SQLite database
    conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")
    c = conn.cursor()

    # Get the content of the first sentence
    c.execute("SELECT sent_content FROM sent_summary WHERE sent_id = 1")
    
    identity = "temp"
    
    # Update Company Name from first Sentence into Doc Identity
    # This assumes the company name is at the beginning of the first sentence,
    # before the first occurrence of multiple spaces
    for row in c.fetchall():
        identity = row[0].split("      ", 1)[0]

    # Update the document identity in the database
    c.execute("UPDATE doc_summary SET identity = ? where doc_id = 1", [identity])
    conn.commit()
    
    # Get the maximum phenotype ID where syn_id is 0
    # This is used for progress reporting
    c.execute("SELECT MAX(phen_id) FROM phen_summary WHERE syn_id = 0")

    max_phen_id = 0

    for row in c.fetchall():
        max_phen_id = row[0]

    # Initialize list to store raw phenotypes
    rawPhen = []

    # Get all phenotypes where syn_id is 0
    c.execute("SELECT PHEN_ID, PHEN FROM phen_summary WHERE syn_id = 0")

    # Change to the database directory
    os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
    
    # Write phenotypes to a temporary file for processing by cortextClass
    with open('temp_cortext_io.txt', 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        
        # Process each phenotype, removing "quote" and "apos" strings
        for row in c.fetchall():
            try:
                cleaned_phen = row[1].replace("quote", "").replace("apos", "")
                spamwriter.writerow([cleaned_phen])
                rawPhen.append([int(row[0]), str(cleaned_phen)])
            except:
                print("Single Bad Phen")

    # Use cortextClass to score and filter phenotypes
    # This returns only the phenotypes that meet certain criteria
    cleanPhen = cortextClass.scoreMNB("temp_cortext_io.txt")

    # For each raw phenotype that matches a clean phenotype,
    # perform a Wikipedia search and store the results
    for row in rawPhen:
        for clean in cleanPhen:
            # Only apply to clean Phen
            if clean == row[1]:
                try:
                    # Perform Wikipedia search for the phenotype
                    wiki_search = wikipedia.search(row[1])
                    
                    # Store each search result in the database
                    for wiki_search_content in wiki_search:
                        # Insert the search result into the WIKI_SEARCH table
                        c.execute("""Insert into WIKI_SEARCH (wiki_search_id,phen_id,wiki_search_content,url) 
                                    values ((SELECT MAX(wiki_search_id)+1 FROM WIKI_SEARCH),?,?,?)""",
                                 [row[0], wiki_search_content, 
                                  ("https://en.wikipedia.org/wiki/" + wiki_search_content).replace(" ", "_")])
                        
                        # Print progress information
                        print(str(row[0]) + " out of " + str(max_phen_id))
                        
                        # Commit the changes to the database
                        conn.commit()
                except:
                    # Print error message if Wikipedia search fails
                    print("Error")
