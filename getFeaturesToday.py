import trainingData
import featureMakers

query = '''
SELECT * FROM WeeklyContributions 
'''
fileName = 'data/intermediate/byRepoToday.csv'
tref = featureMakers.today()

trainingData.computeAndSaveToFile(query=query, fileName=fileName,
	tref = tref)