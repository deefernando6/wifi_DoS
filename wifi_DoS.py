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