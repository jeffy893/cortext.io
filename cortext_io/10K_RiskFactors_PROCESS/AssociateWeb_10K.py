# AssociateWeb_10K.py
# Purpose: Generates an interactive D3.js visualization of relationships between phenomena
# extracted from 10-K risk factors, with supporting information from Wikipedia and other sources.

import sqlite3
import wikipedia
import urllib
import os
import csv
import cortextClass
import random
import re
import sys
import shutil
import re  # Duplicate import
import pandas as pd
import psycopg2
import sys  # Duplicate import
import boto3
import time
import json

fill = ["#5d8aa8","#00308f","#72a0c1","#a32638","#f0f8ff","#e32636","#c46210","#efdecd","#e52b50","#ffbf00","#ff7e00","#ff033e","#96c","#a4c639","#f2f3f4","#cd9575","#915c83","#841b2d","#faebd7","#008000","#8db600","#fbceb1","#0ff","#7fffd4","#4b5320","#3b444b","#e9d66b","#b2beb5","#87a96b","#f96","#a52a2a","#fdee00","#6e7f80","#568203","#007fff","#f0ffff","#89cff0","#a1caf1","#f4c2c2","#21abcd","#fae7b5","#ffe135","#7c0a02","#848482","#98777b","#bcd4e6","#9f8170","#f5f5dc","#9c2542","#ffe4c4","#3d2b1f","#fe6f5e","#bf4f51","#000","#3d0c02","#253529","#3b3c36","#ffebcd","#a57164","#318ce7","#ace5ee","#faf0be","#00f","#a2a2d0","#1f75fe","#69c","#0d98ba","#0093af","#0087bd","#339","#0247fe","#126180","#8a2be2","#de5d83","#79443b","#0095b6","#e3dac9","#c00","#006a4e","#873260","#0070ff","#b5a642","#cb4154","#1dacd6","#6f0","#bf94e4","#c32148","#ff007f","#08e8de","#d19fe8","#f4bbff","#ff55a3","#fb607f","#004225","#cd7f32","#964b00","#a52a2a","#ffc1cc","#e7feff","#f0dc82","#480607","#800020","#deb887","#c50","#e97451","#8a3324","#bd33a4","#702963","#536872","#5f9ea0","#91a3b0","#006b3c","#ed872d","#e30022","#fff600","#a67b5b","#4b3621","#1e4d2b","#a3c1ad","#c19a6b","#efbbcc","#78866b","#ffef00","#ff0800","#e4717a","#00bfff","#592720","#c41e3a","#0c9","#960018","#d70040","#eb4c42","#ff0038","#ffa6c9","#b31b1b","#99badd","#ed9121","#062a78","#92a1cf","#ace1af","#007ba7","#2f847c","#b2ffff","#4997d0","#de3163","#ec3b83","#007ba7","#2a52be","#6d9bc3","#007aa5","#e03c31","#a0785a","#fad6a5","#36454f","#e68fac","#dfff00","#7fff00","#de3163","#ffb7c5","#cd5c5c","#de6fa1","#a8516e","#aa381e","#7b3f00","#d2691e","#ffa700","#98817b","#e34234","#d2691e","#e4d00a","#fbcce7","#0047ab","#d2691e","#6f4e37","#9bddff","#f88379","#002e63","#8c92ac","#b87333","#da8a67","#ad6f69","#cb6d51","#966","#ff3800","#ff7f50","#f88379","#ff4040","#893f45","#fbec5d","#b31b1b","#6495ed","#fff8dc","#fff8e7","#ffbcd9","#fffdd0","#dc143c","#be0032","#0ff","#00b7eb","#ffff31","#f0e130","#00008b","#654321","#5d3954","#a40000","#08457e","#986960","#cd5b45","#008b8b","#536878","#b8860b","#a9a9a9","#013220","#00416a","#1a2421","#bdb76b","#483c32","#734f96","#8b008b","#036","#556b2f","#ff8c00","#9932cc","#779ecb","#03c03c","#966fd6","#c23b22","#e75480","#039","#872657","#8b0000","#e9967a","#560319","#8fbc8f","#3c1414","#483d8b","#2f4f4f","#177245","#918151","#ffa812","#483c32","#cc4e5c","#00ced1","#9400d3","#9b870c","#00703c","#555","#d70a53","#a9203e","#ef3038","#e9692c","#da3287","#fad6a5","#b94e48","#704241","#c154c1","#004b49","#95b","#c0c","#ffcba4","#ff1493","#843f5b","#f93","#00bfff","#66424d","#1560bd","#c19a6b","#edc9af","#696969","#1e90ff","#d71868","#85bb65","#967117","#00009c","#e1a95f","#555d50","#c2b280","#614051","#f0ead6","#1034a6","#7df9ff","#ff003f","#0ff","#0f0","#6f00ff","#f4bbff","#cf0","#bf00ff","#3f00ff","#8f00ff","#ff0","#50c878","#b48395","#96c8a2","#c19a6b","#801818","#b53389","#f400a1","#e5aa70","#4d5d53","#4f7942","#ff2800","#6c541e","#ce2029","#b22222","#e25822","#fc8eac","#f7e98e","#eedc82","#fffaf0","#ffbf00","#ff1493","#cf0","#ff004f","#014421","#228b22","#a67b5b","#0072bb","#86608e","#cf0","#c72c48","#f64a8a","#f0f","#c154c1","#f7f","#c74375","#e48400","#c66","#dcdcdc","#e49b0f","#f8f8ff","#b06500","#6082b6","#e6e8fa","#d4af37","#ffd700","#996515","#fcc200","#ffdf00","#daa520","#a8e4a0","#808080","#465945","#808080","#bebebe","#0f0","#1cac78","#008000","#00a877","#009f6b","#00a550","#66b032","#adff2f","#a99a86","#00ff7f","#663854","#446ccf","#5218fa","#e9d66b","#3fff00","#c90016","#da9100","#808000","#df73ff","#f400a1","#f0fff0","#007fbf","#49796b","#ff1dce","#ff69b4","#355e3b","#71a6d2","#fcf75e","#002395","#b2ec5d","#138808","#cd5c5c","#e3a857","#6f00ff","#00416a","#4b0082","#002fa7","#ff4f00","#ba160c","#c0362c","#5a4fcf","#f4f0ec","#009000","#fffff0","#00a86b","#f8de7e","#d73b3e","#a50b5e","#343434","#fada5e","#bdda57","#29ab87","#4cbb17","#7c1c05","#c3b091","#f0e68c","#e8000d","#087830","#d6cadd","#26619c","#fefe22","#a9ba9d","#cf1020","#ccf","#fff0f5","#b57edc","#c4c3d0","#9457eb","#ee82ee","#e6e6fa","#fbaed2","#967bb6","#fba0e3","#e6e6fa","#7cfc00","#fff700","#fffacd","#e3ff00","#1a1110","#fdd5b1","#add8e6","#b5651d","#e66771","#f08080","#93ccea","#f56991","#e0ffff","#f984ef","#fafad2","#d3d3d3","#90ee90","#f0e68c","#b19cd9","#ffb6c1","#e97451","#ffa07a","#f99","#20b2aa","#87cefa","#789","#b38b6d","#e68fac","#ffffe0","#c8a2c8","#bfff00","#32cd32","#0f0","#9dc209","#195905","#faf0e6","#c19a6b","#6ca0dc","#534b4f","#e62020","#f0f","#ca1f7b","#ff0090","#aaf0d1","#f8f4ff","#c04000","#fbec5d","#6050dc","#0bda51","#979aaa","#ff8243","#74c365","#880085","#c32148","#800000","#b03060","#e0b0ff","#915f6d","#ef98aa","#73c2fb","#e5b73b","#6da","#0000cd","#e2062c","#af4035","#f3e5ab","#035096","#1c352d","#dda0dd","#ba55d3","#0067a5","#9370db","#bb3385","#aa4069","#3cb371","#7b68ee","#c9dc87","#00fa9a","#674c47","#48d1cc","#79443b","#d9603b","#c71585","#f8b878","#f8de7e","#fdbcb4","#191970","#004953","#ffc40c","#3eb489","#f5fffa","#98ff98","#ffe4e1","#faebd7","#967117","#73a9c2","#ae0c00","#addfad","#30ba8f","#997a8d","#18453b","#c54b8c","#ffdb58","#21421e","#f6adc6","#2a8000","#fada5e","#ffdead","#000080","#ffa343","#fe4164","#39ff14","#d7837f","#a4dded","#059033","#0077be","#c72","#008000","#cfb53b","#fdf5e6","#796878","#673147","#c08081","#808000","#3c341f","#6b8e23","#9ab973","#353839","#b784a7","#ff7f00","#ff9f00","#ff4500","#fb9902","#ffa500","#da70d6","#654321","#900","#414a4c","#ff6e4a","#002147","#060","#273be2","#682860","#bcd4e6","#afeeee","#987654","#af4035","#9bc4e2","#ddadaf","#da8a67","#abcdef","#e6be8a","#eee8aa","#98fb98","#dcd0ff","#f984e5","#fadadd","#dda0dd","#db7093","#96ded1","#c9c0bb","#ecebbd","#bc987e","#db7093","#78184a","#ffefd5","#50c878","#aec6cf","#836953","#cfcfc4","#7d7","#f49ac2","#ffb347","#dea5a4","#b39eb5","#ff6961","#cb99c9","#fdfd96","#800080","#536878","#ffe5b4","#ffcba4","#fc9","#ffdab9","#fadfad","#d1e231","#eae0c8","#88d8c0","#b768a2","#e6e200","#ccf","#1c39bb","#00a693","#32127a","#d99058","#f77fbe","#701c1c","#c33","#fe28a2","#ec5800","#cd853f","#df00ff","#000f89","#123524","#fddde6","#01796f","#ffc0cb","#ffddf4","#f96","#e7accf","#f78fa7","#93c572","#e5e4e2","#8e4585","#dda0dd","#ff5a36","#b0e0e6","#ff8f00","#701c1c","#003153","#df00ff","#c89","#ff7518","#69359c","#800080","#9678b6","#9f00c5","#fe4eda","#50404d","#a020f0","#51484f","#5d8aa8","#ff355e","#fbab60","#e30b5d","#915f6d","#e25098","#b3446c","#826644","#f3c","#e3256b","#f00","#a52a2a","#860111","#f2003c","#c40233","#ff5349","#ed1c24","#fe2712","#c71585","#ab4e52","#522d80","#002387","#004040","#f1a7fe","#d70040","#0892d0","#a76bcf","#b666d2","#b03060","#414833","#0cc","#ff007f","#f9429e","#674846","#b76e79","#e32636","#f6c","#aa98a9","#905d5d","#ab4e52","#65000b","#d40000","#bc8f8f","#0038a8","#002366","#4169e1","#ca2c92","#7851a9","#fada5e","#d10056","#e0115f","#9b111e","#ff0028","#bb6528","#e18e96","#a81c07","#80461b","#b7410e","#da2c43","#00563f","#8b4513","#ff6700","#f4c430","#ff8c69","#ff91a4","#c2b280","#967117","#ecd540","#f4a460","#967117","#92000a","#507d2a","#0f52ba","#0067a5","#cba135","#ff2400","#fd0e35","#ffd800","#76ff7a","#006994","#2e8b57","#321414","#fff5ee","#ffba00","#704214","#8a795d","#009e60","#fc0fc0","#ff6fff","#882d17","#c0c0c0","#cb410b","#007474","#87ceeb","#cf71af","#6a5acd","#708090","#039","#933d41","#100c08","#fffafa","#0fc0fc","#a7fc00","#00ff7f","#23297a","#4682b4","#fada5e","#900","#4f666a","#e4d96f","#fc3","#fad6a5","#d2b48c","#f94d00","#f28500","#fc0","#e4717a","#483c32","#8b8589","#d0f0c0","#f88379","#f4c2c2","#008080","#367588","#00827f","#cf3476","#cd5700","#e2725b","#d8bfd8","#de6fa1","#fc89ac","#0abab5","#e08d3c","#dbd7d2","#eee600","#ff6347","#746cc0","#ffc87c","#fd0e35","#808080","#00755e","#0073cf","#417dc1","#deaa88","#b57281","#30d5c8","#00ffef","#a0d6b4","#7c4848","#8a496b","#66023c","#03a","#d9004c","#8878c3","#536895","#ffb300","#3cd070","#ff6fff","#120a8f","#4166f5","#635147","#ffddca","#5b92e5","#b78727","#ff6","#014421","#7b1113","#ae2029","#e1ad21","#004f98","#900","#fc0","#d3003f","#f3e5ab","#c5b358","#c80815","#43b3ae","#e34234","#d9603b","#a020f0","#8f00ff","#324ab2","#7f00ff","#8601af","#ee82ee","#40826d","#922724","#9f1d35","#da1d81","#ffa089","#9f00ff","#004242","#a4f4f9","#645452","#f5deb3","#fff","#f5f5f5","#a2add0","#ff43a4","#fc6c85","#722f37","#673147","#c9a0dc","#c19a6b","#738678","#0f4d92","#ff0","#9acd32","#efcc00","#ffd300","#ffae42","#ffef00","#fefe33","#0014a8","#2c1608"]

