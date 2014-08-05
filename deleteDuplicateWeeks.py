import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');
c = con.cursor()

weeklyContributionDuplicates = '''
CREATE TABLE DupWeeks AS 
SELECT w1.* 
    FROM WeeklyContributions w1 JOIN WeeklyContributions w2
    ON (w1.repo_full_name = w2.repo_full_name 
        AND w1.author_login = w2.author_login
        AND w1.week_start = w2.week_start
        AND w1.id < w2.id)
'''
c.execute(weeklyContributionDuplicates)
con.commit()


query = '''
SELECT * FROM WeeklyContributions 
WHERE WeeklyContributions.id IN (SELECT DupWeeks.id FROM DupWeeks)
'''
c.execute(query)

deleteRequest = '''
DELETE FROM WeeklyContributions 
WHERE WeeklyContributions.id IN (SELECT DupWeeks.id FROM DupWeeks)
'''
c.execute(deleteRequest)
con.commit()
