from customtkinter import *
from tkinter import messagebox
import sqlite3


root = CTk()

root.title("Library Management System")
root.wm_state("zoomed")
set_appearance_mode('dark')
root.geometry(f"{1920}x{1080}")
root.iconbitmap(r'Icon.ico')

# Creating Directory for database
path=os.environ["userprofile"]
try:
    os.mkdir(path+"\\Documents\\Library Database")
except FileExistsError:
    pass

con = sqlite3.connect(path+"\\Documents\\Library Database\mydatabase.db")
cur = con.cursor()

#Creating Tables
con.execute("""CREATE TABLE IF NOT EXISTS empdetail
            (empid varchar(20) PRIMARY KEY,
            name varchar(30), 
            password varchar(30));""")
con.execute("""CREATE TABLE IF NOT EXISTS studetail 
            (stuid varchar(20) PRIMARY KEY, 
            name varchar(30), 
            password varchar(30)),
            email varchar(60);""")
con.execute("""CREATE TABLE IF NOT EXISTS books 
            (bid varchar(20) PRIMARY KEY, 
            title varchar(30), 
            subject varchar(30), 
            author varchar(30), 
            status varchar(30) NOT NULL DEFAULT 'Available');""")
con.execute("""CREATE TABLE IF NOT EXISTS issuedetail 
            (bid varchar(20),
            stuid varchar(20),
            PRIMARY KEY (bid, stuid),
            FOREIGN KEY (bid) REFERENCES books(bid),
            FOREIGN KEY (stuid) REFERENCES studetail(stuid);""")


##############    MAIN  SCREEN    #############
def main_win():
    global button_student, button_admin, main_frame
    button_student = CTkButton(master=root,text='Student',border_width=5,corner_radius=15,border_color='#3333ff',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=student_button_click_register)
    button_student.place(relx=0.07,rely=0.3, relwidth=0.1, relheight=0.41)

    main_frame = CTkFrame(root, border_width=5,corner_radius=8,)
    main_frame.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.8)

    button_admin = CTkButton(master=root,text='Admin',border_width=5,corner_radius=15,border_color='#ff0000',
        fg_color='#ff3737', hover_color='#d20000',font=('Roboto',22,),command=admin_button_click_login)
    button_admin.place(relx=0.83,rely=0.3, relwidth=0.1, relheight=0.41)


def toplevel_message():
    global toplevel_messages

    try:
        toplevel_messages.destroy()
    except:
        pass

    toplevel_messages = CTkToplevel()
    toplevel_messages.title('Message')
    toplevel_messages.geometry(f"{350}x{180}")
    toplevel_messages.minsize(350,180)
    toplevel_messages.maxsize(350,180)

    label_message = CTkLabel(master=toplevel_messages,text='message',font=('Roboto',18,))
    label_message.grid(row=0,column=0,columnspan=2,padx=20,pady=(20,5),sticky='s')

    button_ok = CTkButton(master=toplevel_messages,text='Okay',border_width=3,corner_radius=15,
        border_color='#3f60fc',)
    button_ok.grid(row=1,column=0,padx=(20,10),pady=10)

    button_tryagain = CTkButton(master=toplevel_messages,text='Try Again',border_width=3,corner_radius=15,
        border_color='#3f60fc',)
    button_tryagain.grid(row=1,column=1,padx=(10,20),pady=10)


