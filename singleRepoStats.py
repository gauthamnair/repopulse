import gitImporter
import gitModels
import pandas as pd
import featureMakers
import datetime
import productionModel
import time

importer = gitImporter.importer

def getRepoWeeklyData(repo_full_name):

	cached = gitModels.getOrClearCachedWeeklyData(repo_full_name)

	if len(cached) == 0:
		pyGithubRepo = importer.getRepo(repo_full_name)
		while True:
			weeklyContributions = importer.getWeeklyContributions(pyGithubRepo)
			if weeklyContributions != None:
				break
			else:
				time.sleep(1)

		gitModels.cacheWeeklyContributions(weeklyContributions, 
			repo_full_name = repo_full_name)
		gitModels.session.commit()
		cached = gitModels.getOrClearCachedWeeklyData(repo_full_name)

	return cached

def getTotalCommitsByWeek(weeklyData):
	weeklyTotal = weeklyData.pivot(index='week_start', 
		columns='author_login', values='commits_num').sum(axis=1)
	return [{'week_start': str(t.date()), 'commits_num': c} 
		for (t,c) 
		in zip(weeklyTotal.index, weeklyTotal.values)]

predictionModel = productionModel.loadModel()

def getPredictedProbAlive(weeklyData, tref = None):
	featureMakers.removeTimeFromWeekStartDate(weeklyData)

	if tref == None:
		tref = datetime.date.today()
	fmaker = featureMakers.FeatureMaker(tref=tref)

	features = pd.DataFrame([fmaker.makeFeatures(weeklyData)])

	(predictors, colNames) = productionModel.makePredictors(features)
	prob_alive = predictionModel.predict_proba(predictors)[0,1]
	return prob_alive