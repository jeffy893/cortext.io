"""
Straight Shooter Index Generator

This script calculates and visualizes "Straight Shooter" indices for linguistic analysis.
It processes data from a SQLite database containing linguistic analysis results,
calculates cold and warm straight shooter metrics based on existence, expression,
and sentiment dimensions, and generates 3D vector visualizations of the results.

The script:
1. Connects to the CORTEXT database
2. Modifies the SENT_SUMMARY table schema to add necessary columns
3. Retrieves relevant linguistic data from multiple tables
4. Calculates cold and warm straight shooter metrics for each sentence
5. Updates the database with the calculated metrics
6. Generates 3D vector visualizations showing the progression of metrics
7. Saves the visualizations as a PNG file
"""

import sqlite3
import wikipedia
import urllib
import os
import csv


# Commented out function definition - possibly for future implementation
#def wikiSummary(sizeReport=20):


# Mapping of core_id values to cold and warm straight shooter signs (positive or negative)
# This dictionary defines how different linguistic core elements contribute to the
# cold and warm straight shooter indices
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

# Commented out print statement for debugging
#print(ss_sign)

# Connect to the SQLite database
conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")
c = conn.cursor()

# Attempt to drop existing columns from SENT_SUMMARY table
# This is done to ensure a clean slate before adding new columns
try:
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN WARM_EX")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN WARM_EP")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN WARM_S")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN COLD_EX")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN COLD_EP")
    c.execute("ALTER TABLE SENT_SUMMARY DROP COLUMN COLD_S")
except Exception as e:
    # Print any errors that occur during column dropping
    # These are expected if the columns don't exist yet
    print(e)

# Add new columns to SENT_SUMMARY table for storing straight shooter metrics
try:
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN WARM_EX INTEGER")  # Warm existence
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN WARM_EP INTEGER")  # Warm expression
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN WARM_S INTEGER")   # Warm sentiment
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN COLD_EX INTEGER")  # Cold existence
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN COLD_EP INTEGER")  # Cold expression
    c.execute("ALTER TABLE SENT_SUMMARY ADD COLUMN COLD_S INTEGER")   # Cold sentiment
except Exception as e:
    # Print any errors that occur during column addition
    print(e)
    
# Query to get all sentence IDs that have associated words with non-zero syn_id
# and core categories of EXPRESSION, EXISTENCE, or SENTIMENT
c.execute("""SELECT DISTINCT w.sent_id 
FROM WORD_SUMMARY w 
JOIN SYN_SUMMARY s ON w.syn_id = s.syn_id 
JOIN CORE_SUMMARY c ON s.core_id = c.core_id
WHERE w.syn_id != 0 AND c.CORE_ORDER IN ('EXPRESSION','EXISTENCE','SENTIMENT')""")

# Initialize lists to store cold and warm straight shooter metrics for each sentence
cold_ss = []
warm_ss = []

# Create data structures for each sentence with initial zero values for
# existence (EX), sentiment (S), and expression (EP) dimensions
for row in c.fetchall():
    cold_ss.append({"sent_id":row[0],"EX":0,"S":0,"EP":0})
    warm_ss.append({"sent_id":row[0],"EX":0,"S":0,"EP":0})

# Query to get all words with their associated sentence, core ID, category, and order
c.execute("""SELECT w.word_id, w.sent_id, c.core_id, c.core_cat, c.core_order 
FROM WORD_SUMMARY w 
JOIN SYN_SUMMARY s ON w.syn_id = s.syn_id 
JOIN CORE_SUMMARY c ON s.core_id = c.core_id
WHERE w.syn_id != 0 AND c.CORE_ORDER IN ('EXPRESSION','EXISTENCE','SENTIMENT')""")