# Starting point identifier for the force-directed graph visualization
identity = "START_HERE"

# Change working directory to the database location
os.chdir('/home/ec2-user/cortext_io/cortext_io_db')
    
# Initialize output HTML file
spamwriter = open('000_cortext_io.html', 'w', newline='\n', encoding="utf-8")

# Write HTML header and styling for the D3.js visualization
spamwriter.write("""<!DOCTYPE html>\n
\n
<html lang="en">\n
\n
	<meta charset="UTF-8">\n
	<meta name="viewport" content="width=device-width, initial-scale=1.0">\n
	<style>\n

    .node {\n
        stroke: #fff;\n
        stroke-width: 2px;\n
    }\n
    \n
    .link {\n
        stroke: #777;\n
        stroke-width: 2px;\n
    }\n
\n
</style>\n
<body>\n
<a href="https://cortext.io">Cortext Website</a><br>\n
<a href="https://riskrunners.com">Public Company Risk Factors</a><br>\n
<a href="https://jefferson.cloud">Jefferson.Cloud</a><br>\n
\n
""")

# The following commented out code would have added navigation links to different sections of the page
#<a href="#risk_factors">Jump to Risk Factors</a><br>\n
#\n
#<a href="#industry">Jump to Industries</a><br>\n\n
#<a href="#exposure">Jump to Exposures</a><br>\n\n
#<a href="#event_code">Jump to Event Codes</a><br>\n\n
#<a href="#wiki">Jump to Wiki Summary</a><br><br>\n\n

