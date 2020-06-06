import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:gfylffcz@localhost/iot"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'uploads')
	SECRET_KEY = "barrelroll"

