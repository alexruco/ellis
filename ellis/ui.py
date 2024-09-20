import tkinter as tk
from tkinter import messagebox
from create_conversation import create_conversation

def submit():
    user_email = user_email_entry.get()
    system_email = system_email_entry.get()
    model_email = model_email_entry.get()
    description = description_entry.get("1.0", tk.END)
    conv_key, created_at = create_conversation(user_email, system_email, model_email, description)
    messagebox.showinfo("Success", f"Conversation created with key: {conv_key} at {created_at}")

root = tk.Tk()
root.title("Create Conversation")

tk.Label(root, text="User Email").grid(row=0)
tk.Label(root, text="System Email").grid(row=1)
tk.Label(root, text="Model Email").grid(row=2)
tk.Label(root, text="Description").grid(row=3)

user_email_entry = tk.Entry(root)
system_email_entry = tk.Entry(root)
model_email_entry = tk.Entry(root)
description_entry = tk.Text(root, height=4, width=30)

user_email_entry.grid(row=0, column=1)
system_email_entry.grid(row=1, column=1)
model_email_entry.grid(row=2, column=1)
description_entry.grid(row=3, column=1)

tk.Button(root, text='Submit', command=submit).grid(row=4, column=1, pady=4)

root.mainloop()
