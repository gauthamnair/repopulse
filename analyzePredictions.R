library(ggplot2)
library(plyr)
library(reshape2)
library(grid)
library(data.table)
library(stringr)

graphFileName <- function(str){
	return(paste0('data/graphs/', str, '.pdf'))
}

repoStats <- read.csv('data/intermediate/byRepoWithPredictions.csv')

# checking for repeated packages:
print(any(duplicated(repoStats$repo_full_name)))

repoStats['repo_name'] <- str_replace(repoStats$repo_full_name, '.*/', '')
print(any(duplicated(repoStats$repo_name)))

repetitionStats <- as.data.table(repoStats)
repetitionStats <- repetitionStats[, list(repo_full_name = repo_full_name, 
	number = length(repo_full_name)), by='repo_name']

print(subset(repetitionStats, number > 10))
# amusingly there are 13 packages here with name 'scripts', and 14
# with name 'dotfiles'
subset(repetitionStats, number < 10 &  number > 5)
# there are also a whole bunch of 'blog', 'python'
# and hilariously, 'django-project-template'
# who is starring these things, I don't know.

print(table(repoStats[c('aliveOrDead', 'predicted')]))

repoStats <- transform(repoStats, 
	success = ifelse(aliveOrDead==predicted, 'True', 'False'))

repoStats['exampleType'] <- with(repoStats, paste(success, aliveOrDead))

raincolors <- rev(rainbow(8)[1:7])
q <- ggplot(repoStats, aes(x=log10(daysSinceLastCommit + 1), y=probAlive)) 
q <- q + geom_bin2d(binwidth=c(0.08, 0.02))
q <- q + scale_fill_gradientn(colours=raincolors, trans='sqrt')

pdf(graphFileName('pAliveVsLastCommit'), width=5.5, height=3.5)
print(q)
dev.off()

print(q + facet_wrap(~ aliveOrDead))



falseAlive <- subset(repoStats, (probAlive > 0.95) & aliveOrDead=='dead')
falseAlive <- falseAlive[c('repo_full_name', 'daysSinceLastCommit', 'pastCommits_num', 'probAlive')]
falseAlive <- falseAlive[order(-falseAlive$pastCommits_num),]

falseDead <- subset(repoStats, (probAlive < 0.05) & aliveOrDead=='alive')
falseDead <- falseDead[c('repo_full_name', 'daysSinceLastCommit', 'pastCommits_num', 'probAlive')]
falseDead <- falseDead[order(-falseDead$pastCommits_num),]
