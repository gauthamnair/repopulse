import pandas as pd
import datetime
import numpy as np

daysInWeek = 7
def dailyRangeSinceBeginning(timeseries):
    return pd.date_range(start=timeseries.index[0], end=datetime.date.today())

def resampleToDays(weeklyCommits, daterange=None):
    if daterange == None:
        daterange = dailyRangeSinceBeginning(weeklyCommits)
    x = weeklyCommits.reindex(
        index=daterange,
        method='ffill',
        limit=daysInWeek)
    x = x/daysInWeek
    x = x.fillna(0)
    return x

defaultFutureWindowInDays = 6*30

def defaultTref():
	return datetime.date(2014, 8, 6) - datetime.timedelta(defaultFutureWindowInDays)

def totalInPeriodStarting(timeseries, tref, 
		futureWindowInDays = defaultFutureWindowInDays):

	tfuture = tref + datetime.timedelta(futureWindowInDays)
	return timeseries.ix[tref : tfuture].sum()

def totalInDefaultPeriod(timeseries):
	return totalInPeriodStarting(timeseries, defaultTref())

def mostRecentNonZero(timeseries, tref):
    subsetted = timeseries[timeseries > 0].ix[:tref]
    if len(subsetted)==0:
    	return None
    else:
    	return subsetted.index[-1]

def daysSinceLastNonZero(timeseries, tref):
    t = mostRecentNonZero(timeseries, tref)
    if t == None:
    	return np.nan
    else:
	    deltaT = tref - t.to_datetime().date()
	    return deltaT.days

def oldestNonZero(timeseries, tref):
    subsetted = timeseries[timeseries > 0].ix[:tref]
    if len(subsetted)==0:
    	return None
    else:
    	return subsetted.index[0]

def daysSinceOldestNonZero(timeseries, tref):
    t = oldestNonZero(timeseries, tref)
    if t == None:
    	return np.nan
    else:
	    deltaT = tref - t.to_datetime().date()
	    return deltaT.days

def totalToDate(timeseries, tref):
	return timeseries.ix[:tref].sum()


def basicCommitsFeaturesMaker(tref, futureWindowInDays=defaultFutureWindowInDays):
	def futureCommits_num(x):
		return totalInPeriodStarting(x, tref=tref,
			futureWindowInDays=defaultFutureWindowInDays)
	def daysSinceLastCommit(x):
		return daysSinceLastNonZero(x, tref=tref)
	def daysSinceFirstCommit(x):
		return daysSinceOldestNonZero(x, tref=tref)
	def pastCommits_num(x):
		return totalToDate(x, tref=tref)
	return [futureCommits_num, daysSinceLastCommit, 
		daysSinceFirstCommit, pastCommits_num]


basicFeatureAggregators = {
    'futureCommits_num': np.sum,
    'pastCommits_num' : np.sum,
    'daysSinceLastCommit' : np.min,
    'daysSinceFirstCommit' : np.max
}

def makeByAuthorFeatures(df, tref, futureWindowInDays=defaultFutureWindowInDays):
    authorCommitsFeatureMaker = basicCommitsFeaturesMaker(tref, futureWindowInDays)
    grouped = df[['author_login','commits_num']].groupby(['author_login'], as_index=False)
    return grouped.aggregate(authorCommitsFeatureMaker)['commits_num']    

def aggregateBasicAuthorFeaturesToDict(df):
    aggregated = dict()
    for colName, aggregator in basicFeatureAggregators.items():
        aggregated[colName] = aggregator(df[colName])
    return aggregated

def makeAuthorAggregatedFeatures(df, tref, futureWindowInDays=defaultFutureWindowInDays):
    byAuthor = makeByAuthorFeatures(df, tref, futureWindowInDays)
    return aggregateBasicAuthorFeaturesToDict(byAuthor)


