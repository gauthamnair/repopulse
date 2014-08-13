import singleRepoStats

repoString = 'hadley/plyr'
z= singleRepoStats.getRepoWeeklyData(repoString)

weeklyTotal = z.pivot(index='week_start', columns='author_login', values='commits_num').sum(axis=1)

x = [{'week_start': str(t.date()), 'commits_num': c} for (t,c) in zip(weeklyTotal.index, weeklyTotal.values)]

probAlive = singleRepoStats.getPredictedProbAlive(z)

print probAlive