# Process each word and update the cold and warm straight shooter metrics
for row in c.fetchall():
    for sign in ss_sign:
        if row[2] == sign['core_id']:
            # Update cold straight shooter metrics
            for i, ss in enumerate(cold_ss):
                if cold_ss[i]["sent_id"] == row[1]:
                    # Increment or decrement the appropriate dimension based on
                    # the core order and whether the sign is positive or negative
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
                        
            # Update warm straight shooter metrics
            for i, ss in enumerate(warm_ss):
                if warm_ss[i]["sent_id"] == row[1]:
                    # Increment or decrement the appropriate dimension based on
                    # the core order and whether the sign is positive or negative
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

# Update the database with the calculated cold straight shooter metrics
for cold in cold_ss:
    c.execute("""UPDATE SENT_SUMMARY SET COLD_EX = ?, COLD_EP = ?, COLD_S = ? WHERE sent_id = ?""",
        [cold["EX"], cold["EP"], cold["S"], cold["sent_id"]])
    conn.commit()

# Update the database with the calculated warm straight shooter metrics
for warm in warm_ss:
    c.execute("""UPDATE SENT_SUMMARY SET WARM_EX = ?, WARM_EP = ?, WARM_S = ? WHERE sent_id = ?""",
        [warm["EX"], warm["EP"], warm["S"], warm["sent_id"]])
    conn.commit()


# Initialize lists for storing vector data for visualization
warm_vec = []
cold_vec = []
colors_vec = []

# Track the cumulative values for cold straight shooter metrics
last_vec = [0, 0, 0]

# Build the vector data for cold straight shooter visualization
# Each vector represents the change in metrics for a single sentence
for cold in cold_ss:
    cold_vec.append([int(last_vec[0]), int(last_vec[1]), int(last_vec[2]), 
                     int(cold["EX"]), int(cold["EP"]), int(cold["S"])])
    last_vec[0] += int(cold["EX"])
    last_vec[1] += int(cold["EP"])
    last_vec[2] += int(cold["S"])
    colors_vec.append("#5d8aa8")  # Blue color for cold vectors

# Add a final vector from origin to the cumulative endpoint
cold_vec.append([0, 0, 0, int(last_vec[0]), int(last_vec[1]), int(last_vec[2])])
colors_vec.append("#000000")  # Black color for the final vector

# Commented out print statement for debugging
#print(last_vec)


# Import visualization libraries
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

# Create a new figure for the visualizations
fig = plt.figure()

# Convert the cold vector data to a numpy array
soa = np.array(cold_vec)

# Extract the components of the vectors
X, Y, Z, U, V, W = zip(*soa)

# Create the first subplot for cold straight shooter visualization
ax = fig.add_subplot(221, projection='3d')
ax.quiver(X, Y, Z, U, V, W, colors=colors_vec, arrow_length_ratio=0.07)

# Set the x-axis limits and label based on the final cumulative value
if last_vec[0] > 0:
    ax.set_xlim([0, last_vec[0]])
    ax.set_xlabel('Existence (0 --> ' + str(last_vec[0]) + ')')
elif last_vec[0] == 0:
    ax.set_xlim([-1, 1])
    ax.set_xlabel('Existence (-1 --> 1)')
else:
    ax.set_xlim([last_vec[0], 0])
    ax.set_xlabel('Existence ('+str(last_vec[0])+'--> 0)')
    
# Set the y-axis limits and label based on the final cumulative value
if last_vec[1] > 0:
    ax.set_ylim([0, last_vec[1]])
    ax.set_ylabel('Expression (0 --> ' + str(last_vec[1]) + ')')
elif last_vec[1] == 0:
    ax.set_ylim([-1, 1])
    ax.set_ylabel('Expression (-1 --> 1)')
else:
    ax.set_ylim([last_vec[1], 0])
    ax.set_ylabel('Expression ('+str(last_vec[1])+'--> 0)')
    
# Set the z-axis limits and label based on the final cumulative value
if last_vec[2] > 0:
    ax.set_zlim([0, last_vec[2]])
    ax.set_zlabel('Sentiment (0 --> ' + str(last_vec[2]) + ')')
