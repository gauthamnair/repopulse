from github import Github

g = Github()

hadley = g.get_user('hadley')

repos = {repo.name:repo for repo in hadley.get_repos()}

plyr = repos['plyr']

print plyr.created_at

hadleyAsOwner = plyr.owner

print hadleyAsOwner.name

print (hadley == hadleyAsOwner)


commits = list(plyr.get_commits())

print len(commits)
# says 715
# Exactly matches what Github website says!

# try doing it by hand:

import requests
plyrCommitsURL = r'https://api.github.com/repos/hadley/plyr/commits'
r = requests.get(plyrCommitsURL)
asjson = r.json()
print len(asjson)
#says 30: probably needs pagination
print r.headers['link']
# Yes - best to use pygithub :)


# Try to get a list of repositories:



qstr = 'language:R created:"<= 2011-01-01"'

sr = g.search_repositories(query=qstr)

print sr.totalCount
# gives 354, same as the github website

p0 = sr.get_page(0)
print len(p0)
#30

print len(sr.get_page(13

firstRepo = p0[0]
print type(firstRepo)
# github Repository

print firstRepo.owner.login
print firstRepo.fork
