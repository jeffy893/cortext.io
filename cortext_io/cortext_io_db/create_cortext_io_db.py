import sqlite3

conn = sqlite3.connect("cortext_io.db")

c = conn.cursor()


c.execute("""CREATE TABLE DOC_SUMMARY (
	doc_id INTEGER PRIMARY KEY,
	identity TEXT,
	doc_title TEXT,
	author TEXT,
	geolocation TEXT,
	description TEXT,
	authored_date TEXT,
	entered_date TEXT,
	url TEXT
)""")

c.execute("""CREATE TABLE SENT_SUMMARY (
	sent_id INTEGER PRIMARY KEY,
	doc_id INTEGER NOT NULL,
	sent_order INTEGER,
	sent_total INTEGER,
	sent_content TEXT,
	FOREIGN KEY (doc_id) REFERENCES DOC_SUMMARY (doc_id)
)""")

c.execute("""CREATE TABLE SUBJ_SUMMARY (
	subj_summary_id INTEGER PRIMARY KEY,
	sent_id INTEGER NOT NULL,
	subj_summary_content TEXT,
	FOREIGN KEY (sent_id) REFERENCES SENT_SUMMARY (sent_id)
)""")

c.execute("""CREATE TABLE SUBJ_UNIT (
	subj_unit_id INTEGER PRIMARY KEY,
	subj_summary_id INTEGER NOT NULL,
	subj_unit_content TEXT,
	FOREIGN KEY (subj_summary_id) REFERENCES SUBJ_SUMMARY (subj_summary_id)
)""")

c.execute("""CREATE TABLE WORD_SUMMARY (
	word_id INTEGER PRIMARY KEY,
	sent_id INTEGER NOT NULL,
	syn_id INTEGER NOT NULL,
	word_order INTEGER,
	word_total INTEGER,
	word_content TEXT,
	FOREIGN KEY (sent_id) REFERENCES SENT_SUMMARY (sent_id)
)""")

c.execute("""CREATE TABLE PHEN_SUMMARY (
	phen_id INTEGER PRIMARY KEY,
	sent_id INTEGER,
	syn_id INTEGER,
	subj_summary_id INTEGER,
	concept_id INTEGER,
	entered_date TEXT,
	phen TEXT,
	FOREIGN KEY (sent_id) REFERENCES SENT_SUMMARY (sent_id)
)""")

c.execute("""CREATE TABLE WIKI_SEARCH (
	wiki_search_id INTEGER PRIMARY KEY,
	phen_id INTEGER,
	wiki_search_content TEXT,
    url TEXT,
    wiki_summary TEXT,
    FOREIGN KEY (phen_id) REFERENCES PHEN_SUMMARY (phen_id)
)""")


c.execute("""CREATE TABLE CORE_SUMMARY (
	core_id INTEGER PRIMARY KEY,
	core_cat TEXT,
    core_content TEXT,
    core_esp_content TEXT,
	core_order TEXT
)""")


c.execute("""CREATE TABLE SYN_SUMMARY (
	syn_id INTEGER PRIMARY KEY,
	core_id INTEGER,
	syn_content TEXT,
	FOREIGN KEY (core_id) REFERENCES CORE_SUMMARY (core_id)
)""")



conn.commit()