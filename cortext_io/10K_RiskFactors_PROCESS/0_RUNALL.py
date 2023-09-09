import os
import shutil
import subprocess


#flag = 0

for filename in os.listdir("/home/ec2-user/cortext_io/10K_RiskFactors_PROCESS/10K_RiskFactors_CSV/0_BATCH"):
    
    try:
        print(filename)
        
        src = "/home/ec2-user/10K_RiskFactors_PROCESS/10K_RiskFactors_CSV/0_BATCH/" + filename
        dest = "/home/ec2-user/cortext_io/cortext_io_input/input.txt"

        shutil.copyfile(src,dest)
        
        subprocess.call([r'/home/ec2-user/cortext_io/10K_RiskFactors_PROCESS/1_CORTEXT_Run.sh'])
        
    except Exception as e:
        print(e)
    
    #flag+=1
