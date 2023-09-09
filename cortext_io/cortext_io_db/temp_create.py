import sqlite3

conn = sqlite3.connect("cortext_io.db")

c = conn.cursor()


c.execute("""CREATE TABLE WIKI_SEARCH (
	wiki_search_id INTEGER PRIMARY KEY,
	phen_id INTEGER,
	wiki_search_content TEXT,
    url TEXT,
    FOREIGN KEY (phen_id) REFERENCES PHEN_SUMMARY (phen_id)
)""")


c.execute("""Insert into WIKI_SEARCH (wiki_search_id,phen_id) values (0,0)""")


conn.commit()


