# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 14:21:17 2017

@author: Andrei
"""

import requests

import numpy as np

state= np.zeros((15,15))

#site= "http://localhost:8080"

site = "http://api.andreidonati.xyz"

site= "http://35.185.236.57"


response = requests.put(site + "/processmove", data= {"row": 6, "col": 7, "player": 1, "pc":-1} ) #row < 0 means para pc start the game


response = requests.get(site +"/move" )

a= str(response.content)

b = ast.literal_eval(a[2:-1])

print(b.values())

