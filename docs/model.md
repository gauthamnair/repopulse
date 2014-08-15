

# Predictor Accuracy Metrics

The model predicts a repository as inactive (0) or active (1). There are two types of mistakes we could make:

- Classifying an inactive repository as active. The user then downloads it and it turns out it is not actively maintained any more. This is a false positive.

The false positive rate is the probability that a true negative is classified as positive. It is independent of sample composition.

Precision is the probability that a positive classifier call is actually positive.
This *does* depend on the sample composition. The greater the fraction of true negatives, the greater the chance of a false positive, and therefore the precision will be lower. 

Precision is the probability that a positive-classified is positive.

Recall is the probability that a positive is positive-classified.

Recall is the probability that an positive sample will be classified as positive. A high Recall means a high Sensitivity. They are the same. This does not depend on the test sample composition.

Specificity is the probability that a negative sample is classified as negative. 

an ROC plot is a graph of the recall (or true positive rate = y) against the false negative rate = x. 

ROC curves are therefore insensitive to the class distribution, which is great for me.

- Classifying an active repository as inactive. This is unfair to the developer, but does not harm the downloader so much.


https://cours.etsmtl.ca/sys828/REFS/A1/Fawcett_PRL2006.pdf


# Time Series Validation


Here's my situation:
- I have a full time trace from birth for commit events for thousands of github repositories. As you know, commits are sporadic, sometimes with long gaps.


- I want to predict the probability there will be any commits at all in a 6 month period into the future for any github repository the user wants to inspect.

- My approach: convert the problem into a classification problem. 
Every training example can be specified as a pair 

trainingPoint = (repo, t).

repo: a repository
t :  a time more than 6 months into the past but not older than the repository itself.


# Cross-Validation Schemes

## Single Time, cross-repo

What I have been using so far. Consider a training set 

There is only one t = t0

train = [(r, t0) for r in trainingRepos]
test = [(r, t0) for r NOT in trainingRepos]

Very easy to do.


## Cross-Time, overlapping-repos

t0: a very early time
t1: a more recent time, past the period used to compute the target for (r, t0)

train = [(r, t0) for r in Repos]
test = [(r, t1) for r in Repos]


## MultiTime, cross-repo

This would involve sampling the same repo at a bunch of times.

train = [(r, t) for t in legalTimes(r) if t &lt t0 for r in Repos]

There are several ways to compute the legalTimes for the Repo:

- proportional to the lifetime of the repo
