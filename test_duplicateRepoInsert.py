from gitImporter import importer
import gitModels

linux = importer.getRepo('torvalds/linux')
gitModels.makeRepo(linux)
gitModels.makeRepo(linux)
# second prints, if logging is enabled:
# INFO:root:A repo torvalds/linux already exists. ignoring insert and returning existing
gitModels.session.commit()


indb = gitModels.session.query(gitModels.Repo).filter_by(full_name='torvalds/linux').all()

assert(len(indb) == 1)
assert(indb[0].full_name == 'torvalds/linux')