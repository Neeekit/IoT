from flask import Flask, render_template, url_for, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from config import Config
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import Machine, Book, BookOperations

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
	machine_code = StringField('Machine code', validators=[DataRequired()])
	cell_number = StringField('Cell number', validators=[DataRequired()])
	photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
	submit = SubmitField('Upload')

@app.route('/')
@app.route('/index')
def index():
	machines = Machine.query.all()
	m_dict = {}
	for m in machines:
		m_dict[m.id] = {'adress': m.adress, 'books': []}
		
	last_operation = BookOperations.query.with_entities(BookOperations.machine_id, BookOperations.cell_number, db.func.max(BookOperations.date_time).label('last_operation_date')).group_by(BookOperations.machine_id, BookOperations.cell_number).all()
	for op in last_operation:
		o = BookOperations.query.filter_by(machine_id=op[0], cell_number=op[1], date_time=op[2]).first()
		print(o.id)
		if o.book_id is not None and o.operation_type=='in':
			book = Book.query.filter_by(id = o.book_id).first()
			print(book.image_path)
			m_dict[op[0]]['books'].append(book.image_path)

	machines = []
	for mid in m_dict.keys():
		machines.append(m_dict[mid])
	
	return render_template('index.html', machines=machines)

@app.route('/add', methods=['GET', 'POST'])
def upload_file():
	form = UploadForm()
	if form.validate_on_submit():
		machine_code = form.machine_code.data
		cell_number = int(form.cell_number.data)
		if Machine.query.filter_by(code=machine_code).count() != 0 and Machine.query.filter_by(code=machine_code).first().cells_count >= cell_number:
			m = Machine.query.filter_by(code=machine_code).first()
			op = BookOperations.query.filter_by(machine_id=m.id, cell_number=cell_number, operation_type='in').order_by(BookOperations.date_time.desc()).first()
			print(op.id)
			if (datetime.now() - op.date_time).seconds < 5:
				filename = photos.save(form.photo.data)
				file_url = photos.url(filename)
				q = Book(image_path=filename, cell_number=cell_number, machine_id=m.id)
				db.session.add(q)
				db.session.commit()
				q = Book.query.filter_by(image_path=filename).first()
				op.book_id = q.id
				db.session.commit()
				print(file_url)
				return redirect('/')
	else:
		file_url = None
	return render_template('add.html', form=form)
