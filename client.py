import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import *


HOST = "127.0.0.1"
PORT = 9090
ENCODING = "utf-8"

class Client:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

        msg = Tk()
        msg.withdraw()

        self.nickname = askstring("Nickname", "Please choose a nickname", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = Tk()
        self.win.config(bg="lightgray")

        self.ChatLabel = Label(self.win, text="Chat", bg="lightgray")
        self.ChatLabel.config(font=("Arial", 12))
        self.ChatLabel.pack(padx=20, pady=5)

        self.TextArea = ScrolledText(self.win)
        self.TextArea.pack(padx=20, pady=5)
        self.TextArea.config(state="disabled")

        self.MsgLabel = Label(self.win, text="Message", bg="lightgray")
        self.MsgLabel.config(font=("Arial", 12))
        self.MsgLabel.pack(padx=20, pady=5)

        self.InputArea = Text(self.win, height=3)
        self.InputArea.pack(padx=20, pady=5)

        self.SendButn = Button(self.win, text="Send", command=self.write)
        self.SendButn.config(font=("Arial", 12))
        self.SendButn.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.InputArea.get('1.0', 'end')}"
        self.sock.send(message.encode(ENCODING))
        self.InputArea.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == "NICK":
                    self.sock.send(self.nickname.encode(ENCODING))
                else:
                    if self.gui_done:
                        self.TextArea.config(state="normal")
                        self.TextArea.insert("end", message)
                        self.TextArea.yview("end")
                        self.TextArea.config(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print()
                self.sock.close()
                break

client = Client(HOST, PORT)