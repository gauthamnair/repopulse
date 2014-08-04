import gitModels
from gitImporter import importer

# make sure that the Repo table is clean so that only the inserted
# guy is t

import logging
logging.basicConfig(level=logging.INFO)

plyr = importer.getRepo('hadley/plyr')


stored = gitModels.makeRepo(plyr)


fromdb = gitModels.session.query(gitModels.Repo).first()

assert(fromdb.full_name == stored.full_name)
gitModels.session.commit()