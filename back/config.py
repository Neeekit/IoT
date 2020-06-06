class Config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:gfylffcz@localhost/iot"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = "barrelroll"
