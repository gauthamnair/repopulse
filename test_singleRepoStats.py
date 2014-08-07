import singleRepoStats

repoString = 'torvalds/linux'
# print singleRepoStats.getRepoCommitsStats(repoString)
probAlive = singleRepoStats.getPredictedProbAlive(repoString)

print probAlive