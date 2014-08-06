import pandas as pd
import datetime

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
	return datetime.date.today() - datetime.timedelta(defaultFutureWindowInDays)

def totalInPeriodStarting(timeseries, tref, 
		futureWindowInDays = defaultFutureWindowInDays):

	tfuture = tref + datetime.timedelta(futureWindowInDays)
	return timeseries.ix[tref : tfuture].sum()

def totalInDefaultPeriod(timeseries):
	return totalInPeriodStarting(timeseries, defaultTref())

def mostRecentNonZero(timeseries, tref):
    subsetted = timeseries[timeseries>0].ix[:tref]
    return subsetted.index[-1]

def daysSinceLastNonZero(timeseries, tref):
    t = mostRecentNonZero(timeseries, tref)
    deltaT = tref - t.to_datetime().date()
    return deltaT.days