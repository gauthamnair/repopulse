import featureMakers
import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions"
weeklyData = pd.io.sql.read_sql(query, con)
featureMakers.removeTimeFromWeekStartDate(weeklyData)

tref = featureMakers.defaultTref()
fmaker = featureMakers.FeatureMaker(tref=tref)

commitStatsByRepoDicts = []
for repo_full_name, repoWeeklyData in weeklyData.groupby('repo_full_name'):
	features = fmaker.makeFeatures(repoWeeklyData)
	features['repo_full_name'] = repo_full_name
	commitStatsByRepoDicts.append(features)

commitStatsByRepo = pd.DataFrame(commitStatsByRepoDicts)

def removeReposCreatedAfterTref(df):
	return df[~ df['daysSinceLastCommit'].isnull()]

commitStatsByRepo = removeReposCreatedAfterTref(commitStatsByRepo)
commitStatsByRepo.to_csv('data/intermediate/byRepo.csv')