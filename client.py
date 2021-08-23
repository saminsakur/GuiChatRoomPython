import socket
import threading
from tkinter import Tk, simpledialog, Label, Text, Button
from tkinter.scrolledtext import *

HOST = "127.0.0.1"
PORT = 5050
ADDRESS = (HOST, PORT)
ENCODING = "utf-8"
HEADER = 1024


class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDRESS)

        dlg = Tk()
        dlg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=dlg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recv_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        recv_thread.start()

    def gui_loop(self):
        self.window = Tk()
        self.window.configure(bg="lightgray")

        self.chat_label = Label(self.window, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.textarea = ScrolledText(self.window)
        self.textarea.pack(padx=20, pady=5)
        self.textarea.config(state="disabled")

        self.msg_label = Label(self.window, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_ctrl = Text(self.window, height=3)
        self.input_ctrl.pack(padx=20, pady=5)

        self.send_butn = Button(self.window, text="Send", command=self.write)
        self.send_butn.config(font=("Arial", 12))
        self.send_butn.pack(padx=20, pady=5)

        self.gui_done = True

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_ctrl.get('1.0', 'end')}"
        self.sock.send(message.encode(ENCODING))
        self.input_ctrl.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(HEADER).decode(ENCODING)
                if message == "!NICK":
                    self.sock.send(self.nickname.encode(HEADER))
                else:
                    if self.gui_done:
                        self.textarea.config (state='normal')
                        self.textarea.insert ('end', message)
                        self.textarea.yview ('end')
                        self.textarea.config (state='disabled')

            except ConnectionAbortedError:
                break
            except:
                self.sock.close()
                print("Error!")
                break


if __name__ == "__main__":
   client = Client(HOST, PORT)