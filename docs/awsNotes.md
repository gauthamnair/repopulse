# supervisord

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

works and I can 
