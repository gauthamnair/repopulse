from flask import render_template, request, redirect
from app import app
import pymysql as mdb
import datetime
import singleRepoStats

db = mdb.connect(user="root", host="localhost", db="world_innodb", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", theTime=datetime.datetime.today())

@app.route('/getresult', methods=['POST'])
def mockpost():
	print "\nThe Repo String is"
	repoString = request.form["repoString"]
	print repoString, "\n\n"

	probAlive = singleRepoStats.getPredictedProbAlive(repoString)
	print probAlive
	return render_template("result.html", 
		repoString=repoString,
		probAlive=probAlive)