from flask import Flask, request
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect() 
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/ftball/<name>') 
def profile(name):
    rows = session.execute( """Select * From ftball.stats where home_team = '{}'""".format(name))
    for ftball in rows: 
        return('<h1>{} gains {} results(H for win, D for lose, A for draw), thanks for using .</h1>'.format(name,ftball.result))
    
    return('<h1>That team does not exist!</h1>')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8080)