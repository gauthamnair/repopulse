from flask import Flask
app = Flask(__name__)
from flask import render_template, request, redirect, jsonify
import pymysql as mdb
import datetime
import singleRepoStats



@app.route('/')
@app.route('/index')
@app.route('/singlepage')
def singlepage():
	return render_template("singlepage.html", theTime=datetime.datetime.today())

@app.route('/example', methods=['GET'])
def example():
	return render_template("example.html")

@app.route('/getresult', methods=['GET'])
def mockpost():
	print "\nThe Repo String is"
	repoString = request.args.get("repoString", '')
	print repoString, "\n\n"

	weeklyData = singleRepoStats.getRepoWeeklyData(repoString)
	probAlive = singleRepoStats.getPredictedProbAlive(weeklyData)
	print probAlive
	return render_template("result.html", 
		repoString=repoString,
		probAlive=probAlive)


@app.route('/api/repo/<path:repoString>')
def getRepoStats(repoString):
	weeklyData = singleRepoStats.getRepoWeeklyData(repoString)
	probAlive = singleRepoStats.getPredictedProbAlive(weeklyData)
	weeks = singleRepoStats.getTotalCommitsByWeek(weeklyData)
	return jsonify({'repo_full_name' : repoString,
		'probAlive' : probAlive, 'weeks' : weeks})	


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

