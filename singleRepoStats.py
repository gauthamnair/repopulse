from gitImporter import importer, weeklyContributionsToDicts
import pandas as pd
import featureMakers
import datetime
import productionModel
import modelTools

def getRepoCommitsStats(repoString):
	repo = importer.getRepo(repoString)

	weekly = importer.getWeeklyContributions(repo)
	weekly = pd.DataFrame(list(weeklyContributionsToDicts(weekly)))
	featureMakers.removeTimeFromWeekStartDate(weekly)

	tref = datetime.date.today()
	fmaker = featureMakers.FeatureMaker(tref=tref)

	return pd.DataFrame([fmaker.makeFeatures(weekly)])

def getPredictedProbAlive(repoString):
	commitsFeatures = getRepoCommitsStats(repoString)
	model = productionModel.loadModel()

	(predictors, colNames) = modelTools.makePredictors(commitsFeatures)
	prob_alive = model.predict_proba(predictors)[0,1]
	return prob_alive