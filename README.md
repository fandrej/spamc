# This is a simple Python socket client for spam.
## Designed for load testing
### Installation
```
cd /opt
git clone https://github.com/fandrej/spamc.git
sudo chown -R user:group spamc
sudo chmod -R g+w spamc
cd spamc
python3 -m venv $(pwd)/venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### Parameters
```
./run.sh python ./main.py -h
usage: python ./main.py [-h] [-p PROCESSES] [-i INTERVAL] [-s SENTENCE] [-f FILE] ip port

positional arguments:
  ip                    ip address to spam
  port                  port number

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        number of spam processes
  -i INTERVAL, --interval INTERVAL
                        spam interval (millisec.) per process
  -s SENTENCE, --sentence SENTENCE
                        spam phrase quoted if it contains spaces
  -f FILE, --file FILE  spam file
```

### Run examles
```
ulimit -n 10000
source venv/bin/activate
python ./main.py 127.0.0.1 2000 -p 1000 -s "Test"
python ./main.py 127.0.0.1 2000 -p 1000 -f files/galileo-big.bin
```   
or
```
ulimit -n 10000
./run.sh python ./main.py 127.0.0.1 2000 -p 1000 -s "Test"
```

### Receive spam
```
sudo apt update
sudo apt -y install ncat
ncat -klp 2000 -w 10
```

### Dumping
#### Receiver side
```
sudo tcpdump -i eth0 port 2000 -w /tmp/in.pcap
```

#### Sender side
```
sudo tcpdump -i eth0 src host 127.0.0.1 -w /tmp/out.pcap
```
