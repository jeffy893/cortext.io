import os
import sys
import shutil
import sqlite3
import re


conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")

c = conn.cursor()

c.execute("SELECT identity from doc_summary where doc_id = 1")

identity = ""

for row in c.fetchall():
    identity = re.sub(r'[^a-z]', '', row[0])

src = "/home/ec2-user/cortext_io/cortext_io_db/000_cortext_io.html"
dest = "/home/ec2-user/cortext_io/output/" + identity + "/" + identity + ".html"

shutil.copyfile(src,dest)
