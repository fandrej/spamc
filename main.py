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


def spamer(pid: int, ipaddress: str, port: int, interval: int = 1000, sentence: str = None, path: str = None) -> None:
    if sentence:
        spam_content = str.encode(sentence)
    elif path:
        try:
            with open(path, "rb") as f:
                spam_content = f.read()
        except Exception as ex:
            print("spamer %s: %s" % (pid, str(ex)))
            return
    else:
        return

    while 1:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((ipaddress, port))
                s.settimeout(0.1)   # recv timeout

                while 1:
                    print("spamer %s: %s:%s, spam %s, interval %s" % (
                        pid, ipaddress, port, sentence if sentence else path, interval))

                    # send
                    s.sendall(spam_content)
                    # receive
                    data = s.recv(65535)
                    # send timeout
                    gevent.sleep(interval * 0.001)
            # with socket

            # reconnect timeout
            gevent.sleep(1)

        except (KeyboardInterrupt, socket.timeout):
            pass
        except Exception as ex:
            print("spamer %s: %s" % (pid, str(ex)))
    # while 1
# spamer


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser("spamc")
    parser.add_argument("ip", type=str, help="ip address to spam")
    parser.add_argument("port", type=int, help="port number")
    parser.add_argument("-p", "--processes", type=int, help="number of spam processes", default=10)
    parser.add_argument("-i", "--interval", type=int, help="spam interval (millises.) per process", default=1000)
    parser.add_argument("-s", "--sentence", type=str,
                        help="spam phrase quoted if it contains spaces")
    parser.add_argument("-f", "--file", type=str, help="spam file")
    args = parser.parse_args()

    print(args)

    if not args.sentence and not args.file:
        print("Specify a sentence or file")
        exit(1)

    glist = []
    for i in range(args.processes):
        glist.append(gevent.spawn(spamer, i, args.ip, args.port, args.interval, args.sentence, args.file))

    print("Spam to %s:%s, processes: %s, spam interval: %s, %s: %s" % (args.ip,
                                                                      args.port,
                                                                      args.processes,
                                                                      args.interval,
                                                                      "sentence" if args.sentence else "file",
                                                                      args.sentence if args.sentence else args.file))
    try:
        gevent.joinall(glist)
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(str(ex))
