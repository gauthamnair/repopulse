import gitImporter
import gitModels

importer = gitImporter.importer

qstr = 'language:R stars:>1'

sr = importer.g.search_repositories(qstr)

queryChunker = gitImporter.SearchQueryChunker(
	importer,qstr)

si = queryChunker.searchCurrentInterval()
sires = list(si)

reposGenerator = queryChunker.search()

repos = list(reposGenerator)

print len(repos)
# gives 2363 - it works!