elif last_vec[2] == 0:
    ax.set_zlim([-1, 1])
    ax.set_zlabel('Sentiment (-1 --> 1)')
else:
    ax.set_zlim([last_vec[2], 0])
    ax.set_zlabel('Sentiment ('+str(last_vec[2])+'--> 0)')
    
# Set the title and hide tick labels for cleaner visualization
ax.set_title("Cold Straight Shooter")
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])


# Reset colors and cumulative tracking for warm straight shooter visualization
colors_vec = []
last_vec = [0, 0, 0]

# Build the vector data for warm straight shooter visualization
# Each vector represents the change in metrics for a single sentence
for warm in warm_ss:
    warm_vec.append([int(last_vec[0]), int(last_vec[1]), int(last_vec[2]), 
                     int(warm["EX"]), int(warm["EP"]), int(warm["S"])])
    last_vec[0] += int(warm["EX"])
    last_vec[1] += int(warm["EP"])
    last_vec[2] += int(warm["S"])
    colors_vec.append("#800000")  # Maroon color for warm vectors

# Add a final vector from origin to the cumulative endpoint
warm_vec.append([0, 0, 0, int(last_vec[0]), int(last_vec[1]), int(last_vec[2])])
colors_vec.append("#000000")  # Black color for the final vector


# Convert the warm vector data to a numpy array
soa2 = np.array(warm_vec)

# Extract the components of the vectors
X, Y, Z, U, V, W = zip(*soa2)

# Create the second subplot for warm straight shooter visualization
ax2 = fig.add_subplot(222, projection='3d')
ax2.quiver(X, Y, Z, U, V, W, colors=colors_vec, arrow_length_ratio=0.07)

# Set the x-axis limits and label based on the final cumulative value
if last_vec[0] > 0:
    ax2.set_xlim([0, last_vec[0]])
    ax2.set_xlabel('Existence (0 --> ' + str(last_vec[0]) + ')')
elif last_vec[0] == 0:
    ax2.set_xlim([-1, 1])
    ax2.set_xlabel('Existence (-1 --> 1)')
else:
    ax2.set_xlim([last_vec[0], 0])
    ax2.set_xlabel('Existence ('+str(last_vec[0])+'--> 0)')
    
# Set the y-axis limits and label based on the final cumulative value
if last_vec[1] > 0:
    ax2.set_ylim([0, last_vec[1]])
    ax2.set_ylabel('Expression (0 --> ' + str(last_vec[1]) + ')')
elif last_vec[1] == 0:
    ax2.set_ylim([-1, 1])
    ax2.set_ylabel('Expression (-1 --> 1)')  # Fixed typo: set_yabel -> set_ylabel
else:
    ax2.set_ylim([last_vec[1], 0])
    ax2.set_ylabel('Expression ('+str(last_vec[1])+'--> 0)')
    
# Set the z-axis limits and label based on the final cumulative value
if last_vec[2] > 0:
    ax2.set_zlim([0, last_vec[2]])
    ax2.set_zlabel('Sentiment (0 --> ' + str(last_vec[2]) + ')')
elif last_vec[2] == 0:
    ax2.set_zlim([-1, 1])
    ax2.set_zlabel('Sentiment (-1 --> 1)')
else:
    ax2.set_zlim([last_vec[2], 0])
    ax2.set_zlabel('Sentiment ('+str(last_vec[2])+'--> 0)')
    
# Set the title and hide tick labels for cleaner visualization
ax2.set_title("Warm Straight Shooter")
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.set_zticklabels([])


# Commented out code to display the plot interactively
#plt.show()

# Change to the output directory and save the figure
os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
plt.savefig("000_cortext_ssindex.png")

# Commented out alternative save formats
"""
plt.savefig("output.jpg") #save as jpg
plt.savefig("output.png") #save as png
"""
