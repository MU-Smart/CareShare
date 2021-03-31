from flask import Flask, render_template, abort
from flask import request
import json
import requests

app = Flask(__name__, template_folder='templates')

taxi_ip = ["5001"]
url_taxi = "http://0.0.0.0:"


evaporation_factor = 0.5

@app.route('/')
def hello():
    return 'Hello World 1'

@app.route("/confirmRequest")
def confirm_request():
	print("confirmed")
	#cost_params = obtain_route()
	cost_params = {"route":"ABCD","cost":20}
	for i in taxi_ip:
		r = requests.get(url=url_taxi+i+"/broadcastPheromone",params=cost_params)
	return "confirmed and broadcasted"

@app.route('/broadcastPheromone')
def pheromone_update():
	received = request.args
	centroids_new = []
	route = received["route"]
	for i in route:
		pos = convert_to_xy(i)
		pt = get_nearest_centroids(pos)
		centroids_new.append(pt)
	for i in range(1,len(centroids_new)):
		pheromone[centroids[i-1]][centroids[i]] = (1-evaporation_factor)*pheromone[centroids[i-1]][centroids[i]] + evaporation_factor / received["cost"]

	return "Pheromone Updated"	

@app.route('/getRequest')
def get_request():
	data = {"taxi_id": 1,"cost":-1,"port":5000}
	return json.dumps(data)

if __name__ == '__main__':
	app.run('0.0.0.0',debug=True)
