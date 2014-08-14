import trainingData
import featureMakers

query = '''
SELECT * FROM WeeklyContributions 
WHERE repo_full_name IN ('hadley/plyr', 'pydata/pandas', 'gentinex/kaggle')
'''
fileName = 'data/intermediate/small.csv'

trainingData.computeAndSaveToFile(query=query, fileName=fileName,
	tref = featureMakers.today())