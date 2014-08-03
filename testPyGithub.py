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
