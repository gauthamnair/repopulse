import singleRepoStats

repoString = 'hadley/plyr'
z= singleRepoStats.getRepoWeeklyData(repoString)
probAlive = singleRepoStats.getPredictedProbAlive(z)

print probAlive