from app import db
from datetime import datetime
 
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
	cell_number = db.Column(db.Integer(), nullable=False, server_default='0')

