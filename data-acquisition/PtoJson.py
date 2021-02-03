#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 14:36:39 2021

@author: danikaunger
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# """
# Created on Sat Jan 30 12:25:24 2021
# 
# @author: danikaunger
# """
# 
# # -*- coding: utf-8 -*-
# """
# Spyder Editor
# 
# This is a temporary script file.
# """
# import numpy 
# import JSON 
# 
# latitude = 112 
# altitude = 55
# longitude = 22.4
# latitude = 34.98
# speed = 10
# time = 1.1234
# 
# 
# print(latitude)
# =============================================================================
import json 
from datetime import datetime
now = datetime.now()

#all relevant GPS variables

# figure out units 

GPS_dictionary = {
    "latitude": 112, 
    "altitude" : 55,
    "longitude" : 22.4,
    "speed":  10,
    "time": 1.1234,
    "currenttime": ""              
   } 

#updating time 
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

GPS_dictionary["currenttime"]= current_time 



#updating the dictionary 
GPS_dictionary["speed"] = 12

print('New dictionary', GPS_dictionary) 


# Converts input dictionary into 
# string and stores it in json_string 
json_string = json.dumps(GPS_dictionary) 
print('Equivalent json string of input dictionary:', 
      json_string) 
print("        ") 

with open('gpsdictionaryJSON.txt', 'w') as outfile:
    json.dump(GPS_dictionary, outfile)


arraything = [GPS_dictionary, 5, "hey"] 

print(arraything) 