# Include D3.js library and begin JavaScript for visualization
spamwriter.write("""
    <script src="https://d3js.org/d3.v3.min.js"></script>\n
    <script>\n

// set a width and height for our SVG\n
var width = 3000,\n

    height = 3000;\n
    
// setup links\n
var links =     """)

spamwriter.write("[\n")

# Connect to SQLite database
conn = sqlite3.connect("/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db")
c = conn.cursor()

# Query for sentence IDs that have associated phenomena with Wikipedia summaries
# This ensures we only visualize phenomena that have additional context
c.execute("SELECT distinct sent_id FROM phen_summary WHERE phen_id IN (SELECT distinct phen_id from wiki_search WHERE wiki_summary IS NOT NULL)")

# Store sentence IDs in a list for processing
sentList = []
for row in c.fetchall():
    sentList.append(int(row[0]))

# Initialize variables for graph node creation
id_flag = False
phen_last_sent = str(identity)  # Use the start identifier for the first node
phen_source = str(identity)
phen_target = str(identity)
fillColor = str(random.choice(fill))  # Note: 'fill' variable is not defined in this snippet

# Process each sentence ID to build graph links
for sent_order in sentList:
    # Query for phenomena in the current sentence
    c.execute("SELECT phen, sent_id FROM phen_summary WHERE sent_id = ? AND phen_id IN (SELECT distinct phen_id from wiki_search)", [sent_order])
    
    # Select a random fill color for visualization
    fillColor = str(random.choice(fill))  # Note: 'fill' variable is not defined
    
    # Process each phenomenon in the current sentence
    for row in c.fetchall():
        # Format the target node as "sent_id: phenomenon"
        phen_target = str(row[1]) + ": " + str(re.sub('\s+', ' ', row[0]))
        
        # For the first phenomenon in each sentence
        if id_flag == False:
            # Create a link from the previous sentence's last phenomenon to this one
            link_obj = '{source: \"' + str(phen_last_sent) + '\", target: \"' + phen_target + '\", fill: \"' + fillColor + '\"}'
            phen_last_sent = str(phen_target)  # Update last phenomenon for next iteration
            phen_source = str(phen_target)     # Set current phenomenon as source for next link
            spamwriter.write(str(link_obj) + ",\n")
            id_flag = True
        else:
            # Create links between phenomena within the same sentence
            link_obj = '{source: \"' + phen_source + '\", target: \"' + phen_target + '\", fill: \"' + fillColor + '\"}'
            phen_source = str(phen_target)  # Update source for next link
            spamwriter.write(str(link_obj) + ",\n")
    
    # Reset flag for next sentence
    id_flag = False
    sent_order += 1  # Note: This incrementation doesn't affect the loop as sent_order is not used as a loop control variable

