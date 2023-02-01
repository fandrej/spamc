# This is a simple Python socket client for spam.
### Installation
```
cd /opt
git clone https://github.com/fandrej/spamc.git
sudo chown -R user:group spamc
sudo chmod -R g+w spamc
cd spamc
python3 -m venv $(pwd)/venv
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
