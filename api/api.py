from bottle import route, run, template, post, request
from datetime import datetime
from pymongo import MongoClient

db = MongoClient()

@post('/<area_id>/alert')
def alert(area_id):
	cam_id = request.forms.get('cam_id')
	dt = datetime.now()
	prob = request.forms.get('prob')

	data = {'dt': dt,
	'area_id': area_id,
	'cam_id': cam_id,
	'prob': prob}
	db.gun_detection.dataset.insert_one(data)

	print(f"Câmera {cam_id} detectou arma com {round(float(prob),2)*100}% de probabilidade às {str(dt)}")

	return 1
run(host='0.0.0.0', port=8080, quiet=True)