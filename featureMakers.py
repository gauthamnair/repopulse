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

def removeTimeFromWeekStartDate(df):
    df['week_start'] = pd.to_datetime([x.date() for x in df['week_start']])

def pivotToDailyCommitsByAuthor(df):
    result = df.pivot(index='week_start', columns='author_login', values='commits_num')
    result = result.fillna(0)
    result.index = pd.to_datetime([x.date() for x in result.index])
    return resampleToDays(result)

defaultFutureWindowInDays = 6*30

def today():
    return datetime.date(2014, 8, 6)

def defaultTref():
	return today() - datetime.timedelta(defaultFutureWindowInDays)


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

def getDiversity(series):
    normalized = series.values.astype(np.float64) / series.sum()
    if np.any(np.isnan(normalized)):
        return np.nan
    else:
        entropyParts = np.where(normalized > 0,
            - normalized * np.log(normalized), 0)
        return np.exp(entropyParts.sum())

class FeatureMaker:
    def __init__(self, tref, futureWindowInDays=defaultFutureWindowInDays, 
        daysToWaitBeforeFuture=daysInWeek):
        self.tref = tref
        self.daysToWaitBeforeFuture = daysToWaitBeforeFuture
        self.futureWindowInDays = futureWindowInDays

    def totalInPeriodStarting(self, timeseries):
        tstart = self.tref + datetime.timedelta(self.daysToWaitBeforeFuture)
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

    ewmaTimeScales = {
        'TwoWeeks' : 14,
        'OneMonth' : 30,
        'ThreeMonth' : 30*3,
        'SixMonth' : 30*6,
        'OneYear' : 365
    }

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
            'daysSinceFirstCommit' : self.daysSinceOldestNonZero
        }
        for timeScale, days in self.ewmaTimeScales.items():
            def makeEWMA(tseries, timeScaleInDays=days):
                return self.getEWMA(tseries, timeScaleInDays)
            makers['ewma' + timeScale] = makeEWMA

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
    }
    for timeScale in ewmaTimeScales:
        basicFeatureAggregators['ewma' + timeScale] = np.sum


    def aggregateBasicAuthorFeaturesToDict(self, byAuthorFeatures):
        aggregated = dict()
        for colName, aggregator in self.basicFeatureAggregators.items():
            aggregated[colName] = aggregator(byAuthorFeatures[colName])
        return aggregated    




    diversityFeatures = ['pastCommits_num']
    diversityFeatures += ['ewma' + timeScale for timeScale in ewmaTimeScales]

    def getAuthorDiversity(self, byAuthorFeatures):
        diversity = dict()
        for colName in self.diversityFeatures:
            diversity['diversity_' + colName] = getDiversity(byAuthorFeatures[colName])
        return diversity

  
    def getGapStats(self, dailyCommits):
        zeroRuns = get_ZeroRuns(dailyCommits).ix[:self.tref]
        stats = zeroRuns['gap_length_days'].describe().to_dict()
        return {'gapstats_'+k : v for (k,v) in stats.items()}


    def makeFeatures(self, df):
        dailyCommitsByAuthor = pivotToDailyCommitsByAuthor(df)
        byAuthor = self.makeByAuthorFeatures(dailyCommitsByAuthor)
        features = self.aggregateBasicAuthorFeaturesToDict(byAuthor)

        features.update(self.getAuthorDiversity(byAuthor))

        for scaleName, scaleDays in self.ewmaTimeScales.items():
            orig = features['ewma' + scaleName]
            adjusted = orig * np.exp(features['daysSinceLastCommit'] / float(scaleDays) )
            features['adjusted' + scaleName] = adjusted


        dailyCommits = dailyCommitsByAuthor.sum(axis=1)
        features.update(self.getGapStats(dailyCommits))
        return features




def getCommitsGaps(dailyCommitsByAuthor):
    dailyCommits = dailyCommitsByAuthor.sum(axis=1)
    dailyCommitsResampled = resampleToDays(dailyCommits)
    return get_ZeroRuns(dailyCommitsResampled)