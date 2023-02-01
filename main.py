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
import gevent
import socket


sentense_content = None
file_content = None


def spamer(pid: int, ipaddress: str, port: int, interval: int = 1000) -> None:
    if sentense_content:
        spam_content = sentense_content
    elif file_content:
        spam_content = file_content
    else:
        return

    cnt = 0

    while 1:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((ipaddress, port))
                s.settimeout(0.1)   # recv timeout

                while 1:
                    # send
                    s.sendall(spam_content)

                    # receive
                    try:
                        data = s.recv(65535)
                    except socket.timeout:
                        pass

                    cnt += 1
                    if cnt in [0, 10]:
                        print("spamer %s: %s:%s, interval %s, sended %s times" % (pid, ipaddress, port, interval, cnt))
                        if cnt >= 10:
                            cnt = 0

                    # send timeout
                    gevent.sleep(interval * 0.001)
                # while 1
            # with socket
        except KeyboardInterrupt:
            return
        except Exception as ex:
            print("spamer %s: %s" % (pid, str(ex)))

        # reconnect timeout
        gevent.sleep(1)
    # while 1
# spamer


if __name__ == '__main__':
    parser = argparse.ArgumentParser("spamc")
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

    print("Spam to %s:%s, processes: %s, spam interval: %s, %s: %s" % (args.ip,
                                                                      args.port,
                                                                      args.processes,
                                                                      args.interval,
                                                                      "sentence" if args.sentence else "file",
                                                                      args.sentence if args.sentence else args.file))
    glist = []
    try:
        for i in range(args.processes):
            glist.append(gevent.spawn(spamer, i, args.ip, args.port, args.interval))

        if len(glist):
            gevent.joinall(glist)
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(str(ex))
        exit(1)
