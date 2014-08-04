import gitModels
from gitImporter import importer

# make sure that the Repo table is clean so that only the inserted
# guy is t

import logging
logging.basicConfig(level=logging.INFO)

plyr = importer.getRepo('hadley/plyr')


stored = gitModels.makeRepo(
	full_name = plyr.full_name,
	fork = plyr.fork,
	owner_login = plyr.owner.login,
	has_wiki = plyr.has_wiki
	)


fromdb = gitModels.session.query(gitModels.Repo).first()

assert(fromdb.full_name == stored.full_name)
gitModels.session.commit()