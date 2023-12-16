from customtkinter import *
from CTkMessagebox import CTkMessagebox
from time import strftime
import sqlite3
import os
import hashlib


root = CTk()

root.title("Library Management System")
root.wm_state("zoomed")
set_appearance_mode('dark')
root.geometry(f"{1920}x{1080}")
root.iconbitmap(r'Icon.ico')

student_detail = "studentetail"
admin_detail = 'admindetail'

# Creating Directory for database
path = os.environ["userprofile"]
try:
    os.mkdir(path+"\\Documents\\Library Database")
except FileExistsError:
    pass

con = sqlite3.connect(path+"\\Documents\\Library Database\mydatabase.db")
cur = con.cursor()

###### >>>>>   Creating Tables
# con.execute("DROP TABLE IF EXISTS studentetail")   # Drop the existing table if it exists

# admin details
con.execute("""CREATE TABLE IF NOT EXISTS admindetail
            (admname varchar(30) PRIMARY KEY, 
            password varchar(30));""")

# student details
con.execute("""CREATE TABLE IF NOT EXISTS studentetail 
            (username varchar(30) PRIMARY KEY, 
            password varchar(30),
            email varchar(60));""")

# books details
con.execute("""CREATE TABLE IF NOT EXISTS booksdetail
            (bid varchar(20) PRIMARY KEY, 
            title varchar(30), 
            subject varchar(30), 
            author varchar(30), 
            status varchar(30) NOT NULL DEFAULT 'Available');""")

# borrow details
con.execute("""CREATE TABLE IF NOT EXISTS bookissuedetail 
            (bid varchar(20),
            username varchar(20),
            PRIMARY KEY (bid, username),
            FOREIGN KEY (bid) REFERENCES booksdetail(bid),
            FOREIGN KEY (username) REFERENCES studentetail(username));""")

# Open and read the CSV file
current_dir = os.getcwd()+'\\My sys\\'
with open(current_dir+'booksdata.txt', 'r') as file:
    data = [tuple(line.strip().split(',')) for line in file]

# Insert data into the SQLite table
cur.executemany('INSERT OR IGNORE INTO booksdetail VALUES (?, ?, ?, ?, ?)', data)
con.commit()


#######    Some Functions    ############
def hash_password(password):
    # Hash the password before storing it
    return hashlib.sha256(password.encode()).hexdigest()

def empty_entry_student(event):
    if entry_student_rusername.get().strip()!="" and entry_student_rpassword1.get().strip()!="" and entry_student_rpassword2.get().strip()!="" and entry_student_remail.get().strip()!="":
        button_student_register.configure(state='normal')
    else:
        button_student_register.configure(state='disabled')

def empty_entry_admin(event):
    if entry_admin_rusername.get().strip()!="" and entry_admin_rpassword1.get().strip()!="" and entry_admin_rpassword2.get().strip()!="" and entry_admin_remail.get().strip()!="":
        button_admin_register.configure(state='normal')
    else:
        button_admin_register.configure(state='disabled')

def email_check_student(event):
    check = entry_student_remail.get()
    if '@gmail.com'in check or'@mail.com'in check or'@outlook.com'in check or'@yahoo.com'in check or'@icloud.com'in check or'@fastmail.com'in check:
        entry_student_remail.configure(border_color='#3f60fc')
        label_error_student.configure(text='Valid Gmail',text_color='#26c115')
    else:
        entry_student_remail.configure(border_color='#f8182f')
        label_error_student.configure(text='Invalid Gmail',text_color='#f8182f')

def email_check_admin(event):
    check = entry_admin_remail.get()
    if '@gmail.com'in check or'@mail.com'in check or'@outlook.com'in check or'@yahoo.com'in check or'@icloud.com'in check or'@fastmail.com'in check:
        entry_admin_remail.configure(border_color='#f8182f')
        label_error_admin.configure(text='Valid Gmail',text_color='#26c115')
    else:
        entry_admin_remail.configure(border_color='#3f60fc')
        label_error_admin.configure(text='Invalid Gmail',text_color='#f8182f')

