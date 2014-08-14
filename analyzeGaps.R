library(ggplot2)
library(plyr)
library(reshape2)

gaps <- read.csv('data/intermediate/gaps.csv')

q <- ggplot(gaps, aes(x=log10(gap_length_days) )) + geom_bar()
q <- q + geom_vline(x=log10(c(365/2, 365)))
print(q)