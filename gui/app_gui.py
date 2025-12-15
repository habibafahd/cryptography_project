import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class ChatApp:
    def __init__(self, send_func, decrypt_func):
        self.send_func = send_func
        self.decrypt_func = decrypt_func
        self.disconnect_func = None  

        self.root = tk.Tk()
        self.root.title("Secure Chat")
        self.root.configure(bg="#ececec") 

        self.chat_frame = tk.Frame(self.root, bg="#d9d9d9", bd=2, relief=tk.RIDGE)
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, state='disabled',
            width=55, height=22, font=("Arial", 12), bg="#ffffff", fg="#000000",
            bd=0, padx=5, pady=5
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.root, bg="#ececec")
        self.entry_frame.pack(padx=10, pady=(0,10), fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
        self.entry.pack(side=tk.LEFT, padx=(0,5), fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.entry_frame, text="Send", command=self.send_message,
            bg="#FF1EA5", fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=5
        )
        self.send_button.pack(side=tk.LEFT)

        self.end_button = tk.Button(
            self.entry_frame, text="End Chat", command=self.end_chat,
            bg="#8F32CD", fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=5
        )
        self.end_button.pack(side=tk.LEFT, padx=(5,0))

        self.chat_area.tag_config("you", foreground="#FF1EA5")
        self.chat_area.tag_config("peer", foreground="#8F32CD")
        self.chat_area.tag_config("system", foreground="#888888", font=("Arial", 10, "italic"))

    def set_disconnect_callback(self, func):
        self.disconnect_func = func

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            self.entry.delete(0, tk.END)
            ciphertext = self.send_func(msg.encode())
            timestamp = datetime.now().strftime("%H:%M")
            self.append_message(f"[{timestamp}] You: {msg}", tag="you")
            self.entry.focus_set()
            return ciphertext
        return None

    def append_message(self, msg, tag=None):
        self.chat_area.configure(state='normal')
        if tag:
            self.chat_area.insert(tk.END, msg + "\n", tag)
        else:
            self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)

    def receive_message(self, ciphertext):
        plaintext = self.decrypt_func(ciphertext)
        timestamp = datetime.now().strftime("%H:%M")
        self.append_message(f"[{timestamp}] Peer: {plaintext.decode()}", tag="peer")
        self.entry.focus_set()

    def end_chat(self):
        if self.disconnect_func:
            self.disconnect_func()
            self.append_message("Chat ended by user.", tag="system")
            self.send_button.config(state="disabled")
            self.end_button.config(state="disabled")
            self.entry.config(state="disabled")

    def run(self):
        self.entry.focus_set()
        self.root.mainloop()
