import singleRepoStats

repoString = 'torvalds/linux'
probAlive = singleRepoStats.getPredictedProbAlive(repoString)

print probAlive