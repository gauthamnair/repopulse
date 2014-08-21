import featureMakers
import pandas as pd
import pymysql as mdb
import datetime
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions WHERE repo_full_name='hadley/ggplot2'"
weekly = pd.io.sql.read_sql(query, con)
featureMakers.removeTimeFromWeekStartDate(weekly)

tref = featureMakers.defaultTref()
# tref = featureMakers.defaultTref() - datetime.timedelta(30)

fmaker = featureMakers.FeatureMaker(tref=tref)

directlyAggregated = fmaker.makeFeatures(weekly)
for k in sorted(directlyAggregated.keys()):
	print k,":",directlyAggregated[k]



# gapsOnly = featureMakers.getCommitsGaps(dailyCommitsByAuthor)

# query = '''
# SELECT * FROM WeeklyContributions 
# WHERE repo_full_name IN ('hadley/plyr', 'hadley/ggplot2')
# '''
# twoRepos = pd.io.sql.read_sql(query, con)

# results = []
# for repo_full_name, weeklyData in twoRepos.groupby('repo_full_name'):
# 	features = fmaker.makeFeatures(weeklyData)
# 	features['repo_full_name'] = repo_full_name
# 	results.append(features)
# print pd.DataFrame(results)