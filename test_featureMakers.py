import featureMakers
import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions WHERE repo_full_name='hadley/plyr'"
weekly = pd.io.sql.read_sql(query, con)
# weekly.index = weekly['week_start']

hadleyWeekly = weekly[weekly['author_login'] == 'hadley']

dailyCommitsByAuthor = featureMakers.pivotToDailyCommitsByAuthor(weekly)

tref = featureMakers.defaultTref()

fmaker = featureMakers.FeatureMaker(tref=featureMakers.defaultTref())

byAuthor = fmaker.makeByAuthorFeatures(dailyCommitsByAuthor)
print byAuthor
aggregated = fmaker.aggregateBasicAuthorFeaturesToDict(byAuthor)
print aggregated

directlyAggregated = fmaker.makeFeatures(weekly)
print directlyAggregated

query = '''
SELECT * FROM WeeklyContributions 
WHERE repo_full_name IN ('hadley/plyr', 'hadley/ggplot2')
'''
twoRepos = pd.io.sql.read_sql(query, con)

results = []
for repo_full_name, weeklyData in twoRepos.groupby('repo_full_name'):
	features = fmaker.makeFeatures(weeklyData)
	features['repo_full_name'] = repo_full_name
	results.append(features)
print pd.DataFrame(results)