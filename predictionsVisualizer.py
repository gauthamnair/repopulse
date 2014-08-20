import singleRepoStats
import datetime
import pandas as pd
import featureMakers



def getPredictionsTrace(repoString, tend = datetime.date.today()):
	weeklyData = singleRepoStats.getRepoWeeklyData(repoString)	
	weeklyTotal = weeklyData.pivot(index='week_start', columns='author_login', values='commits_num').sum(axis=1)
	weeklyTotalResampled = featureMakers.resampleToDays(weeklyTotal)


	earliestCommit = weeklyData['week_start'].min()
	aWeekAfterFirstCommit = earliestCommit + datetime.timedelta(7)

	times = pd.date_range(start=aWeekAfterFirstCommit, 
	                      freq='W', end=tend)
	times = [x.to_datetime().date() for x in times]

	probs = [singleRepoStats.getPredictedProbAlive(weeklyData, t) for t in times]

	probTrace = pd.Series(data=probs, index=pd.to_datetime(times))

	probTraceResampled = probTrace.reindex(
		weeklyTotalResampled.index, method='ffill', limit=1)

	probTraceResampled = probTraceResampled.interpolate()

	commitsAndProb = pd.DataFrame(
		{'commits':weeklyTotalResampled, 'prob':probTraceResampled})

	return commitsAndProb



