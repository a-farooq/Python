#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) game application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import enchant
import tkinter


wordlist = []
namelist = []
clients = []
addresses = {}
dic = enchant.Dict("en_US")


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
        welcome = "WELCOME"
        client_sockid.sendall(str.encode("\n".join([str(welcome), str(tkinter.NORMAL), str(len(clients))])))

        #client_sockid.send(bytes(welcome, "utf8"))
        #client_sockid.send(bytes(tkinter.NORMAL, "utf8"))
        # addresses[client_sockid] = client_address
        Thread(target=handle_client, args=(client_sockid,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Thread - Handles a single client connection."""

    name = ""
    while True:
        name = client.recv(BUFSIZ).decode("utf8")
        if name == "quitt":
            close_thread(client)
            return

        if len(namelist) > 0 and name in namelist:  # checking duplicate username
            # msg = "The username \"" + name + "\" is taken. Try another name."
            msg = "UNAME_FAIL"
            print(msg)
            client.sendall(str.encode("\n".join([str(msg), str(tkinter.NORMAL), str(len(clients))])))
        else:
            msg = "UNAME_OK"
            print(msg)
            client.sendall(str.encode("\n".join([str(msg), str(tkinter.DISABLED), str(len(clients))])))
            namelist.append(name)
            break

    #name, st = [str(i) for i in client.recv(1024).decode('utf-8').split('\n')]
    #print('name: %s' % name)


    #welcome = 'Welcome %s!' % name
    #client.send(bytes(welcome, "utf8"))
    #client.sendall(str.encode("\n".join([str(welcome), str(tkinter.NORMAL)])))
    msg = "%s has joined the game!" % name
    print(msg)
    #broadcast(bytes(msg, "utf8"))
    broadcast(msg, client)

    while True:
        try:
            # print("Thread waiting for word from "+name)
            word = client.recv(BUFSIZ).decode('utf-8')
            print("#####"+word)
            #word, st = [str(i) for i in client.recv(1024).decode('utf-8').split('\n')]
            #if word != bytes("quit", "utf8"):
            if word != "quitt":
                if is_new(str(word)):  # new word
                    index = enable_next(name)
                    msg = "WORD_OK"
                    print(msg + ": " + word)
                    client.sendall(str.encode("\n".join([str(msg), "", str(len(clients))])))
                    broadcast(word, client, index, name + ": ")
                else:
                    msg = "WORD_EXIST"
                    print(msg + ": " + word)
                    client.sendall(str.encode("\n".join([str(msg), "", str(len(clients))])))

                print(name + ": " + word)
                # print(wordlist)
            else:  # client closed
                # client.send(bytes("quit", "utf8")) #broken pipe
                close_thread(client)
                quit_game(name, client)
                break
        except OSError:
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
        # sockid.send(bytes(prefix, "utf8") + msg)

        if next_client < 0:  # join or quit msg broadcast
            sockid.sendall(str.encode("\n".join([str(prefix + msg), "", str(len(clients))])))
        elif clients.index(sockid) == next_client:
            sockid.sendall(str.encode("\n".join([str(prefix + msg), str(tkinter.NORMAL), str(len(clients))])))
        elif next_client >= 0:
            sockid.sendall(str.encode("\n".join([str(prefix + msg), str(tkinter.DISABLED), str(len(clients))])))
    print("******leaving broadcast")


def enable_next(name):
    print("======inside enable_next, name: "+name)
    index = namelist.index(name)
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
SERVER.settimeout(60)
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
        print("Exception caught")
        pass
