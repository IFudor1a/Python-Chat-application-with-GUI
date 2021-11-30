import tkinter
import tkinter.scrolledtext
from tkinter import *


def write():
    pass


class Interface:
    def gui(self):
        window = Tk()
        window.title("Messenger")
        window.geometry("1080x600")

        chat_label = tkinter.Label(window, text="Chat:")
        chat_label.config(font=("Arial", 12))
        chat_label.pack(padx=20, pady=5)

        text_area = tkinter.scrolledtext.ScrolledText(window)
        text_area.pack(padx=20, pady=5)
        text_area.config(state="disabled")

        msg_label = tkinter.Label(window, text="Input:")
        msg_label.config(font=("Arial", 12))
        msg_label.pack(padx=20, pady=5)

        input_area = tkinter.Text(window, height=3)
        input_area.pack(padx=20, pady=5)

        send_button = tkinter.Button(window, text="Send", command= write)
        send_button.config(font=("Arial", 12))
        window.mainloop()


Interface.gui("")