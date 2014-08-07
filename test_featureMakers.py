import featureMakers
import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions WHERE repo_full_name='hadley/plyr'"
weekly = pd.io.sql.read_sql(query, con)
weekly.index = weekly['week_start']

hadleyWeekly = weekly[weekly['author_login'] == 'hadley']

tref = featureMakers.defaultTref()
byAuthor = featureMakers.makeByAuthorFeatures(weekly, tref=tref)
aggregated = featureMakers.aggregateBasicAuthorFeaturesToDict(byAuthor)

directlyAggregated = featureMakers.makeAuthorAggregatedFeatures(weekly, tref=tref)

z = weekly.groupby('repo_full_name').apply(
	lambda x: pd.DataFrame([featureMakers.makeAuthorAggregatedFeatures(x, tref=tref)]))

query = '''
SELECT * FROM WeeklyContributions 
WHERE repo_full_name IN ('hadley/plyr', 'hadley/ggplot2')
'''
twoRepos = pd.io.sql.read_sql(query, con)

results = []
for repo_full_name, weeklyData in twoRepos.groupby('repo_full_name'):
	features = featureMakers.makeAuthorAggregatedFeatures(weeklyData, tref=tref)
	features['repo_full_name'] = repo_full_name
	results.append(features)

# weeklyContributions = contrib

# tref = defaultTref()
# featureMakers = makeFeatureMakers(tref=tref)
# grouped = contrib.groupby(['repo_full_name', 'author_login'], as_index=False)
# commitsFeatures = grouped['commits_num'].aggregate(featureMakers)['commits_num']


# commitStatsByRepo = commitsFeatures.groupby(level=0).aggregate(howToAggregateAuthors)
# commitStatsByRepo = commitStatsByRepo[~ commitStatsByRepo['daysSinceLastCommit'].isnull()]

# query = "SELECT full_name, created_at, downloaded_on, language FROM Repos"
# repos = pd.io.sql.read_sql(query, con)

# timeSinceCreation = [tref - t.to_datetime().date() for t in repos['created_at']]
# repos['daysSinceCreation'] = [t.days for t in timeSinceCreation]
# repoStats = repos[['full_name', 'daysSinceCreation', 'language']]

# byRepo = pd.merge(repoStats, commitStatsByRepo,
# 	how='inner', left_on='full_name', right_index=True)

# byRepo.to_csv('data/intermediate/byRepo.csv')