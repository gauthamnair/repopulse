
## Problem setup

A repository is created at a time t_0
There is a stream of commits that occur
at times:
{t_i}

We are a time T, attempting to predict
if there will be any events between
T and T + D. D is probably going to be
6 months.




## Ideas for features

repo language

time since repo creation
time since last commit

exponentially weighted 
moving average of commit number
over the past week, month, six months

exponentially weighted
committer diversity over past
weeks, months, six months.