def pass_switch(to_switch, entry_password):
    on_off = to_switch.get()
    if on_off == 1:
        entry_password.configure(show='')
    elif on_off == 0:
        entry_password.configure(show='*')

def update_daydatetime():
    current_time = strftime('%H:%M:%S %p')
    timelabel.configure(text=current_time)
    current_day = strftime('%A')
    daylabel.configure(text=current_day)
    current_date = strftime('%B %d, %Y')
    datelabel.configure(text=current_date)
    timelabel.after(1000, update_daydatetime)  # Update every 1000 milliseconds (1 second)


#############   Register and Login functions for Student and Admin   #########
#  >> Student
def student_register():
    # Getting details
    username = entry_student_rusername.get()
    userpassword = hash_password(entry_student_rpassword1.get())
    useremail = entry_student_remail.get()

    sql = f"INSERT INTO {student_detail} VALUES (?, ?, ?)"
    data = (username, userpassword, useremail)
    try:
        cur.execute(sql, data)
        con.commit()
        CTkMessagebox(title="Success", message="Successfully registered", icon='check', option_1='Thanks')

        entry_student_rusername.delete(0, END)
        entry_student_rpassword1.delete(0, END)
        entry_student_rpassword2.delete(0, END)
        entry_student_remail.delete(0, END)
    except sqlite3.Error as e:
        CTkMessagebox(title="Error inserting", message=f"Cannot add data to Database \nError: {e}", icon='cancel', option_1='Okay')
    
    # Print the SQL statement used for table creation
    # cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='studentetail'")
    # print(cur.fetchone()[0])

def student_login():
    # Getting details
    username = entry_student_lusername.get()
    userpassword = hash_password(entry_student_lpassword.get())
    sqlLoginInfo = f"SELECT password FROM {student_detail} WHERE username = ?"
    try:
        cur.execute(sqlLoginInfo, (username,))

        # Fetch the first result
        result = cur.fetchone()

        if result and result[0] == userpassword:
            CTkMessagebox(title="Done", message="Student Logged In!", icon='check', option_1='Nice!')

        else:
            CTkMessagebox(title="WRONG PASSWORD", message="What? You can't even remember \nyour own password?", icon='warning', option_1='Okay')
    except sqlite3.Error as e:
        CTkMessagebox(title="FAILED", message=f"Error: {e}", icon='cancel', option_1='Okay')

#  >> Admin
def admin_register():
    # Getting details
    adminname = entry_admin_rusername.get()
    adminpassword = hash_password(entry_admin_rpassword1.get())
    adminemail = entry_admin_remail.get()

    sql = f"INSERT INTO {admin_detail} VALUES (?, ?, ?)"
    data = (adminname, adminpassword, adminemail)
    try:
        cur.execute(sql, data)
        con.commit()
        CTkMessagebox(title="Success", message="Successfully registered", icon='check', option_1='Thanks')

        entry_admin_rusername.delete(0, END)
        entry_admin_rpassword1.delete(0, END)
        entry_admin_rpassword2.delete(0, END)
        entry_admin_remail.delete(0, END)
    except sqlite3.Error as e:
        CTkMessagebox(title="Error inserting", message=f"Cannot add data to Database \nError: {e}", icon='cancel', option_1='Okay')

def admin_login():
    # Getting details
    adminname = entry_admin_lusername.get()
    adminpassword = hash_password(entry_admin_lpassword.get())
    sqlLoginInfo = f"SELECT password FROM {admin_detail} WHERE username = ?"
    try:
        cur.execute(sqlLoginInfo, (adminname,))

        # Fetch the first result
        result = cur.fetchone()

        if result and result[0] == adminpassword:
            CTkMessagebox(title="Done", message="Admin Logged In!", icon='check', option_1='Nice!')

        else:
            CTkMessagebox(title="WRONG PASSWORD", message="What? You can't even remember \nyour own password?", icon='warning', option_1='Okay')
    except sqlite3.Error as e:
        CTkMessagebox(title="FAILED", message=f"Error: {e}", icon='cancel', option_1='Okay')