# Create final link back to the start identifier to complete the graph
spamwriter.write('{source: \"' + str(phen_last_sent) + '\", target: \"' + identity + '\", fill: \"' + fillColor + '\"}];')

# Write D3.js visualization code for force-directed graph
spamwriter.write(""" 
    // create empty nodes array
    var nodes = {};
	var colorFill = [];
	
    // compute nodes from links data
    links.forEach(function(link) {
        link.source = nodes[link.source] ||
            (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] ||
            (nodes[link.target] = {name: link.target});
		colorFill.push({name: link.source.name, fill: link.fill });
		colorFill.push({name: link.target.name, fill: link.fill });
    });
	
	console.log(colorFill);


    // add a SVG to the body for our viz
    var svg=d3.select('body').append('svg')
        .attr("viewBox", "0 0 " + width + " " + height );

    // use the force
    var force = d3.layout.force()
		.charge(-5000)
		.gravity(0.3)
        .size([width, height])
        .nodes(d3.values(nodes))
        .links(links)
        .on("tick", tick)
        .linkDistance(200)
        .start();

    // add links
    var link = svg.selectAll('.link')
        .data(links)
        .enter().append('line')
        .attr('class', 'link'); 

    // add nodes
    var node = svg.selectAll('.node')
        .data(force.nodes())
        .enter().append('circle')
        .attr('class', 'node')
        .attr('r', width * 0.0035)
		.style("fill", function(d) {
									for (var i = 0; i < colorFill.length; i++) {
										//console.log(d.name);
										if(colorFill[i].name == d.name){
											console.log(colorFill[i].fill);
											return colorFill[i].fill;
										}
									} return "#555";
									
									});
	var label = svg.selectAll(null)
		.data(force.nodes())
		.enter()
		.append("text")
		.text(function (d) { return d.name; })
		.style("text-anchor", "middle")
		.style("fill", "#555")
		.style("font-family", "Arial")
		.style("font-size", 34);


    // what to do 
    function tick(e) {
        
        node.attr('cx', function(d) { return d.x = Math.max(6, Math.min(width - 6, d.x)); })
            .attr('cy', function(d) { return d.y = Math.max(6, Math.min(height - 6, d.y)); })
            .call(force.drag);
            
        link.attr('x1', function(d) { return d.source.x; })
            .attr('y1', function(d) { return d.source.y; })
            .attr('x2', function(d) { return d.target.x; })
            .attr('y2', function(d) { return d.target.y; });
		
		label.attr("x", function(d){ return d.x; })
             .attr("y", function (d) {return d.y - 10; });
        
    }
    
</script>""" )

