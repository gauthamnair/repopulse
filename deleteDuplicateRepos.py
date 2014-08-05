import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');
c = con.cursor()


makeDuplicateIdTables = '''
CREATE TEMPORARY TABLE dupRepos AS 
SELECT r1.id AS id
    FROM Repos r1 JOIN Repos r2
    ON (r1.full_name = r2.full_name AND r1.id < r2.id)
'''
c.execute(makeDuplicateIdTables)
con.commit()

query = "DELETE FROM Repos WHERE Repos.id IN (SELECT dupRepos.id FROM dupRepos)"
c.execute(query)
con.commit()

dropDuplicateIdTables = "DROP TABLE IF EXISTS dupRepos"
c.execute(dropDuplicateIdTables)
con.commit()

