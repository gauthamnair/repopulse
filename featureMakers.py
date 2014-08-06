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

def totalToDate(timeseries, tref):
	return timeseries.ix[:tref].sum()


def makeFeatureMakers(tref, futureWindowInDays=defaultFutureWindowInDays):
	def futureCommits_num(x):
		return totalInPeriodStarting(x, tref=tref,
			futureWindowInDays=defaultFutureWindowInDays)
	def daysSinceLastCommit(x):
		return daysSinceLastNonZero(x, tref=tref)
	def pastCommits_num(x):
		return totalToDate(x, tref=tref)
	return [futureCommits_num, daysSinceLastCommit, pastCommits_num]

