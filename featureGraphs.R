library(ggplot2)
library(plyr)
library(reshape2)

repoStats <- read.csv('data/intermediate/byRepo.csv')
repoStats$X <- NULL
repoStats$aliveOrDead <- ifelse(repoStats$futureCommits_num > 0,
	'alive', 'dead')

graphFileName <- function(str){
	return(paste0('data/graphs/', str, '.pdf'))
}



q <- ggplot(repoStats, aes(x=log10(daysSinceLastCommit+1)))
q <- q + geom_bar()
q <- q + facet_wrap(~aliveOrDead)

pdf(graphFileName('daysSinceLastCommit'), width=5.5, height=3)
print(q)
dev.off()

melted <- melt(repoStats, id.vars = c('repo_full_name', 'aliveOrDead'))

graphOneExplanatory <- function(df){
	q <- ggplot(df, aes(x=log10(value+1)))
	q <- q + geom_bar()
	q <- q + facet_grid(aliveOrDead ~ .)
	q <- q + xlab(paste('log10(', df$variable[1], '+ 1)'))
	return(q)
}

pdf(graphFileName('allLogExplanatory'), width = 3.7, height = 4.6)
d_ply(melted, 'variable', function(x){
	print(graphOneExplanatory(x))
	})
dev.off()


hundredDaysLastCommit <- subset(repoStats, 
	(daysSinceLastCommit >= 100) &  (daysSinceLastCommit <= 150) )

q <- ggplot(hundredDaysLastCommit, 
	aes(x=diversity_ewmaSixMonth))
q <- q + geom_bar()
q <- q + facet_wrap(~aliveOrDead)
print(q)