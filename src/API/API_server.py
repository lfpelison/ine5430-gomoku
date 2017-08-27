import json
import bottle
from bottle import route, run, request, abort

import ast


#  nohup run python in background ex: nohup python API_server.py > test.txt 2>&1 </dev/null &
#  ps -ef see all process
#  kill PID -> to kill the background process
 
#from pymongo import MongoClient
#musica = {  "_id": 12345,
#             "nome": "Nothing lef to say",
#             "banda": "Imagine Dragons",
#             "categorias": ["indie", "rock"],
#             "lancamento": datetime.datetime.now()
#         }
#
#
#cliente = MongoClient('localhost', 27017)
#banco = cliente.test_database


import numpy as np

state = np.zeros((15,15))


from decideMove import *

def makePCMove(param, state):
    state[param[0]][param[1]]=param[2] # apply player move
    moves = decideMove(state, param[3], param[2])
    return moves
    
@route('/documents', method='PUT')
def put_document():
    return "<h1>Hello World!</h1>"

@route('/lala', method='PUT')
def put_document():
    return "<h1>Hello Kaka!</h1>"
    
   
@route('/makemove/:id', method='GET') # id= [row that player player, col that player played, numofplayer, number of PC ]
def get_document(id):
    param = ast.literal_eval(id)
    moves = makeClientMove(param)
	return moves

@route('/reset/:pass', method='GET')
def get_document(pass): 
    if pass=22:
        state = np.zeros((15,15))
	return state

 

#run(host='localhost', port=8080)    

run(host='0.0.0.0', port=4040)