from featureMakers import makeFeatureMakers, defaultTref
import numpy as np
import pandas as pd
import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions"
contrib = pd.io.sql.read_sql(query, con)
contrib.index = contrib['week_start']

featureMakers = makeFeatureMakers(tref=defaultTref())
grouped = contrib.groupby(['repo_full_name', 'author_login'], as_index=False)
commitsFeatures = grouped['commits_num'].aggregate(featureMakers)['commits_num']


howToAggregate = {
'futureCommits_num': np.sum,
'pastCommits_num' : np.sum,
'daysSinceLastCommit' : np.min
}
byRepo = commitsFeatures.groupby(level=0).aggregate(howToAggregate)
byRepo = byRepo[~ byRepo['daysSinceLastCommit'].isnull()]

byRepo.to_csv('data/intermediate/byRepo.csv')