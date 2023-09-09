#!/bin/sh
cd /home/ec2-user/cortext_io/cortext_io_input
cp input.txt input2.txt
tr -cd '[:print:]' < input2.txt > input.txt
cd /home/ec2-user/cortext_io/AA_cortext_io_linux_0.1/AA_cortext_io_linux
./AA_cortext_io_linux_run.sh
cd /home/ec2-user/cortext_io/10K_RiskFactors_PROCESS
./3_CORTEXT_TRANSFORM.sh
./4_CORTEXT_LAYOUT_SIZE_40.sh
./5_CORTEXT_AssociateWeb.sh
./6_CORTEXT_SSIndex.sh
python3 zzz_pushElastic.py "$1" "$2"
python3 sendEmail.py "$1" "$2"
