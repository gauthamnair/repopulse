import gitImporter
import gitModels
import pandas as pd
import featureMakers
import datetime
import productionModel
import modelTools
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

def getPredictedProbAlive(weeklyData):
	featureMakers.removeTimeFromWeekStartDate(weeklyData)
	tref = datetime.date.today()
	fmaker = featureMakers.FeatureMaker(tref=tref)

	features = pd.DataFrame([fmaker.makeFeatures(weeklyData)])
	model = productionModel.loadModel()

	(predictors, colNames) = modelTools.makePredictors(features)
	prob_alive = model.predict_proba(predictors)[0,1]
	return prob_alive