import pandas as pd
import pymysql as mdb
import numpy as np
con = mdb.connect('localhost', 'root', '', 'gitdb');
import featureMakers
import logging

_extractedFileName = 'data/intermediate/gapsToday.csv'


query = '''
SELECT * FROM WeeklyContributions 
'''
weeklyData = pd.io.sql.read_sql(query, con)
featureMakers.removeTimeFromWeekStartDate(weeklyData)

tref = featureMakers.today()

def getCommitsGaps(df):
	dailyCommitsByAuthor = featureMakers.pivotToDailyCommitsByAuthor(df)
	return featureMakers.getCommitsGaps(dailyCommitsByAuthor).ix[:tref]


x = weeklyData.groupby('repo_full_name').apply(getCommitsGaps)
del x['gap_end']
x.reset_index()

x.to_csv(_extractedFileName)