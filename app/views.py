from flask import render_template, request, redirect
from app import app
import pymysql as mdb
import datetime

db = mdb.connect(user="root", host="localhost", db="world_innodb", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", theTime=datetime.datetime.today())

@app.route('/mockpost', methods=['POST'])
def mockpost():
	print "\nThe Field is"
	print request.form["somefield"], "\n\n"
	return redirect("/index")