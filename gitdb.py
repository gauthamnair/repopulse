import pymysql as mdb
import logging

con = mdb.connect('localhost', 'root', '', 'gitdb'); 

repoSchema = {
	'Id' : 'INT PRIMARY KEY AUTO_INCREMENT',
	'fork' : 'BOOLEAN',
	'full_name' : 'VARCHAR(1024)',
	'name' : 'VARCHAR(1024)',
	'owner_login' : 'VARCHAR(1024)',
	'has_wiki' : 'BOOLEAN',
	'has_issues' : 'BOOLEAN',
	'homepage' : 'VARCHAR(1024)',
	'language' : 'VARCHAR(1024)',
	'description' : 'TEXT',
	'created_at' : 'DATETIME',
	'pushed_at' : 'DATETIME',
	'size' : 'INT'
}

def initializeReposTable():
	schemaStatement = ','.join([k+' '+v for (k,v) in repoSchema.items()])
	createStatement = "CREATE TABLE Repos (%s);" % schemaStatement
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS Repos")
		cur = con.cursor()
		cur.execute(createStatement)


def storeRepo(repo):
	kvpairs = {
		'fork' : repo.fork + 0,
		'full_name' : repo.full_name,
		'name' : repo.name,
		'owner_login' : repo.owner.login,
		'has_wiki' : repo.has_wiki + 0,
		'has_issues' : repo.has_issues + 0,
		'homepage' : repo.homepage,
		'language' : repo.language,
		'description' : repo.description,
		'created_at' : repo.created_at,
		'pushed_at' : repo.pushed_at,
		'size' : repo.size
	}
	colNames = []
	formatStrings = []
	values = []

	for colName, value in kvpairs.items():
		if not value == None:
			colNames.append(colName)
			values.append(value)
			formatStrings.append('%s')

	insertStatement = "INSERT INTO %s(%s) VALUES(%s)" % (
		'Repos', 
		', '.join(colNames), 
		', '.join(formatStrings))
	logging.info(insertStatement)
	logging.info(values)
	with con:
		cur = con.cursor()
		return cur.execute(insertStatement, tuple(values))