# The following commented-out code sections provide alternative data access methods for
# PostgreSQL and AWS Athena queries but are currently disabled

# AWS Athena client setup (commented out)
#client = boto3.client('athena')

"""
# PostgreSQL connection configuration (commented out)
# Contains database credentials for connecting to a PostgreSQL database
PG_HOST="news.sensutec.com"
PG_PORT=5432
PG_USER="sensutec"
PG_PASSWORD="PeanutBrittle#21"  # Note: Hardcoded credentials should be avoided in production code
PG_DATABASE="postgres"

connection = psycopg2.connect(host=PG_HOST,
                        port=PG_PORT,
                        user=PG_USER,
                        password=PG_PASSWORD,
                        dbname=PG_DATABASE,
                        sslmode='require')

connection.autocommit = True  # Ensure data is added to the database immediately after write commands
cursor = connection.cursor()

# Commented-out test queries to verify PostgreSQL connection
#cursor.execute('SELECT %s as connected;', ('Connection to postgres successful!',))
#cursor.execute('SELECT "IDENTITY" FROM public.doc_summary where "DOC_ID" = 45;')
#print(cursor.fetchone())

for record in cursor.fetchall():
    print(record[0])
"""

"""
# Dataframe creation from query results (commented out)
df = pd.DataFrame(data=cursor.fetchall())
print(df)
"""

