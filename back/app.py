from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
		
def post(self, machine_code, cell_number, position):
	return 'OK', 201
	  
api.add_resource(HelloWorld, "/<string:machine_code>/<int:cell_number>/<int:position>")
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6060, debug=True)
