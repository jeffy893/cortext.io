#!/bin/sh
# CORTEXT Processing Pipeline - Main Execution Script
# This script coordinates the execution of the entire CORTEXT processing pipeline
# It prepares the input file, runs the core CORTEXT engine, and executes all post-processing steps

# Navigate to input directory and prepare the input file
cd /home/ec2-user/cortext_io/cortext_io_input
cp input.txt input2.txt
# Remove non-printable characters to ensure clean input for processing
tr -cd '[:print:]' < input2.txt > input.txt

# Navigate to CORTEXT engine directory and execute the core processing
cd /home/ec2-user/cortext_io/AA_cortext_io_linux_0.1/AA_cortext_io_linux
./AA_cortext_io_linux_run.sh

# Navigate to processing directory and execute the post-processing pipeline
cd /home/ec2-user/cortext_io/10K_RiskFactors_PROCESS
./3_CORTEXT_TRANSFORM.sh
./4_CORTEXT_LAYOUT_SIZE_40.sh
./5_CORTEXT_AssociateWeb.sh
./6_CORTEXT_SSIndex.sh

# Push processed data to Elasticsearch
# $1 and $2 are tag and email params
python3 zzz_pushElastic.py "$1" "$2"

# Send email notification upon completion
# $1 and $2 are identity and email params
python3 sendEmail.py "$1" "$2"
