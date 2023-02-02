"""
This is a simple Python socket client for spam.
Author: Andrey Fedorov, mail@locman.org

Help:
https://vovkd.github.io/gevent-tutorial/
https://realpython.com/python-sockets/

Receive spam:
windows:
    nc.exe -L -p 2000
linux:
    ncat -klp 2000 -w 10
"""

import argparse
import socket
import time
import random
from multiprocessing import Process


sentense_content = None
file_content = None


def spamer(pid: int, ipaddress: str, port: int, interval: int = 1000) -> None:
    if sentense_content:
        spam_content = sentense_content
    elif file_content:
        spam_content = file_content
    else:
        return

    time.sleep(random.random())
    while 1:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((ipaddress, port))
                s.settimeout(0.5)   # recv timeout

                while 1:
                    # send
                    s.sendall(spam_content)

                    # receive
                    try:
                        data = s.recv(65535)
                    except socket.timeout:
                        pass

                    # send timeout
                    time.sleep(interval * 0.001)
                # while 1
            # with socket
        except KeyboardInterrupt:
            return
        except Exception as ex:
            print("spamer %s: %s" % (pid, str(ex)))

        # reconnect timeout
        time.sleep(1)
    # while 1
# spamer


if __name__ == '__main__':
    parser = argparse.ArgumentParser("python ./main.py")
    parser.add_argument("ip", type=str, help="ip address to spam")
    parser.add_argument("port", type=int, help="port number")
    parser.add_argument("-p", "--processes", type=int, help="number of spam processes", default=10)
    parser.add_argument("-i", "--interval", type=int, help="spam interval (millisec.) per process", default=1000)
    parser.add_argument("-s", "--sentence", type=str,
                        help="spam phrase quoted if it contains spaces")
    parser.add_argument("-f", "--file", type=str, help="spam file")
    args = parser.parse_args()

    if args.sentence:
        sentense_content = str.encode(args.sentence)
    elif args.file:
        try:
            with open(args.file, "rb") as f:
                file_content = f.read()
        except Exception as ex:
            print("file %s error: %s" % (args.file, str(ex)))
            exit(1)
    else:
        print("Specify a sentence or file")
        exit(1)

    if(args.processes <= 0):
        print("Invalid parameter processes")
        exit(1)

    if(args.interval <= 0):
        print("Invalid parameter interval")
        exit(1)

    print("Spam to %s:%s, processes: %s, spam interval: %s, %s: %s" % (args.ip,
                                                                      args.port,
                                                                      args.processes,
                                                                      args.interval,
                                                                      "sentence" if args.sentence else "file",
                                                                      args.sentence if args.sentence else args.file))
    procs = []

    try:
        for i in range(args.processes):
            p = Process(target=spamer, args=(i, args.ip, args.port, args.interval,), daemon=True)
            procs.append(p)
            p.start()

        [proc.join() for proc in procs]
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(str(ex))
        exit(1)
