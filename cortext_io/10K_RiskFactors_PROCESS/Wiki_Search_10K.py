import sqlite3
import wikipedia
import urllib
import os
import csv
import cortextClass

def wikiSearch():
    conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")

    c = conn.cursor()

    c.execute("SELECT sent_content FROM sent_summary WHERE sent_id = 1")
    
    identity = "temp"
    
    # Update Company Name from first Sentence into Doc Identity
    
    for row in c.fetchall():
        identity = row[0].split("      ",1)[0]

    c.execute("UPDATE doc_summary SET identity = ? where doc_id = 1",[identity])
    conn.commit()
    
    
    
    c.execute("SELECT MAX(phen_id) FROM phen_summary WHERE syn_id = 0")


    max_phen_id = 0

    for row in c.fetchall():
        max_phen_id = row[0]


    rawPhen = []

    c.execute("SELECT PHEN_ID, PHEN FROM phen_summary WHERE syn_id = 0")

    os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
    with open('temp_cortext_io.txt', 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        

        for row in c.fetchall():
            try:
                spamwriter.writerow([row[1].replace("quote","").replace("apos","")])
                rawPhen.append([int(row[0]),str(row[1].replace("quote","").replace("apos",""))])
            except:
                print("Single Bad Phen")

    cleanPhen = cortextClass.scoreMNB("temp_cortext_io.txt")



    for row in rawPhen:
        for clean in cleanPhen:
            # Only apply to clean Phen
            if clean == row[1]:
                try:
                    wiki_search = wikipedia.search(row[1])
                    for wiki_search_content in wiki_search:
                        c.execute("""Insert into WIKI_SEARCH (wiki_search_id,phen_id,wiki_search_content,url) values ((SELECT MAX(wiki_search_id)+1 FROM WIKI_SEARCH),?,?,?)""",
                        [row[0],wiki_search_content,("https://en.wikipedia.org/wiki/" + wiki_search_content).replace(" ","_")])
                        print(str(row[0]) + " out of " + str(max_phen_id))
                        conn.commit()
                except:
                    print("Error")