import singleRepoStats

repoString = 'hadley/plyr'
print singleRepoStats.getRepoCommitsStats(repoString)
probAlive = singleRepoStats.getPredictedProbAlive(repoString)

print probAlive