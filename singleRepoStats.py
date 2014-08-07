from gitImporter import importer, weeklyContributionsToDicts
import pandas as pd
import featureMakers
import datetime
import productionModel

def getRepoCommitsStats(repoString):
	repo = importer.getRepo(repoString)

	weekly = importer.getWeeklyContributions(repo)
	df = pd.DataFrame(list(weeklyContributionsToDicts(weekly)))
	df.index = df['week_start']

	tref = datetime.date.today()
	fmaker = featureMakers.FeatureMaker(tref=tref)

	commitsFeatures = fmaker.makeAuthorAggregatedFeatures(df)
	return pd.DataFrame([commitsFeatures])

def getPredictedProbAlive(repoString):
	commitsFeatures = getRepoCommitsStats(repoString)
	model = productionModel.loadModel()
	predictors = productionModel.makePredictors(commitsFeatures)

	prob_alive = model.predict_proba(predictors)[0,1]
	return prob_alive