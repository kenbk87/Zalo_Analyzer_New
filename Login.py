import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from main import Window

import pyrebase

root = Tk()

# width and height
w = 450
h = 525
# background color
bgcolor = "#bdc3c7"

firebaseConfig = {
  'apiKey': "AIzaSyAgcyXvddrP67teA992IBingaGOeIMRfYE",
  'authDomain': "zalo-project-4e2f9.firebaseapp.com",
  'projectId': "zalo-project-4e2f9",
  'storageBucket': "zalo-project-4e2f9.appspot.com",
  'messagingSenderId': "268796536576",
  'appId': "1:268796536576:web:b363cafd8efb1e792cf5e5",
  'measurementId': "G-W51H0E31D0",
  'databaseURL': ''}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# ----------- CENTER FORM ------------- #
root.overrideredirect(1)  # remove border
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws - w) / 2
y = (hs - h) / 2
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# ----------- HEADER ------------- #

headerframe = tk.Frame(root, bg='#95a5a6', width=w, height=70)
titleframe = tk.Frame(headerframe, bg='yellow', padx=1, pady=1)
title_label = tk.Label(titleframe, text='Register', padx=20, pady=5, bg='green',
                       fg='#fff', font=('Times New Roman', 24), width=8)
close_button = tk.Button(headerframe, text='X', font=('Times New Roman', 12))

headerframe.pack()
titleframe.pack()
title_label.pack()
close_button.pack()

titleframe.place(y=26, relx=0.5, anchor=CENTER)
close_button.place(x=410, y=10)


# close window
def close_win():
    root.destroy()


close_button['command'] = close_win

# ----------- END HEADER ------------- #

mainframe = tk.Frame(root, width=w, height=h)

# ----------- Login Page ------------- #
loginframe = tk.Frame(mainframe, width=w, height=h)
login_contentframe = tk.Frame(loginframe, padx=30, pady=100, bg=bgcolor)

username_label = tk.Label(login_contentframe, text='Username:',
                          font=('Times New Roman', 14), bg=bgcolor)
password_label = tk.Label(login_contentframe, text='Password:',
                          font=('Times New Roman', 14), bg=bgcolor)

username_entry = tk.Entry(login_contentframe, font=('Times New Roman', 12), width=30)
password_entry = tk.Entry(login_contentframe, font=('Times New Roman', 12), width=30, show='*')

login_button = tk.Button(login_contentframe, text="Login", font=('Times New Roman', 16),
                         bg='#2980b9', fg='#fff', padx=25, pady=10, width=25)

go_register_label = tk.Label(login_contentframe,
                             text=">> don't have an account? create one",
                             font=('Times New Roman', 12), bg=bgcolor, fg='red')

mainframe.pack(fill='both', expand=1)
loginframe.pack(fill='both', expand=1)
login_contentframe.pack(fill='both', expand=1)

username_label.grid(row=0, column=0, pady=10)
username_entry.grid(row=0, column=1)

password_label.grid(row=1, column=0, pady=10)
password_entry.grid(row=1, column=1)

login_button.grid(row=2, column=0, columnspan=2, pady=40)

go_register_label.grid(row=3, column=0, columnspan=2, pady=20)


# create a function to display the register frame
def go_to_register():
    loginframe.forget()
    registerframe.pack(fill="both", expand=1)
    title_label['text'] = 'Register'
    title_label['bg'] = '#27ae60'


go_register_label.bind("<Button-1>", lambda page: go_to_register())


def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    try:
        login = auth.sign_in_with_email_and_password(username, password)
        Window()
        root.withdraw()  # hide the root
    except Exception as e:
        messagebox.showinfo('Error', 'Invalid Email or Password')
        print(e)


login_button['command'] = login

# ----------- Register Page ------------- #

registerframe = tk.Frame(mainframe, width=w, height=h)
register_contentframe = tk.Frame(registerframe, padx=15, pady=15, bg=bgcolor)

username_label_rg = tk.Label(register_contentframe, text='Email:',
                             font=('Times New Roman', 14), bg=bgcolor)
password_label_rg = tk.Label(register_contentframe, text='Password:',
                             font=('Times New Roman', 14), bg=bgcolor)
confirmpass_label_rg = tk.Label(register_contentframe, text='Re-Password:',
                                font=('Times New Roman', 14), bg=bgcolor)

username_entry_rg = tk.Entry(register_contentframe, font=('Times New Roman', 12), width=30)
password_entry_rg = tk.Entry(register_contentframe, font=('Times New Roman', 12), width=30,
                             show='*')
confirmpass_entry_rg = tk.Entry(register_contentframe, font=('Times New Roman', 12), width=30,
                                show='*')

selectimage_frame = tk.Frame(register_contentframe, bg=bgcolor)
register_button = tk.Button(register_contentframe, text="Register", font=('Times New Roman', 14),
                            bg='#2980b9', fg='#fff', padx=25, pady=10, width=30)

go_login_label = tk.Label(register_contentframe,
                          text=">> already have an account? sign in",
                          font=('Verdana', 10), bg=bgcolor, fg='red')

register_contentframe.pack(fill='both', expand=1)

username_label_rg.grid(row=1, column=0, pady=5, sticky='e')
username_entry_rg.grid(row=1, column=1)

password_label_rg.grid(row=2, column=0, pady=5, sticky='e')
password_entry_rg.grid(row=2, column=1)

confirmpass_label_rg.grid(row=3, column=0, pady=5, sticky='e')
confirmpass_entry_rg.grid(row=3, column=1)

register_button.grid(row=7, column=0, columnspan=2, pady=20)
go_login_label.grid(row=8, column=0, columnspan=2, pady=10)


# create a function to display the login frame
def go_to_login():
    registerframe.forget()
    loginframe.pack(fill="both", expand=1)
    title_label['text'] = 'Login'
    title_label['bg'] = '#2980b9'


go_login_label.bind("<Button-1>", lambda page: go_to_login())


def register():
    username = username_entry_rg.get().strip()
    password = password_entry_rg.get().strip()
    confirm_password = confirmpass_entry_rg.get().strip()

    if len(username) > 0 and len(password) > 0:
        if password == confirm_password:
            try:
                user = auth.create_user_with_email_and_password(username, password)
                messagebox.showwarning('Successfully!', 'User has already registed successfully!')
            except Exception as e:
                print(e)
                messagebox.showwarning('Error', 'User has already exist')
        else:
            messagebox.showwarning('Error', 'Password does not match!')
    else:
        messagebox.showwarning('Empty Fields', 'make sure to enter all the information')


register_button['command'] = register

root.mainloop()
