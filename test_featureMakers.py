import featureMakers
import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions WHERE repo_full_name='hadley/plyr'"
weekly = pd.io.sql.read_sql(query, con)
weekly.index = weekly['week_start']

hadleyWeekly = weekly[weekly['author_login'] == 'hadley']

tref = featureMakers.defaultTref()

fmaker = featureMakers.FeatureMaker(tref=featureMakers.defaultTref())

byAuthor = fmaker.makeByAuthorFeatures(weekly)
aggregated = fmaker.aggregateBasicAuthorFeaturesToDict(byAuthor)
print aggregated

directlyAggregated = fmaker.makeAuthorAggregatedFeatures(weekly)
print directlyAggregated

query = '''
SELECT * FROM WeeklyContributions 
WHERE repo_full_name IN ('hadley/plyr', 'hadley/ggplot2')
'''
twoRepos = pd.io.sql.read_sql(query, con)
twoRepos.index = twoRepos['week_start']

results = []
for repo_full_name, weeklyData in twoRepos.groupby('repo_full_name'):
	features = fmaker.makeAuthorAggregatedFeatures(weeklyData)
	features['repo_full_name'] = repo_full_name
	results.append(features)
print results