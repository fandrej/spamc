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

### Run examles
```
source venv/bin/activate
python ./main.py 127.0.0.1 2000 -p 1 -s "Test"
python ./main.py 127.0.0.1 2000 -p 1 -f files/galileo-big.bin
```   
or
```
./run.sh python ./main.py 127.0.0.1 2000 -p 1 -s "Test"
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
