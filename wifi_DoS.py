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

if len(check_wifi_result) == 0: #if no wifi adapter connected
	print("Please connect a wifi adapter")
    exit()
	
print("Following Wifi interfaces are available") 
for index, item in enumerate(check_wifi_result): #select a wifi adapter if wifi adapters are available
	print(f"{index} - {item}")

while True:
	wifi_interface_choice = input("please select the interface for the attack : ")
	try:
        if check_wifi_result[int(wifi_interface_choice)]:
		break
	except:
        print("Please select a number in chouces list")