# GICS (Global Industry Classification Standard) query (commented out)
#cursor.execute("""SELECT "gics_lib_content", "gics_2nd" 
#FROM public.gics_library as lib join public.gics_2nd_order as ord
#on lib.gics_2nd_id = ord.gics_2nd_id;""")

"""
*********************************************
****************** GICS *********************
*********************************************
"""
"""
# AWS Athena query execution for GICS data (commented out)
# This section would retrieve industry classification data from AWS Athena
# and process it for use in the visualization

# Get the execution ID
execution_id = "07d04c8a-4ecf-4dd5-b62b-2860ce2d7e0d"

# Check the status of the execution
response = client.get_query_execution(QueryExecutionId=execution_id)
status = response['QueryExecution']['Status']['State']

# Wait until the execution is completed
while status == 'RUNNING':
    time.sleep(1)
    response = client.get_query_execution(QueryExecutionId=execution_id)
    status = response['QueryExecution']['Status']['State']

gics_results = []

# Get the results
if status == 'SUCCEEDED':
    response = client.get_query_results(QueryExecutionId=execution_id)
    time.sleep(3)
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=execution_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )
    flag = 0
    for results_page in results_iter:
        for row in results_page['ResultSet']['Rows']:
            if flag != 0:
                gics_results.append((row["Data"][0]["VarCharValue"],row["Data"][1]["VarCharValue"]))
            flag += 1
        
    #print(results["Rows"][0]["Data"][0]["VarCharValue"])
    
else:
    print("Query Failed")


gics = pd.DataFrame(data=gics_results)
gics[0] = gics[0].str.lower().str.replace(" ","")
gics.columns = ["gics_lib_content","gics_2nd"]
"""

"""
*********************************************
****************** GDELT ********************
*********************************************
"""
"""
# AWS Athena query execution for GDELT data (commented out)
# This section would retrieve Global Database of Events, Language, and Tone data
# for risk exposure analysis

# Get the execution ID
execution_id = "b3aea1a9-7f18-4918-bda6-6bed2a98cefc"

# Check the status of the execution
response = client.get_query_execution(QueryExecutionId=execution_id)
status = response['QueryExecution']['Status']['State']

# Wait until the execution is completed
while status == 'RUNNING':
    time.sleep(1)
    response = client.get_query_execution(QueryExecutionId=execution_id)
    status = response['QueryExecution']['Status']['State']

gdelt_results = []

# Get the results
if status == 'SUCCEEDED':
    response = client.get_query_results(QueryExecutionId=execution_id)
    time.sleep(3)
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=execution_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )
    flag = 0
    for results_page in results_iter:
        for row in results_page['ResultSet']['Rows']:
            if flag != 0:
                gdelt_results.append((row["Data"][0]["VarCharValue"],row["Data"][1]["VarCharValue"]))
            flag += 1
        
    #print(results["Rows"][0]["Data"][0]["VarCharValue"])
    
else:
    print("Query Failed")


gdelt = pd.DataFrame(data=gdelt_results)
gdelt[0] = gdelt[0].str.lower().str.replace(" ","")
gdelt.columns = ["gdelt_lib_content","gdelt_2nd"]
"""

