from flask import render_template
from app import app
import pymysql as mdb

db = mdb.connect(user="root", host="localhost", db="world_innodb", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname': 'Miguelito'}
	return render_template("index.html",
		title='Home',
		user = user)