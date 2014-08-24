library(ggplot2)
library(plyr)
library(reshape2)
library(grid)
library(data.table)

graphFileName <- function(str){
	return(paste0('data/graphs/', str, '.pdf'))
}

features <- read.csv('data/intermediate/byRepoToday.csv')
repoInfo <- read.csv('data/intermediate/infoRepos.csv')
repoInfo$X <- NULL
statsAndInfo <- merge(features, repoInfo, by.x='repo_full_name', by.y='full_name')

statsAndInfo <- subset(statsAndInfo, stargazers_count > 9)

q <- ggplot(statsAndInfo, aes(x=log10(stargazers_count)))
q <- q + geom_bar()
print(q)



q <- ggplot(statsAndInfo, aes(
	x = log10(daysSinceLastCommit + 1), color=stargazers_count>1000))
q <- q + geom_density()

pdf(graphFileName('starsVsLastCommit'), width=6, height=3)
print(q)
dev.off()
