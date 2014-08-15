library(ggplot2)
library(plyr)
library(reshape2)
library(grid)
library(data.table)

gaps <- read.csv('data/intermediate/gapsToday.csv')
features <- read.csv('data/intermediate/byRepoToday.csv')

gaps <- data.table(gaps)

longestgap <- gaps[, list(longest_gap_days = max(gap_length_days)),
	by='repo_full_name']

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



q_age <- ggplot(features, aes(x=daysSinceFirstCommit/365)) + geom_bar()
print(q_age)