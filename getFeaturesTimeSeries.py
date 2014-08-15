import trainingData
import featureMakers

query = '''
SELECT * FROM WeeklyContributions 
WHERE repo_full_name IN ('hadley/plyr', 'pydata/pandas')
'''
fileName = 'data/intermediate/small.csv'
tref = featureMakers.today()

trainingData.computeAndSaveToFile(query=query, fileName=fileName,
	tref = tref)