##############    MAIN  SCREEN    #############
def main_win():
    global button_student, button_admin, main_frame, timelabel, daylabel, datelabel

    button_student = CTkButton(master=root,text='Student',border_width=5,corner_radius=15,border_color='#3333ff',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=student_button_click_register)
    button_student.place(relx=0.07,rely=0.3, relwidth=0.1, relheight=0.41)

    main_frame = CTkFrame(root, border_width=5,corner_radius=8,)
    main_frame.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.8)

    button_admin = CTkButton(master=root,text='Admin',border_width=5,corner_radius=15,border_color='#ff0000',
        fg_color='#ff3737', hover_color='#d20000',font=('Roboto',22,),command=admin_button_click_login)
    button_admin.place(relx=0.83,rely=0.3, relwidth=0.1, relheight=0.41)

    datetime_frame = CTkFrame(root, border_width=3, corner_radius=2)
    datetime_frame.place(relx=0.80,rely=0.01, relwidth=0.19, relheight=0.15)

    # Create a timelabel for displaying the time, day and date
    timelabel = CTkLabel(datetime_frame, font=('calibri',40,'bold'))
    timelabel.place(relx=0.01,rely=0.02, relwidth=0.9, relheight=0.38)
    daylabel = CTkLabel(datetime_frame, font=('calibri', 20, 'bold'))
    daylabel.place(relx=0.01, rely=0.40, relwidth=0.9, relheight=0.26)
    datelabel = CTkLabel(datetime_frame, font=('calibri', 20, 'bold'))
    datelabel.place(relx=0.01, rely=0.68, relwidth=0.9, relheight=0.26)

    update_daydatetime()


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
    global entry_student_lusername, entry_student_lpassword

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

    switch_student_lpassword = CTkSwitch(master=frame_login,text='Show',font=('Roboto',12),switch_height=15,switch_width=30,
        command=lambda:pass_switch(switch_student_lpassword, entry_student_lpassword))
    switch_student_lpassword.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    button_student_login = CTkButton(master=frame_login,text='Login',border_width=3,corner_radius=15,border_color='#3f60fc',
        command=student_login)
    button_student_login.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)
    
    # Filler Frame for Register button
    filler_frame = CTkFrame(master=main_frame, border_width=5, fg_color='#3333ff')
    filler_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
    
    filler_frame_label = CTkLabel(master=filler_frame, text="Don't have an account?",font=('Roboto',30,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_register = CTkButton(master=filler_frame,text='Register',font=('Roboto',24),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#3e9eff',hover_color='#d7d7d7',command=student_button_click_register)
    button_register.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

def student_button_click_register():
    global entry_student_rusername, entry_student_rpassword1, entry_student_rpassword2, entry_student_remail
    global button_student_register, label_error_student, switch_student_rpassword1, switch_student_rpassword2

    button_admin.place(rely=0.3, relheight=0.41)
    button_student.place(rely=0.2, relheight=0.61)

    # Remove all the widgets from the main_frame
    try:
        for widget in main_frame.winfo_children():
            widget.destroy()
    except:
        pass

    # Filler Frame for Login button
    filler_frame = CTkFrame(master=main_frame, border_width=5, fg_color='#3333ff')
    filler_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    filler_frame_label = CTkLabel(master=filler_frame, text="Already have an account?",font=('Roboto',26,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_login = CTkButton(master=filler_frame,text='Login',font=('Roboto',26),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#3e9eff',hover_color='#d7d7d7',command=student_button_click_login)
    button_login.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

    # Register Frame
    label_register = CTkLabel(master=main_frame,text='Register',font=('Roboto',22,))
    label_register.place(relx=0.2, rely=0.05)

    frame_register = CTkFrame(master=main_frame,border_width=4,border_color='#3f60fc')
    frame_register.place(relx=0.02, rely=0.12, relwidth=0.46, relheight=0.84)

    label_username = CTkLabel(master=frame_register,text='Create Username',font=('Roboto',20))
    label_username.place(relx=0.13, rely=0.03)

    entry_student_rusername = CTkEntry(master=frame_register,placeholder_text="    Username",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_rusername.bind('<KeyRelease>',empty_entry_student)
    entry_student_rusername.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.08)

    label_password1 = CTkLabel(master=frame_register,text='Create Password',font=('Roboto',20))
    label_password1.place(relx=0.13, rely=0.19)

    entry_student_rpassword1 = CTkEntry(master=frame_register,placeholder_text="    Password",show='*',
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_rpassword1.bind('<KeyRelease>',empty_entry_student)
    entry_student_rpassword1.place(relx=0.03, rely=0.24, relwidth=0.82, relheight=0.08)

    switch_student_rpassword1 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        command=lambda:pass_switch(switch_student_rpassword1, entry_student_rpassword1))
    switch_student_rpassword1.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    label_password2 = CTkLabel(master=frame_register,text='Confirm Password',font=('Roboto',20))
    label_password2.place(relx=0.13, rely=0.37)

    entry_student_rpassword2 = CTkEntry(master=frame_register,placeholder_text="   Confirm Password",show='*',
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_rpassword2.place(relx=0.03, rely=0.42, relwidth=0.82, relheight=0.08)

    switch_student_rpassword2 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        command=lambda:pass_switch(switch_student_rpassword2, entry_student_rpassword2))
    switch_student_rpassword2.place(relx=0.87, rely=0.43, relwidth=0.1, relheight=0.05)

    label_email = CTkLabel(master=frame_register,text='Enter Email',font=('Roboto',20))
    label_email.place(relx=0.13, rely=0.55)

    entry_student_remail = CTkEntry(master=frame_register,placeholder_text="    Someone123@gmail.com",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,),)
    entry_student_remail.bind('<KeyRelease>',empty_entry_student)
    entry_student_remail.bind('<KeyRelease>',email_check_student)
    entry_student_remail.place(relx=0.03, rely=0.60, relwidth=0.9, relheight=0.08)

    label_error_student = CTkLabel(master=frame_register,text='',font=('Roboto',13))
    label_error_student.place(relx=0.3, rely=0.7)

    button_student_register = CTkButton(master=frame_register,text='Register',border_width=3,corner_radius=15,
        border_color='#3f60fc',command=student_register,state='disabled')
    button_student_register.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)


def admin_button_click_login():
    global entry_admin_lusername, entry_admin_lpassword

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

    switch_admin_lpassword = CTkSwitch(master=frame_login,text='Show',font=('Roboto',12),switch_height=15,switch_width=30,
        progress_color='#ff0000', command=lambda:pass_switch(switch_admin_lpassword, entry_admin_lpassword))
    switch_admin_lpassword.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    button_admin_login = CTkButton(master=frame_login,text='Login',border_width=3,corner_radius=15,border_color='#ff0000',
        fg_color='#ff0000', hover_color='#d20000', command=None)
    button_admin_login.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)

    # Filler Frame for Register button
    filler_frame = CTkFrame(master=main_frame, border_width=5, corner_radius=0, fg_color='#ff0000')
    filler_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    filler_frame_label = CTkLabel(master=filler_frame, text=" "*10+"New Admin?",font=('Roboto',30,'bold'))
    filler_frame_label.place(relx=0.05, rely=0.4,)

    button_register = CTkButton(master=filler_frame,text='Register',font=('Roboto',24),border_width=3,corner_radius=15,
    border_color='#ffffff',fg_color='#ffffff',text_color='#ff0000',hover_color='#d7d7d7',command=admin_button_click_register)
    button_register.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

def admin_button_click_register():
    global entry_admin_rusername, entry_admin_rpassword1, entry_admin_rpassword2, entry_admin_remail
    global button_admin_register, label_error_admin, switch_admin_rpassword1, switch_admin_rpassword2

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

    entry_admin_rusername = CTkEntry(master=frame_register,placeholder_text="    Username",
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    entry_admin_rusername.bind('<KeyRelease>',empty_entry_admin)
    entry_admin_rusername.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.08)

    label_password1 = CTkLabel(master=frame_register,text='Create Password',font=('Roboto',20))
    label_password1.place(relx=0.13, rely=0.19)

    entry_admin_rpassword1 = CTkEntry(master=frame_register,placeholder_text="    Password",show='*',
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    entry_admin_rpassword1.bind('<KeyRelease>',empty_entry_admin)
    entry_admin_rpassword1.place(relx=0.03, rely=0.24, relwidth=0.82, relheight=0.08)

    switch_admin_rpassword1 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        progress_color='#ff0000', command=lambda:pass_switch(switch_admin_rpassword1, entry_admin_rpassword1))
    switch_admin_rpassword1.place(relx=0.87, rely=0.25, relwidth=0.1, relheight=0.05)

    label_password2 = CTkLabel(master=frame_register,text='Confirm Password',font=('Roboto',20))
    label_password2.place(relx=0.13, rely=0.37)

    entry_admin_rpassword2 = CTkEntry(master=frame_register,placeholder_text="   Confirm Password",show='*',
        border_width=3, corner_radius=10,border_color='#ff0000',font=('Roboto',15,))
    entry_admin_rpassword2.place(relx=0.03, rely=0.42, relwidth=0.82, relheight=0.08)

    switch_admin_rpassword2 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        progress_color='#ff0000', command=lambda:pass_switch(switch_admin_rpassword2, entry_admin_rpassword2))
    switch_admin_rpassword2.place(relx=0.87, rely=0.43, relwidth=0.1, relheight=0.05)

    label_gmail = CTkLabel(master=frame_register,text='Enter Email',font=('Roboto',20))
    label_gmail.place(relx=0.13, rely=0.55)

    entry_admin_remail = CTkEntry(master=frame_register,placeholder_text="    Someone123@gmail.com",
        border_width=3,corner_radius=10,border_color='#ff0000',font=('Roboto',15,),)
    entry_admin_remail.bind('<KeyRelease>',empty_entry_admin)
    entry_admin_remail.bind('<KeyRelease>',email_check_admin)
    entry_admin_remail.place(relx=0.03, rely=0.60, relwidth=0.9, relheight=0.08)

    label_error_admin = CTkLabel(master=frame_register,text='',font=('Roboto',13))
    label_error_admin.place(relx=0.3, rely=0.7)

    button_admin_register = CTkButton(master=frame_register,text='Register',border_width=3,corner_radius=15,
        border_color='#ff0000',fg_color='#ff0000', hover_color='#d20000',command=admin_register,state='disabled')
    button_admin_register.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)


def student_main_win():
    global profile_button, all_books_button, return_books_button, main_frame_student_win

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
    all_books_button.place(relx=0,rely=0.5, relwidth=1, relheight=0.2)

    return_books_button = CTkButton(side_frame,text='Return Books',border_width=4,corner_radius=0,border_color='#818181',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=return_books_button_click)
    return_books_button.place(relx=0,rely=0.7, relwidth=1, relheight=0.2)
    
    back_button = CTkButton(side_frame,text='Back',border_width=4,corner_radius=0,border_color='#818181',
        fg_color='#3333ff', hover_color='#ff8000',font=('Roboto',22,),command=None)
    back_button.place(relx=0,rely=0.9, relwidth=1, relheight=0.1)

    main_frame_student_win = CTkFrame(root, border_width=0, corner_radius=0)
    main_frame_student_win.place(relx=0.15, rely=0, relwidth=0.85, relheight=1)

def student_main_win_profile():
    pass

def profile_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.5)
    all_books_button.place(relx=0,rely=0.5, relwidth=1, relheight=0.2)
    return_books_button.place(relx=0,rely=0.7, relwidth=1, relheight=0.2)

def all_books_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.2)
    all_books_button.place(relx=0,rely=0.2, relwidth=1, relheight=0.5)
    return_books_button.place(relx=0,rely=0.7, relwidth=1, relheight=0.2)

def return_books_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.2)
    all_books_button.place(relx=0,rely=0.2, relwidth=1, relheight=0.2)
    return_books_button.place(relx=0,rely=0.4, relwidth=1, relheight=0.5)



# main_win()
student_main_win()

root.mainloop()
