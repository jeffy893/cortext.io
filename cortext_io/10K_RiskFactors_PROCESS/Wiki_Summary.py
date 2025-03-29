"""
Wikipedia Summary Module for CORTEXT

This module retrieves Wikipedia summaries for the most frequent phenotypes found in
the CORTEXT database. It analyzes the distribution of Wikipedia search results,
identifies the most significant phenotypes based on their frequency, and fetches
concise summaries from Wikipedia for these phenotypes. The summaries are then
stored back in the database for later use in analysis and reporting.
"""

import sqlite3
import wikipedia
import urllib
import os
import csv


def condition(prob, max_prob):
    """
    Check if a probability meets or exceeds a threshold.
    
    This helper function is used in the distribution calculation to determine
    which phenotypes are significant enough to include in the results.
    
    Args:
        prob (float): The probability to check
        max_prob (float): The threshold probability
        
    Returns:
        bool: True if the probability meets or exceeds the threshold, False otherwise
    """
    return prob >= max_prob


def distrPhen(wiki_search_content, max_phen_id, sizeReport=20):
    """
    Calculate the distribution of phenotypes based on their frequency.
    
    This function analyzes the frequency of each unique Wikipedia search result
    and calculates a probability distribution. It then determines a threshold
    probability that will yield approximately the desired number of results.
    
    Args:
        wiki_search_content (list): List of Wikipedia search results
        max_phen_id (int): Maximum phenotype ID, used to calculate the probability increment
        sizeReport (int, optional): Target number of results to return. Defaults to 20.
        
    Returns:
        tuple: A tuple containing:
            - set: A set of tuples (probability, phenotype) for each unique search result
            - float: The threshold probability that yields approximately sizeReport results
    """
    # Calculate the increment for probability adjustments
    incr = 1.0/float(max_phen_id)
    
    # Create a set of tuples (probability, phenotype) for each unique search result
    # The probability is calculated as the count of occurrences divided by the total number
    distr = {(wiki_search_content.count(wiki)/len(wiki_search_content), wiki) for wiki in wiki_search_content}
    
    # Initialize the maximum probability threshold
    max_prob = incr
    
    # Find the highest probability in the distribution
    for prob, phen in distr:
        if prob >= max_prob:
            max_prob = prob
    
    count = 1
    
    # Adjust the threshold probability until we get approximately sizeReport results
    while count < sizeReport + 1:
        if max_prob == incr:
            break
        # Count how many phenotypes meet or exceed the current threshold
        count = sum(condition(x, max_prob) for x, y in distr)
        # If we have too few, lower the threshold
        max_prob -= incr
    
    return distr, max_prob


def wikiSummary(sizeReport=20):
    """
    Retrieve Wikipedia summaries for the most frequent phenotypes.
    
    This function:
    1. Connects to the CORTEXT database
    2. Clears existing summaries in the WIKI_SEARCH table
    3. Retrieves all Wikipedia search results
    4. Calculates a distribution of phenotypes using the distrPhen function
    5. Fetches Wikipedia summaries for the most frequent phenotypes (up to sizeReport)
    6. Updates the database with the summaries
    
    Args:
        sizeReport (int, optional): Maximum number of summaries to retrieve. Defaults to 20.
        
    Returns:
        None
    """
    # Commented out test code
    """
    test = ["a","a","b","c","d"]

    distr = distrPhen(test)

    for i in distr:
        print(i)
    """

    # Connect to the SQLite database
    conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")
    c = conn.cursor()

    try:
        # Clear existing summaries
        # Commented out: c.execute("ALTER TABLE WIKI_SEARCH DROP COLUMN WIKI_SUMMARY")
        c.execute("UPDATE WIKI_SEARCH SET WIKI_SUMMARY = null")
        conn.commit()
    except Exception as e:
        print(e)

    # Commented out code to add the WIKI_SUMMARY column
    # This is likely not needed if the column already exists
    #try:
        #c.execute("ALTER TABLE WIKI_SEARCH ADD COLUMN WIKI_SUMMARY TEXT")
    #except Exception as e:
        #print(e)

    # Get the maximum phenotype ID for calculating probability increments
    c.execute("SELECT MAX(phen_id) FROM WIKI_SEARCH")

    max_phen_id = 0

    for row in c.fetchall():
        max_phen_id = row[0]
    
    # Get all Wikipedia search results
    c.execute("SELECT wiki_search_id, phen_id, wiki_search_content FROM WIKI_SEARCH")

    # Initialize lists to store all wiki search entries and just the search content
    allWiki = []
    wikiSearch = []

    # Process each row from the database
    for row in c.fetchall():
        allWiki.append([int(row[0]), int(row[1]), str(row[2])])
        wikiSearch.append(str(row[2]))

    # Calculate the distribution and threshold for significant phenotypes
    distrWiki, threshold = distrPhen(wikiSearch, max_phen_id, sizeReport)

    flag = False
    returnCount = 1

    # Process each phenotype in the distribution
    for distr in distrWiki:
        flag = False
        # Check if this phenotype's probability exceeds the threshold
        if distr[0] > threshold:
            # Look for matching entries in the allWiki list
            for row in allWiki:
                # If we find a match and haven't processed this phenotype yet
                if distr[1] == row[2] and flag == False:
                    try:
                        wiki_search = ""
                        try:
                            # Fetch a 2-sentence summary from Wikipedia
                            wiki_search = wikipedia.summary(row[2], sentences=2)
                        except:
                            # If Wikipedia lookup fails, mark as processed and continue
                            flag = True
                        
                        # Update the database with the summary
                        # Note: This only updates the first occurrence of each search term
                        c.execute("""UPDATE WIKI_SEARCH SET wiki_summary = ? 
                                    WHERE wiki_search_id = (SELECT MIN(wiki_search_id) 
                                    from WIKI_SEARCH where wiki_search_content = ?)""",
                                 [wiki_search, row[2]])
                        
                        # Print progress information
                        print(str(returnCount) + " out of " + str(sizeReport))
                        
                        # Commit the changes to the database
                        conn.commit()
                        
                        # Mark this phenotype as processed
                        flag = True
                        
                        # If we've reached the target number of summaries, break
                        if returnCount == sizeReport:
                            break
                        
                        # Increment the counter
                        returnCount += 1
                    except Exception as e:
                        # Print any errors that occur during processing
                        print(e.__class__, '-', e)
            
            # If we've reached the target number of summaries, break
            if returnCount == sizeReport:
                break
