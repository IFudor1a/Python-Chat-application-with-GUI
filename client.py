import socket, threading
import tkinter

from database import Database
from tkinter import *
from tkinter import scrolledtext


class Client:
    def __init__(self):
        self.window = Tk()
        self.chat_label = tkinter.Label(self.window, text="Chat:",bg="white")
        self.text_area = scrolledtext.ScrolledText(self.window)
        self.msg_label = tkinter.Label(self.window,text="Message:", bg="white")
        self.input_area = tkinter.Text(self.window, height =3)
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gui_thread = threading.Thread(target=self.gui)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()


    def connect(self):
        self.user.connect(('127.0.0.1', 1234))
        self.user.sendall(username.encode('utf-8'))
        self.window.configure(bg="lightgray")

    def gui(self):
        self.window.title("Messenger")
        self.window.geometry("1080x600")

        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,pady=5)

        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state="disabled")

        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area.pack(padx=20,pady=5)

        self.send_button = tkinter.Button(self.window,text="Send",command=self.write)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20,pady=5)



        self.window.mainloop()


    def receive(self):
        while True:
            try:
                message = self.user.recv(2048)
                message = message.decode('utf-8')
                if message is None:
                    break
                self.text_area.config(state='normal')
                self.text_area.insert('end', message)
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
            except:
                print("Disconnected from the server!")
                self.user.close()
                break

    def write(self):
            message = '{}'.format(self.input_area.get('1.0','end'))
            self.user.send(message.encode('utf-8'))
            self.input_area.delete('1.0','end')


if __name__ == "__main__":
    database = Database()
    database.connect()
    print("TO CHANGE FROM PUBLIC TO PRIVATE PLEASE ENTER IN CHAT [PRIVATE] TO NICKNAME MESSAGE")
    username = input("Enter username: ")
    def control(self):
        database.cursor.execute(f"SELECT username FROM clients   WHERE username = '{username}'")
        founds = database.cursor.fetchone()
        if founds is None:
            print("Registration")
            password = input("Enter password:")
            database.cursor.execute(f"INSERT INTO clients VALUES ('{username}','{password}');")
            database.conn.commit()
            self.connect()
        else:
            print("Log in")
            for i in range(3):
                password = input("Enter your password:")
                database.cursor.execute(f"SELECT password FROM clients WHERE username = '{username}'")
                founds = database.cursor.fetchone()
                if password == founds[0]:
                    print("You log in ")
                    database.cursor.execute(f"SELECT * FROM messages WHERE receiver = 'all'")
                    result = database.cursor.fetchall()
                    if result is None:
                        print("None Messages Yet")
                    else:
                        for i in result:
                            message_id, name, receiver, message, time = i
                            print(f"[{time}]{name}: {message}")
                    database.cursor.execute(f"SELECT * FROM messages WHERE receiver = '{username}'")
                    result = database.cursor.fetchall()
                    if result is None:
                        print("None Messages Yet")
                    else:
                        for i in result:
                            message_id, name, receiver, message, time = i
                            print(f"<PRIVATE>[{time}]{name}: {message}")
                    client.connect()
                    break
    client = Client()
    client.write()
