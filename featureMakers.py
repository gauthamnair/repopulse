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
        limit=daysInWeek-1)
    x = x/daysInWeek
    x = x.fillna(0)
    return x

def setIndexToWeekStartDate(df):
    df.index = pd.to_datetime([x.date() for x in df['week_start']])

def pivotToDailyCommitsByAuthor(df):
    result = df.pivot(index='week_start', columns='author_login', values='commits_num')
    result = result.fillna(0)
    result.index = pd.to_datetime([x.date() for x in result.index])
    return resampleToDays(result)

defaultFutureWindowInDays = 6*30

def defaultTref():
	return datetime.date(2014, 8, 6) - datetime.timedelta(defaultFutureWindowInDays)

nsInADay = 10**9 * 3600 * 24

def get_ZeroRuns(continuousSeries):
    noActivity = continuousSeries == 0
    different_from_last = noActivity.diff()
    different_from_last[0] = False
    gap_ends = continuousSeries[~noActivity & different_from_last].index.values
    gap_starts = continuousSeries[noActivity & different_from_last].index.values
    if len(gap_starts) > len(gap_ends):
        gap_starts = gap_starts[:-1]
    result = pd.DataFrame(data={'gap_start': gap_starts, 'gap_end' : gap_ends}, 
        index = gap_ends)
    result.index.name = 'gap_end'
    gaps = result['gap_end'] - result['gap_start']
    result['gap_length_days'] = gaps.values.astype(np.float64)/nsInADay
    return result


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

    def getEWMA(self, timeseries, timeScaleInDays=30):
        ewmaseries = pd.ewma(timeseries.ix[:self.tref], com=timeScaleInDays)
        if len(ewmaseries) == 0:
            return 0
        else:
            return ewmaseries.values[-1]

    def ewmaTwoWeeks(self, timeseries):
        return self.getEWMA(timeseries, timeScaleInDays=14)

    def ewmaOneMonth(self, timeseries):
        return self.getEWMA(timeseries, timeScaleInDays=30)
    
    def ewmaThreeMonth(self, timeseries):
        return self.getEWMA(timeseries, timeScaleInDays=30*3)

    def ewmaSixMonth(self, timeseries):
        return self.getEWMA(timeseries, timeScaleInDays=30*6)

    def ewmaOneYear(self, timeseries):
        return self.getEWMA(timeseries, timeScaleInDays=365)

    def makeBasicCommitsFeatureMakers(self):
        makers = {
            'futureCommits_num' :  self.totalInPeriodStarting,
            'pastCommits_num' : self.totalToDate,
            'daysSinceLastCommit' : self.daysSinceLastNonZero,
            'daysSinceFirstCommit' : self.daysSinceOldestNonZero,
            'ewmaTwoWeeks' : self.ewmaTwoWeeks,
            'ewmaOneMonth' : self.ewmaOneMonth,
            'ewmaThreeMonth' : self.ewmaThreeMonth,
            'ewmaSixMonth' : self.ewmaSixMonth,
            'ewmaOneYear' : self.ewmaOneYear,
        }
        return makers

    def makeByAuthorFeatures(self, dailyCommitsByAuthor):
        makers = self.makeBasicCommitsFeatureMakers()
        def makeFeatures(continuousSeries):
            names, values = zip(*[(name,f(continuousSeries)) for (name,f) in makers.items()])
            return pd.Series(values, index=names)
        return dailyCommitsByAuthor.apply(makeFeatures).T

    basicFeatureAggregators = {
        'futureCommits_num': np.sum,
        'pastCommits_num' : np.sum,
        'daysSinceLastCommit' : np.min,
        'daysSinceFirstCommit' : np.max,
        'ewmaTwoWeeks' : np.sum,
        'ewmaOneMonth' : np.sum,
        'ewmaThreeMonth' : np.sum,
        'ewmaSixMonth' : np.sum,
        'ewmaOneYear' : np.sum,
    }

    diversityFeatures = [
        'pastCommits_num',
        'ewmaTwoWeeks',
        'ewmaOneMonth',
        'ewmaThreeMonth',
        'ewmaSixMonth',
        'ewmaOneYear']

    def aggregateBasicAuthorFeaturesToDict(self, byAuthorFeatures):
        aggregated = dict()
        for colName, aggregator in self.basicFeatureAggregators.items():
            aggregated[colName] = aggregator(byAuthorFeatures[colName])
        return aggregated

    def makeGapsFeature(self, df):
        aggregatedSeries = df['commits_num'].groupby(level=0).aggregate(np.sum)
        gaps = get_ZeroRuns(resampleToDays(aggregatedSeries))
        return(gaps)        

    def makeFeatures(self, df):
        dailyCommitsVsAuthor = pivotToDailyCommitsByAuthor(df)
        byAuthor = self.makeByAuthorFeatures(dailyCommitsVsAuthor)
        simpleAggregations = self.aggregateBasicAuthorFeaturesToDict(byAuthor)

        return simpleAggregations




