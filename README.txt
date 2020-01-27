
sudo apt-get install python-pip python-dev build-essential vim
sudo pip2 install pysnmp
sudo pip install lxml

# redis 

sudo apt-get install redis-server
 
 or
 
sudo pip install redis

redis-cli
127.0.0.1:6379> get obvescanje-FailStates
127.0.0.1:6379> get obvescanje-OKStates
127.0.0.1:6379> get poller-data


# cron 

* * * * * /home/pi/scripts/poller_obve/poller.py 2>&1
* * * * * /home/pi/scripts/poller_obve/obvescanje.py 2>&1



# usage:

./poller.py --help
Usage: poller.py

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -d           Debug nacin
  -l LOG_FILE  Debug, zapisovanje v Log file
  -n           Ne posiljaj metrik v graphite
  -j JSON      Zapisi metrike v json
  -m           Pozeni, vendar ne posiljaj SMS-ov

  
  
./obvescanje.py --help
Usage: obvescanje.py

Options:
  --version         show program's version number and exit
  -h, --help        show this help message and exit
  -d                Debug nacin
  -l LOG_FILE       Debug zapis v Log file
  -m                Pozeni, vendar ne posiljaj SMS-ov
  -u TEST_SMS_USER  Poslji testni SMS uporabniku "-u Peter"
  -t TEST_SMS       Nastavi besedilo testnemu SMS-ju: -t "Testno sporocilo"
