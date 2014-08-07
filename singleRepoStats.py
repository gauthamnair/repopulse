from gitImporter import importer, weeklyContributionsToDicts
from featureMakers import makeFeatureMakers, howToAggregateAuthors
import pandas as pd
import featureMakers
import datetime
import productionModel

def getRepoCommitsStats(repoString):
	repo = importer.getRepo(repoString)

	weekly = importer.getWeeklyContributions(repo)

	tref = datetime.date.today()
	featureMakers = makeFeatureMakers(tref=tref)

	df = pd.DataFrame(list(weeklyContributionsToDicts(weekly)))
	df.index = df['week_start']
	grouped = df[['author_login','commits_num']].groupby(['author_login'], as_index=False)

	byAuthor = grouped.aggregate(featureMakers)['commits_num']

	commitsFeatures = {colName : aggregator(byAuthor[colName]) 
		for (colName, aggregator) in howToAggregateAuthors.items()}
	commitsFeatures = pd.DataFrame([commitsFeatures])
	return commitsFeatures

def getPredictedProbAlive(repoString):
	commitsFeatures = getRepoCommitsStats(repoString)
	model = productionModel.loadModel()
	predictors = productionModel.makePredictors(commitsFeatures)

	prob_alive = model.predict_proba(predictors)[0,1]
	return prob_alive