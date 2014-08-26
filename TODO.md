
# fortify the app and presentation

- add a demo mode with a hyperlink to the github python api
- make screenshots of the app in action
? figure out why it sometimes does not work with Chrome
	x found that there is a timeout occasionally on getRepo
	x think I fixed it by adding auto retry to singleRepoStats
x checked app on pc chrome and pc IE
x put slides on slideshare/slides.com
x check for duplicate entries in package names
- remake plots of independent variables against the dependent variable.

x what exactly is the rate of misclassification of each case?
x find some examples of packages mistakenly taken for dead
	and packages mistakenly taken for alive
x what is the straight-up classification error on the training set?
	16% of called-Dead are alive
	24% of called-Alive are dead

- what is the effect of regularization?
x what is the effect of stars?

- articulate the problem with choosing a time horizon
- notes on other classifiers I attempted to use





# analysis

x explore gap time distribution to discuss live/dead cutoff
x graph how quickly the algorithm predicts death for a repo.
- check that the EWMA code is doing the right thing. Diversity seems too big.
- implement a learning curve visualizer
- clean up feature-making tests
- see if gaps can be reincorporated, replacing nans with zeros.



# deployment

x propagated feature-making/training changes up to the website.

# user experience

Notes from talking to Div and Brandon:

the parameters to tune in a RandomForest are:
- max_features (mostly)
- n_estimators (a little)

the parameters to tune in a grandient boosting classifier:
- max_depth (key)

brandon also pointed me to his repo in which he has
encapsulated some of these workflows for reuse:

https://github.com/brandonckelly/bck_stats
note especially
bck_stats/sklearn_estimator_suite.py
