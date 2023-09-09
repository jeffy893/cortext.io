import Wiki_Summary
import sqlite3
import wikipedia
import urllib
import os
import csv
import sys


try:
    Wiki_Summary.wikiSummary(int(sys.argv[1]))

    conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")

    c = conn.cursor()

    c.execute("""SELECT DISTINCT s.sent_id, s.sent_content, p.phen_id, p.phen, w.WIKI_SUMMARY, 
    w.url, w.wiki_search_content
    FROM WIKI_SEARCH AS w
    join PHEN_SUMMARY AS p
    on w.phen_id = p.phen_id
    join SENT_SUMMARY as s
    on p.sent_id = s.sent_id
    order by p.phen_id asc""")
    
    os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
    with open('000_cortext_io.csv', 'w', newline='\n', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(["SENT_ID","SENT_CONTENT","PHEN_ID","PHEN","WIKI_SUMMARY","WIKI_URL","WIKI_SEARCH_CONTENT"])

        for row in c.fetchall():
            try:
                spamwriter.writerow([int(row[0]),row[1],int(row[2]),row[3],row[4],row[5],row[6]])
            except:
                print("Single Bad Phen")

    
except Exception as e:
    print("Make sure to enter a size of report! For instance: ~ py 2_CORTEXT_LAYOUT.py 20")
    print(e)
