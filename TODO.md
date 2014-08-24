
# fortify the app and presentation

- make screenshots of the app in action
- add a demo mode with a hyperlink to the github python api
- figure out why it sometimes does not work with Chrome
	- found that there is a timeout occasionally on getRepo




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
