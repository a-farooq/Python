#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) game application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
#import enchant
import tkinter


wordlist = []
namelist = []
clients = []
addresses = {}
#dic = enchant.Dict("en_US")


def is_new(word):
    if word not in wordlist:
        wordlist.append(word)
        return True

    return False


def close_thread(client):
    print("Thread closing for " + str(client))
    client.close()
    clients.remove(client)
    pass


def quit_game(name, client):
    namelist.remove(name)
    # broadcast(bytes("%s has left the game." % name, "utf8"))
    msg = "%s has quit the game!" % name
    print(msg)
    broadcast(msg, client)
    pass


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:

        client_sockid, client_address = SERVER.accept()

        if len(clients) == 0:
            wordlist.clear()

        clients.append(client_sockid)
        print("%s:%s has connected." % client_address)
        # welcome = "WELCOME"
        str_to_send = "WELCOME-"+str(tkinter.NORMAL)+"-"+str(len(clients))
        print("msg_to_send: "+str_to_send)
        client_sockid.send(str.encode(str_to_send))

        Thread(target=handle_client, args=(client_sockid,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Thread - Handles a single client connection."""

    name = ""
    while True:
        print("Waiting for name")
        str_recd = client.recv(BUFSIZ).decode("utf8")
        print("str_recd: "+str_recd)
        code = str_recd.split('-')[0]
        name = str_recd.split('-')[1]

        print("Received " + name)
        if code == "QUIT":
            close_thread(client)
            return
        elif code == "UNAME":
            if len(namelist) > 0 and name in namelist:  # checking duplicate username
                # msg = "The username \"" + name + "\" is taken. Try another name."
                str_to_send = "UNAME_FAIL-" + "" + "-" + ""
                print("str_to_send: " + str_to_send)
                client.send(str.encode(str_to_send))
            else:
                str_to_send = "UNAME_OK-" + "" + "-" + str(len(clients))
                print("str_to_send: " + str_to_send)
                client.send(str.encode(str_to_send))
                break

    msg = "%s has joined the game!" % name
    print(msg)
    broadcast(msg, client)
    namelist.append(name)

    while True:
        try:
            print("Thread waiting for word from "+name)
            str_recd = client.recv(BUFSIZ).decode('utf-8')
            print("str_recd: " + str_recd)
            code = str_recd.split('-')[0]
            word = str_recd.split('-')[1]

            if code == "QUIT":  # client closed
                # client.send(bytes("quit", "utf8")) #broken pipe
                close_thread(client)
                quit_game(name, client)
                break
            elif code == "PASS":
                # disable_cur
                # enable next
                pass
            elif code == "WORD":
                if is_new(str(word)):  # new word
                    index = enable_next(name)
                    str_to_send = "WORD_OK-"+""+"-"+str(len(clients))
                    print("str_to_send: " + str_to_send)
                    client.send(str.encode(str_to_send))
                    broadcast(word, client, index, name + " : ")
                else:
                    str_to_send = "WORD_EXIST-" + "" + "-" + str(len(clients))
                    print("str_to_send: " + str_to_send)
                    client.send(str.encode(str_to_send))

                print(name + ": " + word)
                print(wordlist)

        except OSError:
            print("Exception caught")
            break


def broadcast(msg, cur_client, next_client=-1, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    print("******inside broadcast")
    print(msg)
    print("clients count: %d" % len(clients))
    for sockid in clients:
        if sockid == cur_client:
            continue

        # print(sockid)
        # print("next index: %d" % next_client)

        if next_client < 0:  # join or quit msg broadcast
            st = ""
        elif clients.index(sockid) == next_client:
            st = tkinter.NORMAL
        elif next_client >= 0:
            st = tkinter.DISABLED

        str_to_send = "BROADCAST-" + st + "-" + str(len(clients)) + "-" + str(prefix + msg)
        print("str_to_send: " + str_to_send)
        sockid.send(str.encode(str_to_send))
    print("******leaving broadcast")


def enable_next(curname):
    print("======inside enable_next, name: "+curname)
    index = namelist.index(curname)
    # print("index: %d" % index)

    if index != len(namelist) - 1:
        index = index + 1
    else:
        index = 0

    print("next index: %d" % index)
    print("======leaving enable_next")
    return index


HOST = ''
PORT = 34000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    try:
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except OSError:
        pass
