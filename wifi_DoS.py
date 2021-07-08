import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime

acitve_wireless_networks = [] #create an empty list

def check_for_essid(essid, lst): #test if ESSID is already in the list
	check_status = True
	
	if len(lst) == 0:
		return check_status
		
	for item in lst : #this will run if there are access points in the list
		if essid in item["ESSID"]:
		 check_status = False     
	return check_status
	
if not "SUDO_UID" in os.environ.keys(): #check whether user run with sudo previledges.
	print('You need root previledges. Try with sudo')
	exit()

for file_name in os.listdir(): #to remove csv files before exxecuting the script
	if ".csv" in file_name:
		print("Yo have to remove .csv files in your directory")
        directory = os.getcwd()
		try: 
            os.mkdir(directory + "/backup/") #creating backup folder
		except:
            print('Backup folder is already in the directory')
		
		timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)
		
wlan_pattern = re.compile("^wlan[0-9]+")
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
