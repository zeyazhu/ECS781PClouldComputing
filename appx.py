from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
import http.client
import requests
import json

cluster = Cluster(['cassandra'])
session = cluster.connect() 
app = Flask(__name__)

@app.route('/<mydata>', methods=['GET'])
def hello(mydata):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': 'bf1a425e36894e8ca223ff2f7bf05edf' }
    connection.request('GET', '/v2//', mydata, headers )#match of england
    response = json.loads(connection.getresponse().read().decode())
    if response.ok:
       ftbdata = response
    else:
        print(response.reason)
    #categories = (categ["home_team"]:categ["away_team"]["home_goals"]["away_goals"],["result"],["season"])


    return jsonify(response)
    # return('<h1> {} </h1>'.format(response))


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8080)