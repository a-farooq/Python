#!/usr/bin/env python3
"""Script for Tkinter GUI game client."""
# from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread
import tkinter
#import enchant

copyright = "Developed By - Aamil Farooq"
#dic = enchant.Dict("en_US")
welcome = ""
name = ""


def set_score():
    score = int(lblscore.cget('text')) + 1
    lblscore.config(text=str(score))


def show_error(error):
    print(error)


def is_valid(word):
    word.split()
    print("inside is_valid")
    err_english = word + " is not an english word"
    err_empty = "Input a word"

    if not word:
        show_error(err_empty)
        msg_list.insert(tkinter.END, err_empty)
        msg_list.itemconfig(tkinter.END, foreground="red")
        msg_list.yview(tkinter.END)
        return False

    #if not dic.check(word):
    #    show_error(err_english)
    #    msg_list.insert(tkinter.END, err_english)
    #    msg_list.itemconfig(tkinter.END, foreground="red")
    #    msg_list.yview(tkinter.END)
    #    return False

    return True


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg, st, count = [str(i) for i in client_socket.recv(BUFSIZ).decode('utf-8').split('\n')]
            if msg == "WORD_OK":
                set_score()
                msg_list.insert(tkinter.END, name + ": " + my_msg.get())
            elif msg == "WORD_EXIST":
                error = my_msg.get() + " already entered. Input a new word."
                msg_list.insert(tkinter.END, error)
                msg_list.itemconfig(tkinter.END, foreground="red")
            elif msg == "WELCOME":
                greet = "Greetings! Type your name and press enter!"
                txtbox.focus_set()
                msg_list.insert(tkinter.END, greet)
                msg_list.itemconfig(tkinter.END, foreground="blue")
            else:
                msg_list.insert(tkinter.END, msg)

            print(msg + ": " + my_msg.get())
            msg_list.yview(tkinter.END)
            my_msg.set("")
            lblonline.config(text=count+" Live")

            if st != "":
                txtbox.config(state=st)
                btnsend.config(state=st)
        except OSError:  # Possibly client has left the game.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    global welcome
    global name
    word = my_msg.get()
    # my_msg.set("")  # Clears input field.

    # client_socket.send(bytes(msg, "utf8"))
    # client_socket.send(bytes(tkinter.NORMAL, "utf8"))

    if welcome == "":
        print("if: " + word)
        s1 = "Welcome " + word + "!"
        s2 = "Enter english word starting with the last letter of previous word."
        welcome = s1 + '\n' + s2
        name = word
        client_socket.send(str.encode(str(word)))

        #msg, st, count = [str(i) for i in client_socket.recv(BUFSIZ).decode('utf-8').split('\n')]
        #if msg != "UNAME_OK":
        #    msg = "The username \"" + name + "\" is taken. Try another name."
        #    print(msg)
        #    msg_list.insert(tkinter.END, msg)
        #    msg_list.itemconfig(tkinter.END, foreground="red")
        #    msg_list.yview(tkinter.END)
        #    return

        #print(welcome)
        #lblonline.config(text=count + " Live")

        msg_list.insert(tkinter.END, s1)
        msg_list.itemconfig(tkinter.END, fg="green")
        msg_list.insert(tkinter.END, s2)
        msg_list.itemconfig(tkinter.END, fg="blue")
        msg_list.yview(tkinter.END)
        my_msg.set("")
    else:
        print("else: " + word)
        if is_valid(word):
            print("Sending the word " + word)
            client_socket.send(str.encode(str(word)))
        else:
            pass


def _quit():  # event is passed by binders.
    """Handles sending of messages."""
    client_socket.send(str.encode(str("quitt")))
    client_socket.close()
    top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    _quit()


top = tkinter.Tk()
w = 450
h = 350

ws = top.winfo_screenwidth()
hs = top.winfo_screenheight()

x = (ws / 2) - w / 2
y = (hs / 2) - h / 2

top.geometry("%dx%d+%d+%d" % (w, h, x, y))

top.title("Word Chain Game v2.0")

row = tkinter.Frame(top)
lblonline = tkinter.Label(row, text='', fg='blue', width=40, justify=tkinter.RIGHT)
row.pack(pady=5)
lblonline.pack()

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=12, width=45, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack(pady=5)

row = tkinter.Frame(top)
txtbox = tkinter.Entry(row, textvariable=my_msg, width=15, bg='yellow')
txtbox.bind("<Return>", send)
btnsend = tkinter.Button(row, text="OK", width=5, command=send)
btnpass = tkinter.Button(row, text="Pass", width=5)
lblscore = tkinter.Label(row, text='0', width=3)
# btnsend.pack(side=tkinter.LEFT)
row.pack(pady=5)
txtbox.pack(side=tkinter.LEFT)
lblscore.pack(side=tkinter.RIGHT)
btnpass.pack(side=tkinter.RIGHT)
btnsend.pack(side=tkinter.RIGHT)
# btnsend.place(relx=0.8, rely=0.8, anchor=tkinter.CENTER)

row = tkinter.Frame(top)
btnquit = tkinter.Button(row, text="Quit", width=5, command=_quit)
row.pack(pady=5)
btnquit.pack(side=tkinter.RIGHT)

row = tkinter.Frame(top)
cpy_label = tkinter.Label(row, text=copyright, fg='blue', width=40, justify=tkinter.CENTER)
row.pack(pady=5)
cpy_label.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


# ----Now comes the sockets part----
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# HOST = input('Enter host: ')
#HOST = '172.16.120.180'
HOST = '127.0.0.1'
#HOST = socket.gethostbyname('BANL1648dc7d3.local')
#HOST = socket.gethostname()
#print(HOST)
#print(socket.gethostbyname(HOST))
#PORT = input('Enter port: ')
#if not PORT:
#    PORT = 34000
#else:
#    PORT = int(PORT)
PORT = 34000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.