# Alternative PostgreSQL query for GDELT data (commented out)
#cursor.execute("""SELECT "gdelt_lib_content", "gdelt_2nd"
#FROM public.gdelt_library as lib join public.gdelt_2nd_order as ord
#on lib.gdelt_2nd_id = ord.gdelt_2nd_id;""")

#gdelt = pd.DataFrame(data=cursor.fetchall())

"""
*********************************************
****************** IDEA  ********************
*********************************************
"""
"""
# AWS Athena query execution for IDEA data (commented out)
# This section would retrieve Integrated Data for Events Analysis data
# for event categorization

# Get the execution ID
execution_id = "00152b88-b5b7-47ff-a7f4-bc2450cdd3e9"

# Check the status of the execution
response = client.get_query_execution(QueryExecutionId=execution_id)
status = response['QueryExecution']['Status']['State']

# Wait until the execution is completed
while status == 'RUNNING':
    time.sleep(1)
    response = client.get_query_execution(QueryExecutionId=execution_id)
    status = response['QueryExecution']['Status']['State']

idea_results = []
"""
# Get the results
"""
if status == 'SUCCEEDED':
    response = client.get_query_results(QueryExecutionId=execution_id)
    time.sleep(3)
    results_paginator = client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=execution_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )
    flag = 0
    for results_page in results_iter:
        for row in results_page['ResultSet']['Rows']:
            if flag != 0:
                idea_results.append((row["Data"][0]["VarCharValue"],row["Data"][1]["VarCharValue"]))
            flag += 1
        
    #print(results["Rows"][0]["Data"][0]["VarCharValue"])
"""
#else:
#   print("Query Failed")

# Data processing for IDEA results (commented out)
#idea = pd.DataFrame(data=idea_results)
#idea[0] = idea[0].str.lower().str.replace(" ","")
#idea.columns = ["idea_lib_content","idea_2nd"]

# Alternative PostgreSQL query for IDEA data (commented out)
#cursor.execute("""SELECT "idea_lib_content", "idea_2nd"
#FROM public.idea_library as lib join public.idea_2nd_order as ord
#on lib.idea_2nd_id = ord.idea_2nd_id;""")

#idea = pd.DataFrame(data=cursor.fetchall())
#idea[0] = idea[0].str.lower().str.replace(" ","")
#idea.columns = ["idea_lib_content","idea_2nd"]

"""
# Debug output for dataframes (commented out)
print(gics)
print(gdelt)
print(idea)
"""

# Set working directory again (possibly redundant)
os.chdir('/home/ec2-user/cortext_io/cortext_io_db')

# Load data from CSV file containing text analysis results
df = pd.read_csv('000_cortext_io.csv', delimiter=',')

# Extract Wikipedia summary information for phenomena
wiki_summary = df[df.WIKI_SUMMARY.notnull()][["WIKI_SEARCH_CONTENT","WIKI_SUMMARY","WIKI_URL"]].copy()
# Create HTML links to Wikipedia articles
wiki_summary["WIKI"] ='<a href="' + wiki_summary["WIKI_URL"] + '">' + wiki_summary["WIKI_SEARCH_CONTENT"] + "</a>"
#print(wiki_summary[["WIKI","WIKI_SUMMARY"]].drop_duplicates().dropna().to_html(index=False).replace("&lt;","<").replace("&gt;",">"))

# Get unique phenomena with Wikipedia information
phen_wiki = df[["PHEN","WIKI_URL","WIKI_SEARCH_CONTENT"]].drop_duplicates().dropna().copy()

# The following commented out code would have joined the phenomena with classification data
# from GICS, GDELT, and IDEA databases for additional context

