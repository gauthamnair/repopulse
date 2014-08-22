# supervisord

## devsetup version

from home:
```
sudo supervisord -c simple.conf
```

## seeing what supervisor is doing:
ps aux | grep 'supervisord'

pid should match supervisord.pid


ps aux | grep 'gunicorn'
should see 5 entries if ran gunicorn
with w=4. presumably one master and
4 workers.

## restarting or stopping supervisor:

kill -HUP [supervisord's pid]

This will make supervisor re-read the 
configuration file that it was started
with and relaunch its child processes.

kill -TERM [supervisord's pid]

This terminates supervisor and all its
child processes. Works for me.




# Installing python packages

sudo pip install numpy
verified it worked

used 
http://stackoverflow.com/questions/19595944/trouble-installing-scipy-in-virtualenv-on-a-amazon-ec2-linux-micro-instance/20890162#20890162
to install scipy:

Enables Swap:
```
sudo /bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024
sudo /sbin/mkswap /var/swap.1
sudo /sbin/swapon /var/swap.1
```

Installs some mysterious libraries:
```
sudo apt-get install -y libatlas-base-dev gfortran python-dev build-essential g++
```

then scipy install seems to work:
```
sudo pip install scipy
```

also had to install nose to
get linear_model to import
```
sudo pip install nose
```

Then disabled swap:
```
sudo swapoff /var/swap.1
sudo rm /var/swap.1
```


```
sudo pip install scikit-learn 
```
(Installs without scipy but doesn't work
if you, for example, import linear_model)


```
sudo pip install pandas
```

```
sudo pip install pymysql
```

```
sudo pip install PyGithub
```

```
sudo pip install SQLAlchemy
```

```
sudo pip install ipython
```


# MySQL

```
sudo apt-get install mysql-server-5.6
```

Then I pressed enter wherever it asked for a password
(which was multiple times).

then 
mysql -u root -p


# my code

from home:
```
git clone https://github.com
```

then in mysql created the gitdb database:
```
CREATE DATABASE gitdb
```


Just like that the gitModels seems to work!
```
python gitModels.py
```
created the databases in gitdb and did not complain

tested:
```
python test_singleRepoStats.py
```
and it worked! it added hadley/plyr to the cache
and correctly calculated the probability.


# getting the server to run.

I made sure github could authenticate
by setting the environment variable.


Then made a modified awsrun.py,

and

```
python awsrun.py
```

then browsing to:
http://54.164.92.112:5000/

worked!
the app works just fine!


Now let's go back to the gunicorn thing:

following the dev setup:
(from the home directory)

```
~ $ cat simple.conf
[program:myserver]
command=gunicorn hello:app -w 4 -b 0.0.0.0:80

[supervisord]
logfile=/home/ubuntu/supervisord.log
loglevel=debug
user=root
```

```
~$ cat hello.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

then running:
```
sudo supervisord -c simple.conf
```
makes hello world show up at my ip: 
http://54.164.92.112/

and fires up a bunch of gunicorn processes

I stopped supervisord and the gunicorn processes

Now, if I try from the command line:
```
gunicorn hello:app -b 0.0.0.0:80
```

it thinks a bit and exits without producing any output

```
gunicorn hello:app -w 1 -b 0.0.0.0:80
```

This fails too.


# working solution with div

Turns out the main problem was
that when I was sudo'ing to run
supervisord or gunicorn,
I was loosing the environment 
variable that held the github 
api authentication.

I switched how that is done, 

and with help form Div to refactor
my views.py/app.py/run.py into 
a single file, the whole thing works!



