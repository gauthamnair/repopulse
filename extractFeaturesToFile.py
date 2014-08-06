from featureMakers import makeFeatureMakers, defaultTref
import numpy as np
import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions"
contrib = pd.io.sql.read_sql(query, con)
contrib.index = contrib['week_start']

tref = defaultTref()
featureMakers = makeFeatureMakers(tref=tref)
grouped = contrib.groupby(['repo_full_name', 'author_login'], as_index=False)
commitsFeatures = grouped['commits_num'].aggregate(featureMakers)['commits_num']


howToAggregate = {
'futureCommits_num': np.sum,
'pastCommits_num' : np.sum,
'daysSinceLastCommit' : np.min
}
commitStatsByRepo = commitsFeatures.groupby(level=0).aggregate(howToAggregate)
commitStatsByRepo = commitStatsByRepo[~ commitStatsByRepo['daysSinceLastCommit'].isnull()]

query = "SELECT full_name, created_at, downloaded_on, language FROM Repos"
repos = pd.io.sql.read_sql(query, con)
repos.head()

timeSinceCreation = [tref - t.to_datetime().date() for t in repos['created_at']]
repos['daysSinceCreation'] = [t.days for t in timeSinceCreation]
repoStats = repos[['full_name', 'daysSinceCreation']]

byRepo = pd.merge(repoStats, commitStatsByRepo,
	how='inner', left_on='full_name', right_index=True)


byRepo.to_csv('data/intermediate/byRepo.csv')