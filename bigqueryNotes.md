
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

SELECT repository_name, count(repository_name) as pushes, repository_description, repository_url
FROM [githubarchive:github.timeline]
WHERE type="PushEvent"
    AND repository_language="Ruby"
    AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
GROUP BY repository_name, repository_description, repository_url
ORDER BY pushes DESC
LIMIT 100;

I click RUN QUERY, it works for 9.6s:

"Query complete (9.6s elapsed, 28.8 GB processed)"

and the query results is populated. The option to download as CSV is given.



## Useful Links

bigQuery SQL:

https://developers.google.com/bigquery/query-reference

bigQuery results schema:

https://github.com/igrigorik/githubarchive.org/blob/master/bigquery/schema.js

This is enormous and shows ~ 200 fields available. But they are grouped
and could be browseable in some
other form.

