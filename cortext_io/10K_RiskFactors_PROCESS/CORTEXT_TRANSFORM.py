"""
CORTEXT Transform Module

This script is a part of the CORTEXT 10K Risk Factors Processing system. It serves as
a wrapper that initiates the Wikipedia search and enrichment process for extracted
phenotypes (key phrases or concepts) from financial documents.

The script imports the necessary modules and calls the wikiSearch() function from
the Wiki_Search_10K module, which performs the following operations:
1. Connects to the CORTEXT database
2. Updates document identity information
3. Retrieves phenotypes from the database
4. Filters phenotypes using the Multinomial Naive Bayes classifier
5. Performs Wikipedia searches for relevant phenotypes
6. Stores the search results in the database for later use

This script is typically executed by the 3_CORTEXT_TRANSFORM.sh shell script as part
of the overall CORTEXT processing pipeline.
"""

import Wiki_Search_10K  # Module containing the wikiSearch function
import sqlite3          # For database operations
import wikipedia        # For Wikipedia API access
import urllib           # For URL handling
import os               # For file system operations
import csv              # For CSV file operations

# Execute the Wikipedia search process for phenotypes extracted from 10-K risk factors
Wiki_Search_10K.wikiSearch()
