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

class FeatureMaker:
    def __init__(self, tref, futureWindowInDays=defaultFutureWindowInDays):
        self.tref = tref
        self.futureWindowInDays = futureWindowInDays

    def totalInPeriodStarting(self, timeseries):
    	tfuture = self.tref + datetime.timedelta(self.futureWindowInDays)
    	return timeseries.ix[self.tref : tfuture].sum()

    def mostRecentNonZero(self, timeseries):
        subsetted = timeseries[timeseries > 0].ix[:self.tref]
        if len(subsetted)==0:
        	return None
        else:
        	return subsetted.index[-1]

    def daysSinceLastNonZero(self, timeseries):
        t = self.mostRecentNonZero(timeseries)
        if t == None:
        	return np.nan
        else:
    	    deltaT = self.tref - t.to_datetime().date()
    	    return deltaT.days

    def oldestNonZero(self, timeseries):
        subsetted = timeseries[timeseries > 0].ix[:self.tref]
        if len(subsetted)==0:
        	return None
        else:
        	return subsetted.index[0]

    def daysSinceOldestNonZero(self, timeseries):
        t = self.oldestNonZero(timeseries)
        if t == None:
        	return np.nan
        else:
    	    deltaT = self.tref - t.to_datetime().date()
    	    return deltaT.days

    def totalToDate(self, timeseries):
    	return timeseries.ix[:self.tref].sum()

    def makeBasicCommitsFeatureMakers(self):
        makers = {
            'futureCommits_num' :  self.totalInPeriodStarting,
            'pastCommits_num' : self.totalToDate,
            'daysSinceLastCommit' : self.daysSinceLastNonZero,
            'daysSinceFirstCommit' : self.daysSinceOldestNonZero
        }
        return {'commits_num':makers}

    def makeByAuthorFeatures(self, df):
        grouped = df[['author_login','commits_num']].groupby(['author_login'])
        aggregated = grouped.aggregate(self.makeBasicCommitsFeatureMakers())
        # to get rid of multi-index
        return aggregated['commits_num']

    basicFeatureAggregators = {
        'futureCommits_num': np.sum,
        'pastCommits_num' : np.sum,
        'daysSinceLastCommit' : np.min,
        'daysSinceFirstCommit' : np.max
    }

    def aggregateBasicAuthorFeaturesToDict(self, df):
        aggregated = dict()
        for colName, aggregator in self.basicFeatureAggregators.items():
            aggregated[colName] = aggregator(df[colName])
        return aggregated

    def makeAuthorAggregatedFeatures(self, df):
        byAuthor = self.makeByAuthorFeatures(df)
        return self.aggregateBasicAuthorFeaturesToDict(byAuthor)


