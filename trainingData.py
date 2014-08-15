import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');
import logging
import featureMakers

_extractedFileName = 'data/intermediate/byRepo.csv'

def computeAndSaveToFile(
	tref = featureMakers.defaultTref(),
	query = "SELECT * FROM WeeklyContributions", 
	fileName = _extractedFileName):

	weeklyData = pd.io.sql.read_sql(query, con)
	featureMakers.removeTimeFromWeekStartDate(weeklyData)

	fmaker = featureMakers.FeatureMaker(tref=tref)

	commitStatsByRepoDicts = []
	for repo_full_name, repoWeeklyData in weeklyData.groupby('repo_full_name'):
		if repoWeeklyData['week_start'].min().date() > tref:
			continue
		else:
			try:
				features = fmaker.makeFeatures(repoWeeklyData)
				features['repo_full_name'] = repo_full_name
			except:
				logging.exception(repo_full_name)
			commitStatsByRepoDicts.append(features)

	commitStatsByRepo = pd.DataFrame(commitStatsByRepoDicts)
	commitStatsByRepo['tref'] = pd.to_datetime(tref)

	def removeReposCreatedAfterTref(df):
		return df[~ df['daysSinceLastCommit'].isnull()]

	commitStatsByRepo = removeReposCreatedAfterTref(commitStatsByRepo)
	commitStatsByRepo.to_csv(fileName)


def load(fileName = _extractedFileName):
	byRepo = pd.read_csv(fileName)
	del byRepo['Unnamed: 0']
	return byRepo


if __name__ == '__main__':
	computeAndSaveToFile()