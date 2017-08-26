import json
import bottle
from bottle import route, run, request, abort
#from pymongo import Connection
#from pymongo import MongoClient

#client = MongoClient('localhost:27017')
#db = client.mydatabase
 
@route('/documents', method='PUT')
def put_document():
    return "<h1>Hello World!</h1>"
    

     
@route('/documents/:id', method='GET')
def get_document(id):
	return {"_id": "doc1", "name": "Test Document 1"}

 
run(host='0.0.0.0', port=80)