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