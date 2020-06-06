from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime
from flask_user import UserMixin
import uuid

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Machine(db.Model):
	__tablename__ = 'machines'
	id = db.Column(db.Integer, primary_key=True)
	adress = db.Column(db.Text(), nullable=False, server_default='')
	code = db.Column(db.Text(), nullable=False, server_default='')
	cells_count = db.Column(db.Integer(), nullable=False, server_default='0')

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	image_path = db.Column(db.Text(), nullable=False, server_default='')
	cell_number = db.Column(db.Integer(), nullable=False, server_default='0')
	machine_id = db.Column(db.Integer(), db.ForeignKey('machines.id'))
	machine = db.relationship('Machine', backref=db.backref('books', lazy=True))

class BookOperations(db.Model):
	__tablename__ = 'book_operations'
	id = db.Column(db.Integer, primary_key=True)
	operation_type = db.Column(db.Enum('in', 'out', name='operation_type'), nullable=False, server_default='in')
	date_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	book_id = db.Column(db.Integer(), db.ForeignKey('books.id'), nullable=True)
	machine_id = db.Column(db.Integer(), db.ForeignKey('machines.id'))
	cell_number = db.Column(db.Integer(), nullable=False)

@app.route('/', methods=['POST'])
def set_operation():
	data = request.json
	print(data)
	bo = BookOperations(operation_type=data['operation_type'], machine_id=data['machine_id'], cell_number=data['cell_number'], date_time=datetime.now())
	db.session.add(bo)
	db.session.commit()
	return jsonify({'OK': 200})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6060, debug=True)