#phen_wiki["KEY"] = phen_wiki["PHEN"]
#phen_wiki["KEY"] = phen_wiki["KEY"].str.lower().str.replace(" ","")

#phen_wiki_gdelt = pd.merge(phen_wiki, gdelt, left_on='KEY', right_on='gdelt_lib_content', how='left')
#phen_wiki_gics = pd.merge(phen_wiki_gdelt, gics, left_on='KEY', right_on='gics_lib_content', how='left')
#phen_wiki_all = pd.merge(phen_wiki_gics, idea, left_on='KEY', right_on='idea_lib_content', how='left')

#phen_wiki_all.drop("gdelt_lib_content", axis=1,inplace=True)
#phen_wiki_all.drop("gics_lib_content", axis=1,inplace=True)
#phen_wiki_all.drop("idea_lib_content", axis=1,inplace=True)

"""
GICS --> Industry
GDELT --> Exposure
IDEA --> Event Code
"""

#phen_wiki_all.rename(columns = {'gics_2nd':'INDUSTRY', 'gdelt_2nd':'EXPOSURE', 'idea_2nd':'EVENT_CODE'}, inplace = True)

#print(phen_wiki_all[["EVENT_CODE"]].drop_duplicates().dropna().to_html(index=False))

# The following commented-out tables would have displayed classification information
#spamwriter.write(phen_wiki_all[["INDUSTRY"]].drop_duplicates().dropna().to_html(index=False).replace("<th>INDUSTRY","<th id='industry'>Industries"))
#spamwriter.write(phen_wiki_all[["EXPOSURE"]].drop_duplicates().dropna().to_html(index=False).replace("<th>EXPOSURE","<th id='exposure'>Exposures"))
#spamwriter.write(phen_wiki_all[["EVENT_CODE"]].drop_duplicates().dropna().to_html(index=False).replace("<th>EVENT_CODE","<th id='event_code'>Event Codes"))

# Write Wikipedia summary table to HTML
spamwriter.write(wiki_summary[["WIKI","WIKI_SUMMARY"]].drop_duplicates().dropna().to_html(index=False).replace("&lt;","<").replace("&gt;",">").replace("<th>WIKI<","<th id='wiki'>Wiki<").replace("<th>WIKI_SUMMARY","<th>Wiki Summary"))

# Extract unique risk factor sentences
risk_factors = df[["SENT_CONTENT"]].drop_duplicates().dropna().copy()
risk_factors.rename(columns = {'SENT_CONTENT':'RISK_FACTORS'}, inplace = True)

# Highlight phenomena within risk factor sentences by coloring them blue
for name, phen in phen_wiki["PHEN"].drop_duplicates().dropna().items():
    risk_factors["RISK_FACTORS"] = risk_factors["RISK_FACTORS"].str.replace(phen,'<font color="blue">' + phen + "</font>")

# Write highlighted risk factors to HTML
spamwriter.write(risk_factors[["RISK_FACTORS"]].to_html(index=False).replace("&lt;","<").replace("&gt;",">").replace("<th>RISK_FACTORS","<th id='risk_factors'>Sentences"))

# Close HTML document
spamwriter.write("""</body>


</html>""")

"""
# This commented-out code would have handled publishing the HTML and 
# archiving the database using the company identifier

# Publish HTML and Archive .DB

c.execute("SELECT identity from doc_summary where doc_id = 1")

for row in c.fetchall():
    identity = re.sub(r'[^a-zA-Z]', '', row[0])
    
src = "/home/ec2-user/cortext_io/cortext_io_db/cortext_io.db"
dest = "/home/ec2-user/cortext_io/10K_RiskFactors_PROCESS/10K_RiskFactors_DB/" + identity + ".db"

shutil.copyfile(src,dest)

src = "/home/ec2-user/cortext_io/cortext_io_db/000_cortext_io.html"
dest = "/home/ec2-user/cortext_io/10K_RiskFactors_PROCESS/10K_RiskFactors_HTML/" + identity + ".html"

shutil.copyfile(src,dest)

cursor.close()
connection.close()
"""
