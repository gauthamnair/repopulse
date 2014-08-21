library(ggplot2)
library(plyr)
library(reshape2)
library(grid)
library(data.table)

gaps <- read.csv('data/intermediate/gapsToday.csv')
features <- read.csv('data/intermediate/byRepoToday.csv')

gaps <- data.table(gaps)

longestgap <- gaps[, list(longest_gap_days = max(gap_length_days),
	num_gaps = length(gap_length_days), num_gaps_sixM = sum(gap_length_days>30*6)),
	by='repo_full_name']


repoStats <- merge(longestgap, features[c('repo_full_name', 'pastCommits_num')],
	by='repo_full_name')

totalStats <- summarize(repoStats, num_gaps=sum(num_gaps), 
	num_gaps_sixM = sum(num_gaps_sixM),
	pastCommits_num = sum(pastCommits_num))

print(totalStats$num_gaps_sixM / totalStats$pastCommits_num)


graphFileName <- function(str){
	return(paste0('data/graphs/', str, '.pdf'))
}


binwidth <- 0.05
q_gaps <- ggplot(gaps, aes(x=log10(gap_length_days + 1) )) + 
	geom_bar(binwidth=binwidth)
q_gaps <- q_gaps + geom_vline(x=log10(c(365/2, 365)))
# print(q_gaps)

q_longest <- ggplot(longestgap, aes(x=log10(longest_gap_days + 1) )) + 
	geom_bar(binwidth=binwidth)
q_longest <- q_longest + geom_vline(x=log10(c(365/2, 365)))
# print(q_longest)

q_lastcommit <- ggplot(features, aes(x=log10(daysSinceLastCommit + 1))) + 
	geom_bar(binwidth=binwidth)
q_lastcommit <- q_lastcommit + geom_vline(x=log10(c(365/2, 365)))
# print(q_lastcommit)

pdf(graphFileName('gapStats'), width=5, height=6)
pushViewport(viewport(layout=grid.layout(3,1)))
print(q_gaps + xlim(0,3.5), vp = viewport(layout.pos.row=1))
print(q_longest + xlim(0,3.5), vp = viewport(layout.pos.row=2))
print(q_lastcommit + xlim(0,3.5), vp = viewport(layout.pos.row=3))
dev.off()



q_gapsecdf <- ggplot(data=NULL) + 
	stat_ecdf(data=gaps, aes(x=gap_length_days / 30)) +
	theme_bw() +
	xlab('months') +
	ylab('cumulative distribution') +
	scale_x_continuous(breaks=seq(0,12,2), limits=c(0,12))
print(q_gapsecdf)


makeECDF <- function(gap_lengths, days=c(0:365)){
	gapsecdf <- ecdf(gap_lengths)
	return(data.frame(days=days, prob=gapsecdf(days)))
}

q_gapsecdf <- ggplot(data=makeECDF(gaps$gap_length_days)) + 
	geom_line(aes(x=days / 30, y=prob, group=1)) +
	theme_bw() +
	xlab('months') +
	ylab('cumulative distribution') +
	scale_x_continuous(breaks=seq(0,12,2), limits=c(0,12)) +
	ylim(0, 1)

pdf(graphFileName('gapsECDF_linear'), width=3, height=2.7)
print(q_gapsecdf)
dev.off()


q_age <- ggplot(features, aes(x=daysSinceFirstCommit/365)) + geom_bar()
q_age <- q_age + xlab('age in years') + xlim(0, 10)

pdf(graphFileName('ageDistribution'), width=6, height=4.5)
print(q_age)
dev.off()




q <- ggplot(features, aes(x=gapstats_max, y=gapstats_mean))
q <- q + geom_point()
print(q)

q <- ggplot(features, aes(x=gapstats_max, y=daysSinceLastCommit))
q <- q + geom_bin2d()
q <- q + scale_fill_gradientn(colours=rainbow(7), trans='sqrt')
print(q)