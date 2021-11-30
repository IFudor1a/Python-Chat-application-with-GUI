import socket
import threading
import tkinter
from tkinter import *
from tkinter import scrolledtext

from database import Database


def check():
    return True


class Client:
    def __init__(self):
        self.gui_done = False
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.user.connect(('127.0.0.1', 1234))
        self.user.sendall(self.nickname.encode('utf-8'))

    def top(self, database):
        self.top = Toplevel()
        self.top.title("Registration")
        self.top.geometry("1080x800")

        self.username_label = Label(self.top, text="username", bg="white")
        self.username_label.pack(padx=20,pady=10)
        self.username = Entry(self.top)
        self.username.config(font=("Arial", 12))
        self.username.pack(padx=20, pady=10)

        self.password_label = Label(self.top, text="password", bg="white")
        self.password_label.pack(padx=20,pady=10)
        self.password = Entry(self.top)
        self.password.config(font=("Arial", 12))
        self.password.pack(padx=20, pady=10)

        self.button = Button(self.top, text="Send", command=lambda: self.control(database))
        self.button.config(font=("Arial", 12))
        self.button.pack(padx=20, pady=5)



    def control(self, db):
        self.nickname = "{}".format(self.username.get())
        password = "{}".format(self.password.get())
        print("Done")
        db.cursor.execute(f"SELECT username FROM clients WHERE username = '{self.nickname}'")
        founds = db.cursor.fetchone()
        if founds is None:
            db.cursor.execute(f"INSERT INTO clients VALUES ('{self.nickname}','{password}');")
            db.conn.commit()
            self.connect()
        else:
            self.top.title("Log in")
            for i in range(3):
                password = f"{self.password.get()}"
                db.cursor.execute(f"SELECT password FROM clients WHERE username = '{self.nickname}'")
                founds = db.cursor.fetchone()
                if password == founds[0]:
                    db.cursor.execute(f"SELECT * FROM messages WHERE receiver = 'all'")
                    result = db.cursor.fetchall()
                    if result is None:
                        print("None Messages Yet")
                    else:
                        for i in result:
                            message_id, name, receiver, message, time = i
                            message = f"[{time}]{name}: {message}"
                            self.text_area.config(state='normal')
                            self.text_area.insert(tkinter.END, message)
                            self.text_area.yview(tkinter.END)
                            self.text_area.config(state='disabled')
                    db.cursor.execute(f"SELECT * FROM messages WHERE receiver = '{self.nickname}'")
                    result = db.cursor.fetchall()
                    if result is None:
                        print("None Messages Yet")
                    else:
                        for i in result:
                            message_id, name, receiver, message, time = i
                            message = f"<PRIVATE>[{time}]{name}: {message}"
                            self.text_area.config(state='normal')
                            self.text_area.insert(tkinter.END, message)
                            self.text_area.yview(tkinter.END)
                            self.text_area.config(state='disabled')
                    self.connect()
                    self.top.destroy()
                    break

    def gui(self):
        # window
        self.window = Tk()
        self.window.title("Messenger")
        self.window.geometry("1080x800")
        self.window.configure(bg="white")

        # output part
        self.output_label = Label(self.window, text="Chat", bg="white")
        self.output_label.config(font=("Arial", 12))
        self.output_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.window, font=("Arial", 12))
        self.text_area.pack(padx=20, pady=10)
        self.text_area.configure(state="disabled")

        # input part
        self.input_label = Label(self.window, text="Input", bg="white")
        self.input_label.config(font=("Arial", 12))
        self.input_label.pack(padx=20, pady=5)

        self.input_text = Text(self.window, height=3)
        self.input_text.config(font=("Arial", 12))
        self.input_text.pack(padx=20, pady=5)

        self.button = Button(self.window, text="Send", command=self.write)
        self.button.config(font=("Arial", 12))
        self.button.pack(padx=20, pady=5)

        self.gui_done = True

        self.window.mainloop()

    def write(self):
        receive_thread = threading.Thread(target=client.receive)
        receive_thread.start()
        message = '{}'.format(self.input_text.get('1.0', tkinter.END))
        self.user.send(message.encode('utf-8'))
        self.input_text.delete('1.0', tkinter.END)

    def receive(self):
        while self.gui_done:
            try:
                message = self.user.recv(2048)
                message = message.decode('utf-8')
                if message is None:
                    break
                self.text_area.config(state='normal')
                self.text_area.insert(tkinter.END, message)
                self.text_area.yview(tkinter.END)
                self.text_area.config(state='disabled')
            except:
                print("Disconnected from the server!")
                self.user.close()
                break


if __name__ == "__main__":
    database = Database()
    database.connect()
    client = Client()
    client.top(database)
    client.gui()
