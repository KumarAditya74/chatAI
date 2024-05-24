import tkinter as tk
from tkinter import scrolledtext
from groq import Groq

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat.ai Assistant")

        self.client = Groq(api_key='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')

        self.main_container_bg = tk.Canvas(master, bg="grey", bd=0, highlightthickness=0)
        self.main_container_bg.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        self.main_container_bg.create_rectangle(0, 0, 800, 600, fill="grey", outline="")
        self.main_container_bg.create_text(400, 100, text="Welcome to Chat.ai Assistant!", font=("Helvetica", 18), fill="white")
        self.main_container_bg.create_text(400, 140, text="Start chatting below:", font=("Helvetica", 12), fill="white")

        self.chat_container = tk.Canvas(master, bg="black", bd=0, highlightthickness=0)
        self.chat_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.7)
        self.chat_container.create_rectangle(0, 0, 800, 400, fill="black", outline="", stipple="gray50")

        self.messages = scrolledtext.ScrolledText(self.chat_container, wrap=tk.WORD, width=60, height=20, bg="black", fg="white")
        self.messages.place(relx=0.5, rely=0.4, anchor=tk.CENTER, relwidth=0.95, relheight=0.75)
        self.messages.configure(state="disabled")
        self.messages.config(yscrollcommand=self.set_scrollbar_color)

        self.input_field = tk.Entry(self.chat_container, width=50,  bg="black", fg="white", insertbackground="white")
        self.input_field.place(relx=0.5, rely=0.85, anchor=tk.CENTER, relwidth=0.7)
        self.input_field.focus()

        self.send_button = tk.Button(self.chat_container, text="Send", command=self.send_message, bg="grey", fg="white", relief=tk.FLAT, cursor="hand2" ,width=15, height = 1)
        self.send_button.place(relx=0.5, rely=0.92, anchor=tk.CENTER)
        self.send_button.bind("<Enter>", self.on_enter)
        self.send_button.bind("<Leave>", self.on_leave)

        self.messages_list = [
            {
                "role": "assistant",
                "content": "Welcome to chat.ai Assistant! Start chatting below:\n"
            }
        ]

        self.display_message("Assistant: Welcome to chat.ai Assistant! Start chatting below\n")

    def send_message(self):
        user_input = self.input_field.get()
        if user_input:
            self.display_message("You: " + user_input + "\n", disable=True)
            self.messages_list.append({"role": "user", "content": user_input})
            response = self.get_response()
            self.messages_list.append({"role": "assistant", "content": response})
            self.display_message("Assistant: " + response + "\n")
            self.input_field.delete(0, tk.END)

    def get_response(self):
        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=self.messages_list,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
        return response

    def display_message(self, message, disable=False):
        self.messages.configure(state="normal")
        self.messages.insert(tk.END, message)
        self.messages.configure(state="disabled")
        self.messages.see(tk.END)

    def set_scrollbar_color(self, *args):
        self.messages.yview(*args)
        self.messages.config(yscrollcommand=lambda *args: self.messages.yview_moveto(args[0]))
        self.messages.config(yscrollcommand=lambda *args: self.messages.yview_moveto(args[0]))
        self.messages.config(yscrollcommand=lambda *args: self.messages.yview_moveto(args[0]))
        self.messages.config(yscrollcommand=lambda *args: self.messages.yview_moveto(args[0]))
        self.messages.config(yscrollcommand=lambda *args: self.messages.yview_moveto(args[0]))

    def on_enter(self, event):
        self.send_button.config(bg="darkgrey")

    def on_leave(self, event):
        self.send_button.config(bg="grey")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = ChatApp(root)
    root.mainloop()
