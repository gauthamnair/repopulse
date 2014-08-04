from github import Github
import os

mypw = os.environ['GITPASSWD']
g = Github('gauthamnair', mypw)


ratelimit = g.get_rate_limit()

print ratelimit.rate.limit

hadley = g.get_user('hadley')

repos = {repo.name:repo for repo in hadley.get_repos()}

plyr = repos['plyr']

print plyr.created_at

hadleyAsOwner = plyr.owner

print hadleyAsOwner.name

print (hadley == hadleyAsOwner)


commits = list(plyr.get_commits())
# using g.get_rate_limit().rate.remaining
# can see that each pagination counts as an api call.

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

print len(sr.get_page(13))
#0

firstRepo = p0[0]
print type(firstRepo)
# github Repository

print firstRepo.owner.login
print firstRepo.full_name
print firstRepo.fork

def storeRepo()
