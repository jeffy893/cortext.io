#!/usr/bin/env python3
"""
Batch Processing Controller for CORTEXT 10K Risk Factors

This script serves as the main controller for batch processing multiple input files.
It iterates through files in a designated batch directory, copies each file to the
input location, and triggers the processing pipeline for each file.
"""

import os
import shutil
import subprocess


# Commented out counter variable - likely used for debugging or limiting batch size
#flag = 0

# Iterate through each file in the batch directory
for filename in os.listdir("/home/ec2-user/cortext_io/10K_RiskFactors_PROCESS/10K_RiskFactors_CSV/0_BATCH"):
    
    try:
        # Print current file being processed for logging purposes
        print(filename)
        
        # Define source and destination paths
        # Source: The original file in the batch directory
        # Destination: The standard input location expected by the processing pipeline
        src = "/home/ec2-user/10K_RiskFactors_PROCESS/10K_RiskFactors_CSV/0_BATCH/" + filename
        dest = "/home/ec2-user/cortext_io/cortext_io_input/input.txt"

        # Copy the current batch file to the standard input location
        shutil.copyfile(src, dest)
        
        # Execute the main processing pipeline script
        # This script will trigger the entire sequence of processing steps
        subprocess.call([r'/home/ec2-user/cortext_io/10K_RiskFactors_PROCESS/1_CORTEXT_Run.sh'])
        
    except Exception as e:
        # Log any errors that occur during processing
        # This ensures the batch process continues even if one file fails
        print(e)
    
    # Commented out counter increment - likely used for debugging or limiting batch size
    #flag+=1
