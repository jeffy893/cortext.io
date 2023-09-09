import sqlite3
import wikipedia
import urllib
import os
import csv



def condition(prob,max_prob):
    return prob >= max_prob

def distrPhen(wiki_search_content,max_phen_id,sizeReport=20):
   
   incr = 1.0/float(max_phen_id)
   
   distr = {(wiki_search_content.count(wiki)/len(wiki_search_content),wiki) for wiki in wiki_search_content}
   
   max_prob = incr
   
   for prob, phen in distr:
    if prob >= max_prob:
        max_prob = prob
   
   count = 1
   
   while count < sizeReport + 1:
    if max_prob == incr:
        break
    count = sum(condition(x,max_prob) for x,y in distr)
    max_prob -= incr
   
   
   return distr,max_prob


def wikiSummary(sizeReport=20):

    """
    test = ["a","a","b","c","d"]

    distr = distrPhen(test)

    for i in distr:
        print(i)

    """



    conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")

    c = conn.cursor()

    try:
        #c.execute("ALTER TABLE WIKI_SEARCH DROP COLUMN WIKI_SUMMARY")
        c.execute("UPDATE WIKI_SEARCH SET WIKI_SUMMARY = null")
        conn.commit()
    except Exception as e:
        print(e)

    #try:
        #c.execute("ALTER TABLE WIKI_SEARCH ADD COLUMN WIKI_SUMMARY TEXT")
    #except Exception as e:
        #print(e)

    c.execute("SELECT MAX(phen_id) FROM WIKI_SEARCH")


    max_phen_id = 0

    for row in c.fetchall():
        max_phen_id = row[0]
        
        


    c.execute("SELECT wiki_search_id,phen_id,wiki_search_content FROM WIKI_SEARCH")



    allWiki = []
    wikiSearch = []



    for row in c.fetchall():
        allWiki.append([int(row[0]),int(row[1]),str(row[2])])
        wikiSearch.append(str(row[2]))

    distrWiki, threshold = distrPhen(wikiSearch,max_phen_id,sizeReport)

    flag = False
    
    returnCount = 1

    for distr in distrWiki:
        flag = False
        for row in allWiki:
            # Only apply to clean Phen
            if distr[0] > threshold:
                if distr[1] == row[2] and flag == False:
                    try:
                        wiki_search = ""
                        try:
                            wiki_search = wikipedia.summary(row[2], sentences = 2)
                        except:
                            flag = True
                        c.execute("""UPDATE WIKI_SEARCH SET wiki_summary = ? WHERE wiki_search_id = (SELECT MIN(wiki_search_id) from WIKI_SEARCH where wiki_search_content = ?)""",
                        [wiki_search,row[2]])
                        print(str(returnCount) + " out of " + str(sizeReport))
                        conn.commit()
                        flag = True
                        if returnCount == sizeReport:
                            break
                        returnCount+=1
                    except Exception as e:
                        print(e.__class__, '-', e)
        if returnCount == sizeReport:
                break
                            
