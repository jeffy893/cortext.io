import sqlite3
import wikipedia
import urllib
import os
import csv



#def wikiSummary(sizeReport=20):


ss_sign = [{"core_id":52,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":53,"COLD_SS":"NEG","WARM_SS":"NEG"},
    {"core_id":54,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":55,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":56,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":57,"COLD_SS":"NEG","WARM_SS":"NEG"},
    {"core_id":58,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":59,"COLD_SS":"NEG","WARM_SS":"NEG"},
    {"core_id":43,"COLD_SS":"POS","WARM_SS":"NEG"},
    {"core_id":44,"COLD_SS":"POS","WARM_SS":"NEG"},
    {"core_id":45,"COLD_SS":"NEG","WARM_SS":"POS"},
    {"core_id":46,"COLD_SS":"NEG","WARM_SS":"POS"},
    {"core_id":47,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":48,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":49,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":50,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":85,"COLD_SS":"POS","WARM_SS":"NEG"},
    {"core_id":86,"COLD_SS":"POS","WARM_SS":"NEG"},
    {"core_id":87,"COLD_SS":"NEG","WARM_SS":"POS"},
    {"core_id":88,"COLD_SS":"NEG","WARM_SS":"POS"},
    {"core_id":39,"COLD_SS":"POS","WARM_SS":"POS"},
    {"core_id":40,"COLD_SS":"NEG","WARM_SS":"NEG"},
    {"core_id":41,"COLD_SS":"POS","WARM_SS":"NEG"},
    {"core_id":42,"COLD_SS":"NEG","WARM_SS":"POS"}
    ]

#print(ss_sign)

conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")

c = conn.cursor()

try:
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN WARM_EX")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN WARM_EP")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN WARM_S")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN COLD_EX")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN COLD_EP")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN COLD_S")
except Exception as e:
    print(e)

try:
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN WARM_EX INTEGER")
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN WARM_EP INTEGER")
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN WARM_S INTEGER")
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN COLD_EX INTEGER")
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN COLD_EP INTEGER")
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN COLD_S INTEGER")
except Exception as e:
    print(e)
    

c.execute("""SELECT DISTINCT w.sent_id 
FROM WORD_SUMMARY w 
JOIN SYN_SUMMARY s ON w.syn_id = s.syn_id 
JOIN CORE_SUMMARY c ON s.core_id = c.core_id
WHERE w.syn_id != 0 AND c.CORE_ORDER IN ('EXPRESSION','EXISTENCE','SENTIMENT')""")

cold_ss = []
warm_ss = []


for row in c.fetchall():
    cold_ss.append({"sent_id":row[0],"EX":0,"S":0,"EP":0})
    warm_ss.append({"sent_id":row[0],"EX":0,"S":0,"EP":0})

c.execute("""SELECT w.word_id, w.sent_id, c.core_id, c.core_cat, c.core_order 
FROM WORD_SUMMARY w 
JOIN SYN_SUMMARY s ON w.syn_id = s.syn_id 
JOIN CORE_SUMMARY c ON s.core_id = c.core_id
WHERE w.syn_id != 0 AND c.CORE_ORDER IN ('EXPRESSION','EXISTENCE','SENTIMENT')""")

for row in c.fetchall():
    for sign in ss_sign:
        if row[2] == sign['core_id']:
            for i,ss in enumerate(cold_ss):
                if cold_ss[i]["sent_id"] == row[1]:
                    if sign["COLD_SS"] == "POS" and row[4] == "EXISTENCE":
                        cold_ss[i]["EX"] += 1
                    if sign["COLD_SS"] == "NEG" and row[4] == "EXISTENCE":
                        cold_ss[i]["EX"] -= 1
                    if sign["COLD_SS"] == "POS" and row[4] == "EXPRESSION":
                        cold_ss[i]["EP"] += 1
                    if sign["COLD_SS"] == "NEG" and row[4] == "EXPRESSION":
                        cold_ss[i]["EP"] -= 1
                    if sign["COLD_SS"] == "POS" and row[4] == "SENTIMENT":
                        cold_ss[i]["S"] += 1
                    if sign["COLD_SS"] == "NEG" and row[4] == "SENTIMENT":
                        cold_ss[i]["S"] -= 1
                        
            for i,ss in enumerate(warm_ss):
                if warm_ss[i]["sent_id"] == row[1]:
                    if sign["WARM_SS"] == "POS" and row[4] == "EXISTENCE":
                        warm_ss[i]["EX"] += 1
                    if sign["WARM_SS"] == "NEG" and row[4] == "EXISTENCE":
                        warm_ss[i]["EX"] -= 1
                    if sign["WARM_SS"] == "POS" and row[4] == "EXPRESSION":
                        warm_ss[i]["EP"] += 1
                    if sign["WARM_SS"] == "NEG" and row[4] == "EXPRESSION":
                        warm_ss[i]["EP"] -= 1
                    if sign["WARM_SS"] == "POS" and row[4] == "SENTIMENT":
                        warm_ss[i]["S"] += 1
                    if sign["WARM_SS"] == "NEG" and row[4] == "SENTIMENT":
                        warm_ss[i]["S"] -= 1


for cold in cold_ss:
    c.execute("""UPDATE SENT_SUMMARY SET COLD_EX = ?, COLD_EP = ?, COLD_S = ? WHERE sent_id = ?""",
        [cold["EX"],cold["EP"],cold["S"],cold["sent_id"]])
    conn.commit()
