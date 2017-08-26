# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 14:21:17 2017

@author: Andrei
"""

import requests


response = requests.put("http://104.199.112.43/documents", 
                        data={"_id": "doc1", "name": "Test Document 1"} )


response = requests.get("http://104.199.112.43/documents/doc1")

print(response.status_code)

print(response.content)

