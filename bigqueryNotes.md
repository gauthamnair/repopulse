
http://www.githubarchive.org/

says that you can get things from
bigQuery. I set up an account with google
(the same one I use for my lab's probe-db)
and was able to run queries from the
web browser.


## Log:

I created a google "project":
https://console.developers.google.com/project

PROJECT NAME: repoPulse
PROJECT ID: repo-pulse


Then went to queries:
https://bigquery.cloud.google.com/queries/repo-pulse


Here's the example query from google for github:

```
SELECT repository_name, count(repository_name) as pushes, repository_description, repository_url
FROM [githubarchive:github.timeline]
WHERE type="PushEvent"
    AND repository_language="Ruby"
    AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
GROUP BY repository_name, repository_description, repository_url
ORDER BY pushes DESC
LIMIT 100;
```

I click RUN QUERY, it works for 9.6s:

"Query complete (9.6s elapsed, 28.8 GB processed)"

and the query results is populated. The option to download as CSV is given.


## Improving queries:

querying for hadley's R repositories, organized by how many pushes since April 2012, showing when the repository was created.

```
SELECT repository_name, count(repository_name) as pushes, repository_created_at, repository_url
FROM [githubarchive:github.timeline]
WHERE type="PushEvent"
    AND repository_language="R"
    AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
    AND repository_owner="hadley"
GROUP BY repository_name, repository_created_at, repository_url
ORDER BY pushes DESC
LIMIT 100;
```

The result looks about right:
```
repository_name	pushes	repository_created_at	repository_url
dplyr	695	2012-10-28 13:39:17	https://github.com/hadley/dplyr
devtools	662	2010-05-03 04:08:49	https://github.com/hadley/devtools
adv-r	586	2013-08-20 11:43:03	https://github.com/hadley/adv-r
ggplot2	537	2008-05-25 01:21:32	https://github.com/hadley/ggplot2
httr	195	2011-11-11 15:05:00	https://github.com/hadley/httr
lubridate	113	2009-03-11 01:18:52	https://github.com/hadley/lubridate
plyr	100	2008-11-19 15:08:14	https://github.com/hadley/plyr
pryr	69	2013-01-07 23:19:25	https://github.com/hadley/pryr
...
```


## pushes on dplyr

```
SELECT repository_name, created_at, actor_attributes_name
FROM [githubarchive:github.timeline]
WHERE type="PushEvent"
    AND repository_name="dplyr"
    AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
    AND repository_owner="hadley"
ORDER BY created_at DESC
LIMIT 100;
```

The result looks good, with lots of pushes from Hadley. By adding:

```
AND NOT actor_attributes_name="Hadley Wickham"
```
I could see who else contributed


Need to query for old repositories and see if I can group commits by month.





## Useful Links

bigQuery SQL:

https://developers.google.com/bigquery/query-reference

bigQuery results schema:

https://github.com/igrigorik/githubarchive.org/blob/master/bigquery/schema.js

This is enormous and shows ~ 200 fields available. But they are grouped
and could be browseable in some
other form.