def student_button_click_login():
    button_admin.place(rely=0.3, relheight=0.41)
    button_student.place(rely=0.2, relheight=0.61)

    # Remove all the widgets from the main_frame
    try:
        for widget in main_frame.winfo_children():
            widget.destroy()
    except:
        pass

    # Login Frame
    label_login = CTkLabel(master=main_frame,text='Login',font=('Roboto',22,))
    label_login.place(relx=0.7, rely=0.05)

    frame_login = CTkFrame(master=main_frame,border_width=4,border_color='#3f60fc')
    frame_login.place(relx=0.52, rely=0.12, relwidth=0.46, relheight=0.84)

    label_username = CTkLabel(master=frame_login,text='Enter Username',font=('Roboto',20))
    label_username.place(relx=0.13, rely=0.03)

    entry_student_lusername = CTkEntry(master=frame_login,placeholder_text="           Username",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_lusername.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.08)

    label_password = CTkLabel(master=frame_login,text='Enter Password',font=('Roboto',20))
    label_password.place(relx=0.13, rely=0.19)

    entry_student_lpassword = CTkEntry(master=frame_login,placeholder_text="           Password",show='*',
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_lpassword.place(relx=0.03, rely=0.24, relwidth=0.82, relheight=0.08)

    switch_lpassword = CTkSwitch(master=frame_login,text='Show',font=('Roboto',12),switch_height=15,switch_width=30,
        command=lambda:None)
    switch_lpassword.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    button_login = CTkButton(master=frame_login,text='Login',border_width=3,corner_radius=15,border_color='#3f60fc',
        command=None)
    button_login.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)
    
    # Filler Frame for Register button
    filler_frame = CTkFrame(master=main_frame, border_width=5, fg_color='#3333ff')
    filler_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
    
    filler_frame_label = CTkLabel(master=filler_frame, text="Don't have an account?",font=('Roboto',30,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_register = CTkButton(master=filler_frame,text='Register',font=('Roboto',24),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#3e9eff',hover_color='#d7d7d7',command=student_button_click_register)
    button_register.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)


def student_button_click_register():
    button_admin.place(rely=0.3, relheight=0.41)
    button_student.place(rely=0.2, relheight=0.61)

    # Remove all the widgets from the main_frame
    try:
        for widget in main_frame.winfo_children():
            widget.destroy()
    except:
        pass

    # Filler Frame for Register button
    filler_frame = CTkFrame(master=main_frame, border_width=5, fg_color='#3333ff')
    filler_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    filler_frame_label = CTkLabel(master=filler_frame, text="Already have an account?",font=('Roboto',26,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_login = CTkButton(master=filler_frame,text='Login',font=('Roboto',26),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#3e9eff',hover_color='#d7d7d7',command=student_button_click_login)
    button_login.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

    # Login Frame
    label_register = CTkLabel(master=main_frame,text='Register',font=('Roboto',22,))
    label_register.place(relx=0.2, rely=0.05)

    frame_register = CTkFrame(master=main_frame,border_width=4,border_color='#3f60fc')
    frame_register.place(relx=0.02, rely=0.12, relwidth=0.46, relheight=0.84)

    label_username = CTkLabel(master=frame_register,text='Create Username',font=('Roboto',20))
    label_username.place(relx=0.13, rely=0.03)

    entry_student_rusername = CTkEntry(master=frame_register,placeholder_text="    Username",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    # entry_rusername.bind('<KeyRelease>',empty_entry)
    entry_student_rusername.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.08)

    label_password1 = CTkLabel(master=frame_register,text='Create Password',font=('Roboto',20))
    label_password1.place(relx=0.13, rely=0.19)

    entry_student_rpassword1 = CTkEntry(master=frame_register,placeholder_text="    Password",show='*',
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    # entry_rpassword1.bind('<KeyRelease>',empty_entry)
    entry_student_rpassword1.place(relx=0.03, rely=0.24, relwidth=0.82, relheight=0.08)

    switch_rpassword1 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        command=lambda:None)
    switch_rpassword1.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    label_password2 = CTkLabel(master=frame_register,text='Confirm Password',font=('Roboto',20))
    label_password2.place(relx=0.13, rely=0.37)

    entry_student_rpassword2 = CTkEntry(master=frame_register,placeholder_text="   Confirm Password",show='*',
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_rpassword2.place(relx=0.03, rely=0.42, relwidth=0.82, relheight=0.08)

    switch_rpassword2 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        command=lambda:None)
    switch_rpassword2.place(relx=0.87, rely=0.43, relwidth=0.1, relheight=0.05)

    label_gmail = CTkLabel(master=frame_register,text='Enter Email',font=('Roboto',20))
    label_gmail.place(relx=0.13, rely=0.55)

    entry_rgmail = CTkEntry(master=frame_register,placeholder_text="    Someone123@gmail.com",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,),)
    # entry_rgmail.bind('<KeyRelease>',empty_entry)
    # entry_rgmail.bind('<KeyRelease>',email_check)
    entry_rgmail.place(relx=0.03, rely=0.60, relwidth=0.9, relheight=0.08)
    
    label_error = CTkLabel(master=frame_register,text='',font=('Roboto',13))
    label_error.place(relx=0.3, rely=0.73)

    button_register = CTkButton(master=frame_register,text='Register',border_width=3,corner_radius=15,
        border_color='#3f60fc',command=None,state='disabled')
    button_register.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)


def admin_button_click_login():
    button_student.place(rely=0.3, relheight=0.41)
    button_admin.place(rely=0.2, relheight=0.61)

    # Remove all the widgets from the main_frame
    try:
        for widget in main_frame.winfo_children():
            widget.destroy()
    except:
        pass

    # Login Frame
    label_login = CTkLabel(master=main_frame,text='Login',font=('Roboto',22,))
    label_login.place(relx=0.7, rely=0.05)

    frame_login = CTkFrame(master=main_frame,border_width=4,border_color='#ff0000')
    frame_login.place(relx=0.52, rely=0.12, relwidth=0.46, relheight=0.84)

    label_username = CTkLabel(master=frame_login,text='Enter Username',font=('Roboto',20))
    label_username.place(relx=0.13, rely=0.03)

    entry_admin_lusername = CTkEntry(master=frame_login,placeholder_text="           Username",
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    entry_admin_lusername.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.08)

    label_password = CTkLabel(master=frame_login,text='Enter Password',font=('Roboto',20))
    label_password.place(relx=0.13, rely=0.19)

    entry_admin_lpassword = CTkEntry(master=frame_login,placeholder_text="           Password",show='*',
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    entry_admin_lpassword.place(relx=0.03, rely=0.24, relwidth=0.82, relheight=0.08)

    switch_lpassword = CTkSwitch(master=frame_login,text='Show',font=('Roboto',12),switch_height=15,switch_width=30,
        progress_color='#ff0000', command=lambda:None)
    switch_lpassword.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    button_login = CTkButton(master=frame_login,text='Login',border_width=3,corner_radius=15,border_color='#ff0000',
        fg_color='#ff0000', hover_color='#d20000', command=None)
    button_login.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)

    # Filler Frame for Register button
    filler_frame = CTkFrame(master=main_frame, border_width=5, corner_radius=0, fg_color='#ff0000')
    filler_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    filler_frame_label = CTkLabel(master=filler_frame, text=" "*10+"New Admin?",font=('Roboto',30,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_register = CTkButton(master=filler_frame,text='Register',font=('Roboto',24),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#ff0000',hover_color='#d7d7d7',command=admin_button_click_register)
    button_register.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)


def admin_button_click_register():
    button_student.place(rely=0.3, relheight=0.41)
    button_admin.place(rely=0.2, relheight=0.61)

    # Remove all the widgets from the main_frame
    try:
        for widget in main_frame.winfo_children():
            widget.destroy()
    except:
        pass

    # Filler Frame for Register button
    filler_frame = CTkFrame(master=main_frame, border_width=5, corner_radius=0, fg_color='#ff0000')
    filler_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    filler_frame_label = CTkLabel(master=filler_frame, text=" "*8+"Already an Admin?",font=('Roboto',26,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_login = CTkButton(master=filler_frame,text='Login',font=('Roboto',26),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#ff0000',hover_color='#d7d7d7',command=admin_button_click_login)
    button_login.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

    # Login Frame
    label_register = CTkLabel(master=main_frame,text='Register',font=('Roboto',22,))
    label_register.place(relx=0.2, rely=0.05)

    frame_register = CTkFrame(master=main_frame,border_width=4,border_color='#ff0000')
    frame_register.place(relx=0.02, rely=0.12, relwidth=0.46, relheight=0.84)

    label_username = CTkLabel(master=frame_register,text='Create Username',font=('Roboto',20))
    label_username.place(relx=0.13, rely=0.03)

    entry_rusername = CTkEntry(master=frame_register,placeholder_text="    Username",
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    # entry_rusername.bind('<KeyRelease>',empty_entry)
    entry_rusername.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.08)

    label_password1 = CTkLabel(master=frame_register,text='Create Password',font=('Roboto',20))
    label_password1.place(relx=0.13, rely=0.19)

    entry_rpassword1 = CTkEntry(master=frame_register,placeholder_text="    Password",show='*',
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    # entry_rpassword1.bind('<KeyRelease>',empty_entry)
    entry_rpassword1.place(relx=0.03, rely=0.24, relwidth=0.82, relheight=0.08)

    switch_rpassword1 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        progress_color='#ff0000', command=lambda:None)
    switch_rpassword1.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    label_password2 = CTkLabel(master=frame_register,text='Confirm Password',font=('Roboto',20))
    label_password2.place(relx=0.13, rely=0.37)

    entry_rpassword2 = CTkEntry(master=frame_register,placeholder_text="   Confirm Password",show='*',
        border_width=3, corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    entry_rpassword2.place(relx=0.03, rely=0.42, relwidth=0.82, relheight=0.08)

    switch_rpassword2 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        progress_color='#ff0000', command=lambda:None)
    switch_rpassword2.place(relx=0.87, rely=0.43, relwidth=0.1, relheight=0.05)

    label_gmail = CTkLabel(master=frame_register,text='Enter Email',font=('Roboto',20))
    label_gmail.place(relx=0.13, rely=0.55)

    entry_rgmail = CTkEntry(master=frame_register,placeholder_text="    Someone123@gmail.com",
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,),)
    # entry_rgmail.bind('<KeyRelease>',empty_entry)
    # entry_rgmail.bind('<KeyRelease>',email_check)
    entry_rgmail.place(relx=0.03, rely=0.60, relwidth=0.9, relheight=0.08)
    
    label_error = CTkLabel(master=frame_register,text='',font=('Roboto',13))
    label_error.place(relx=0.3, rely=0.73)

    button_register = CTkButton(master=frame_register,text='Register',border_width=3,corner_radius=15,
        border_color='#ff0000',fg_color='#ff0000', hover_color='#d20000',command=None,state='disabled')
    button_register.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)


def student_main_win():
    global profile_button, all_books_button, return_books_button

    # Remove all the widgets from the main_win
    try:
        for widget in root.winfo_children():
            widget.destroy()
    except:
        pass

    side_frame = CTkFrame(root, border_width=5,corner_radius=0,)
    side_frame.place(relx=0,rely=0,relwidth=0.15,relheight=1)
    
    profile_button = CTkButton(side_frame,text='Profile',border_width=4,corner_radius=0,border_color='#818181',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=profile_button_click)
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.5)

    all_books_button = CTkButton(side_frame,text='All Books',border_width=4,corner_radius=0,border_color='#818181',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=all_books_button_click)
    all_books_button.place(relx=0,rely=0.5, relwidth=1, relheight=0.25)

    return_books_button = CTkButton(side_frame,text='Return Books',border_width=4,corner_radius=0,border_color='#818181',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=return_books_button_click)
    return_books_button.place(relx=0,rely=0.75, relwidth=1, relheight=0.25)

def profile_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.5)
    all_books_button.place(relx=0,rely=0.5, relwidth=1, relheight=0.25)
    return_books_button.place(relx=0,rely=0.75, relwidth=1, relheight=0.25)

def all_books_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.25)
    all_books_button.place(relx=0,rely=0.25, relwidth=1, relheight=0.5)
    return_books_button.place(relx=0,rely=0.75, relwidth=1, relheight=0.25)

def return_books_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.25)
    all_books_button.place(relx=0,rely=0.25, relwidth=1, relheight=0.25)
    return_books_button.place(relx=0,rely=0.5, relwidth=1, relheight=0.5)



main_win()
# student_main_win()

root.mainloop()