for warm in warm_ss:
    c.execute("""UPDATE SENT_SUMMARY SET WARM_EX = ?, WARM_EP = ?, WARM_S = ? WHERE sent_id = ?""",
        [warm["EX"],warm["EP"],warm["S"],warm["sent_id"]])
    conn.commit()








warm_vec = []
cold_vec = []
colors_vec = []

last_vec = [0,0,0]

for cold in cold_ss:
    cold_vec.append([int(last_vec[0]),int(last_vec[1]),int(last_vec[2]),int(cold["EX"]),int(cold["EP"]),int(cold["S"])],)
    last_vec[0] += int(cold["EX"])
    last_vec[1] += int(cold["EP"])
    last_vec[2] += int(cold["S"])
    colors_vec.append("#5d8aa8")
cold_vec.append([0,0,0,int(last_vec[0]),int(last_vec[1]),int(last_vec[2])])
colors_vec.append("#000000")


#print(last_vec)


import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

fig = plt.figure()

# draw vector
soa = np.array(cold_vec)


X, Y, Z, U, V, W = zip(*soa)


ax = fig.add_subplot(221, projection='3d')
ax.quiver(X, Y, Z, U, V, W, colors = colors_vec, arrow_length_ratio=0.07)


if last_vec[0] > 0:
    ax.set_xlim([0, last_vec[0]])
    ax.set_xlabel('Existence (0 --> ' + str(last_vec[0]) + ')')
elif last_vec[0] == 0:
    ax.set_xlim([-1, 1])
    ax.set_xlabel('Existence (-1 --> 1)')
else:
    ax.set_xlim([last_vec[0], 0])
    ax.set_xlabel('Existence ('+str(last_vec[0])+'--> 0)')
    
    
    
if last_vec[1] > 0:
    ax.set_ylim([0, last_vec[1]])
    ax.set_ylabel('Expression (0 --> ' + str(last_vec[1]) + ')')
elif last_vec[1] == 0:
    ax.set_ylim([-1, 1])
    ax.set_ylabel('Expression (-1 --> 1)')
else:
    ax.set_ylim([last_vec[1], 0])
    ax.set_ylabel('Expression ('+str(last_vec[1])+'--> 0)')
    
    
if last_vec[2] > 0:
    ax.set_zlim([0, last_vec[2]])
    ax.set_zlabel('Sentiment (0 --> ' + str(last_vec[2]) + ')')
elif last_vec[2] == 0:
    ax.set_zlim([-1, 1])
    ax.set_zlabel('Sentiment (-1 --> 1)')
else:
    ax.set_zlim([last_vec[2], 0])
    ax.set_zlabel('Sentiment ('+str(last_vec[2])+'--> 0)')
    
    
    
ax.set_title("Cold Straight Shooter")
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])



 
colors_vec = []
last_vec = [0,0,0]

for warm in warm_ss:
    warm_vec.append([int(last_vec[0]),int(last_vec[1]),int(last_vec[2]),int(warm["EX"]),int(warm["EP"]),int(warm["S"])])
    last_vec[0] += int(warm["EX"])
    last_vec[1] += int(warm["EP"])
    last_vec[2] += int(warm["S"])
    colors_vec.append("#800000")
warm_vec.append([0,0,0,int(last_vec[0]),int(last_vec[1]),int(last_vec[2])])
colors_vec.append("#000000")



# draw vector
soa2 = np.array(warm_vec)


X, Y, Z, U, V, W = zip(*soa2)


ax2 = fig.add_subplot(222, projection='3d')
ax2.quiver(X, Y, Z, U, V, W, colors=colors_vec, arrow_length_ratio=0.07)


if last_vec[0] > 0:
    ax2.set_xlim([0, last_vec[0]])
    ax2.set_xlabel('Existence (0 --> ' + str(last_vec[0]) + ')')
elif last_vec[0] == 0:
    ax2.set_xlim([-1, 1])
    ax2.set_xlabel('Existence (-1 --> 1)')
else:
    ax2.set_xlim([last_vec[0], 0])
    ax2.set_xlabel('Existence ('+str(last_vec[0])+'--> 0)')
    
    
    
if last_vec[1] > 0:
    ax2.set_ylim([0, last_vec[1]])
    ax2.set_ylabel('Expression (0 --> ' + str(last_vec[1]) + ')')
elif last_vec[1] == 0:
    ax2.set_ylim([-1, 1])
    ax2.set_yabel('Expression (-1 --> 1)')
else:
    ax2.set_ylim([last_vec[1], 0])
    ax2.set_ylabel('Expression ('+str(last_vec[1])+'--> 0)')
    
    
if last_vec[2] > 0:
    ax2.set_zlim([0, last_vec[2]])
    ax2.set_zlabel('Sentiment (0 --> ' + str(last_vec[2]) + ')')
elif last_vec[2] == 0:
    ax2.set_zlim([-1, 1])
    ax2.set_zlabel('Sentiment (-1 --> 1)')
else:
    ax2.set_zlim([last_vec[2], 0])
    ax2.set_zlabel('Sentiment ('+str(last_vec[2])+'--> 0)')
    
    
ax2.set_title("Warm Straight Shooter")
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.set_zticklabels([])


#plt.show()
os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
plt.savefig("000_cortext_ssindex.png")
"""
plt.savefig("output.jpg") #save as jpg
plt.savefig("output.png") #save as png
"""