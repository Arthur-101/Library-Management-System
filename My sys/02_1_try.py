from customtkinter import *
from CTkMessagebox import CTkMessagebox
import tkinter as tk
from tkinter import ttk
from time import strftime
from PIL import Image
import sqlite3
import os
import hashlib
import random


root = CTk()

root.title("Library Management System")
root.wm_state("zoomed")
set_appearance_mode('dark')
root.geometry(f"{1920}x{1080}")
root.iconbitmap(r'Icon.ico')

student_detail = "studentdetail"
admin_detail = 'admindetail'
books_detail = 'booksdetail'
book_issue_detail = 'bookissuedetail'

pfp_dir = os.getcwd()+'\\pfp\\'

# Creating Directory for database
path = os.environ["userprofile"]
try:
    os.mkdir(path+"\\Documents\\Library Database")
except FileExistsError:
    pass

con = sqlite3.connect(path+"\\Documents\\Library Database\mydatabase.db")
cur = con.cursor()

###### >>>>>   Creating Tables
# con.execute("DROP TABLE IF EXISTS admindetail")   # Drop the existing table if it exists
# con.execute("DROP TABLE IF EXISTS studentdetail")   # Drop the existing table if it exists
# con.execute("DROP TABLE IF EXISTS booksdetail")   # Drop the existing table if it exists
# con.execute("DROP TABLE IF EXISTS bookissuedetail")   # Drop the existing table if it exists

# admin details
con.execute("""CREATE TABLE IF NOT EXISTS admindetail
            (admname varchar(30) PRIMARY KEY, 
            password varchar(30));""")

# student details
con.execute("""CREATE TABLE IF NOT EXISTS studentdetail 
            (username varchar(30) PRIMARY KEY, 
            password varchar(30),
            class varchar(3),
            email varchar(60),
            pfp varchar(10));""")

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
            FOREIGN KEY (username) REFERENCES studentdetail(username));""")

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

def get_treeview_length(treeview):
    # Getting the last item in the tree
    last_item = treeview.item(treeview.get_children()[-1])
    # index of the last item
    last_index = treeview.index(last_item['tags'])
    # last index + 1 = total length
    return last_index + 1


#############   Register and Login functions for Student and Admin   #########
#  >> Student
def student_register():
    # Getting details
    username = entry_student_rusername.get()
    userpassword = hash_password(entry_student_rpassword1.get())
    userclass = entry_student_class.get()
    useremail = entry_student_remail.get()
    
    pfp_files = [f for f in os.listdir(pfp_dir) if f.endswith('.jpg') or f.endswith('.png')]
    selected_pfp = random.choice(pfp_files)

    sql = f"INSERT INTO {student_detail} VALUES (?, ?, ?, ?, ?)"
    data = (username, userpassword, userclass, useremail, selected_pfp)
    try:
        cur.execute(sql, data)
        con.commit()
        CTkMessagebox(title="Success", message="Successfully registered", icon='check', option_1='Thanks')

        entry_student_rusername.delete(0, END)
        entry_student_rpassword1.delete(0, END)
        entry_student_rpassword2.delete(0, END)
        entry_student_class.delete(0, END)
        entry_student_remail.delete(0, END)
    except sqlite3.Error as e:
        CTkMessagebox(title="Error inserting", message=f"Cannot add data to Database \nError: {e}", icon='cancel', option_1='Okay')

    # Print the SQL statement used for table creation
    # cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='studentdetail'")
    # print(cur.fetchone()[0])

def student_login():
    global pfp_image, username
    # Getting details
    username = entry_student_lusername.get()
    userpassword = hash_password(entry_student_lpassword.get())
    sqlLoginInfo = f"SELECT password FROM {student_detail} WHERE username = ?"
    sqlpfp = f"SELECT pfp FROM {student_detail} WHERE username = ?"
    try:
        cur.execute(sqlLoginInfo, (username,))
        # Fetch the first result
        result = cur.fetchone()

        if result and result[0] == userpassword:
            # CTkMessagebox(title="Done", message="Student Logged In!", icon='check', option_1='Nice!')

            cur.execute(sqlpfp, (username,))
            result_pfp = cur.fetchone()

            if result_pfp:
                selected_image = result_pfp[0]
                image_path = os.path.join(pfp_dir, selected_image)

                # Load and display the image
                pfp_image = CTkImage(dark_image=Image.open(image_path), size=(220,220))
            else:
                pfp_image = "No PFP Found..."

            student_main_win(pfp_image, username)

        else:
            CTkMessagebox(title="WRONG PASSWORD", message="What? You can't even remember \nyour own ID or password?", icon='warning', option_1='I will try again')
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
    global entry_student_rusername, entry_student_rpassword1, entry_student_rpassword2, entry_student_class, entry_student_remail
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

    # label_password2 = CTkLabel(master=frame_register,text='Confirm Password',font=('Roboto',20))
    # label_password2.place(relx=0.13, rely=0.37)

    entry_student_rpassword2 = CTkEntry(master=frame_register,placeholder_text="   Confirm Password",show='*',
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,))
    entry_student_rpassword2.place(relx=0.03, rely=0.37, relwidth=0.82, relheight=0.08)

    switch_student_rpassword2 = CTkSwitch(master=frame_register,text='Show',font=('Roboto',12,),switch_height=15,switch_width=30,
        command=lambda:pass_switch(switch_student_rpassword2, entry_student_rpassword2))
    switch_student_rpassword2.place(relx=0.87, rely=0.38, relwidth=0.1, relheight=0.05)

    entry_student_class = CTkEntry(frame_register, placeholder_text="    Enter Your Class (Eg: X, Xi, XII)",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,),)
    entry_student_class.place(relx=0.03, rely=0.51, relwidth=0.9, relheight=0.08)

    label_email = CTkLabel(master=frame_register,text='Enter Email',font=('Roboto',20))
    label_email.place(relx=0.13, rely=0.61)

    entry_student_remail = CTkEntry(master=frame_register,placeholder_text="    Someone123@gmail.com",
        border_width=3,corner_radius=10,border_color='#3f60fc',font=('Roboto',15,),)
    entry_student_remail.bind('<KeyRelease>',empty_entry_student)
    entry_student_remail.bind('<KeyRelease>',email_check_student)
    entry_student_remail.place(relx=0.03, rely=0.66, relwidth=0.9, relheight=0.08)

    label_error_student = CTkLabel(master=frame_register,text='',font=('Roboto',13))
    label_error_student.place(relx=0.3, rely=0.76)

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


def student_main_win(pfp_image, username):
    global main_frame_student_win, profile_button, all_books_button, return_books_button, main_second_frame_student_win

    # Remove all the widgets from the main_win
    try:
        for widget in root.winfo_children():
            widget.destroy()
    except:
        pass
    
    main_frame_student_win = CTkFrame(root, border_width=0, corner_radius=0)
    main_frame_student_win.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    side_frame = CTkFrame(main_frame_student_win, border_width=5,corner_radius=0,)
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
        fg_color='#3333ff', hover_color='#ff8000',font=('Roboto',22,),command=back_button_click)
    back_button.place(relx=0,rely=0.9, relwidth=1, relheight=0.1)

    main_second_frame_student_win = CTkFrame(main_frame_student_win, border_width=0, corner_radius=0)
    main_second_frame_student_win.place(relx=0.15, rely=0, relwidth=0.85, relheight=1)

    student_main_win_profile(pfp_image, username)

def student_main_win_profile(pfp_image, username):
     # Remove all the widgets from the main_second_frame_student_win
    try:
        for widget in main_second_frame_student_win.winfo_children():
            widget.destroy()
    except:
        pass
    
    def on_select(event):
        selected_item = tree.selection()
    
    sql_student_username = f"SELECT username FROM {student_detail} WHERE username = ?"
    cur.execute(sql_student_username, (username,))
    info_username = cur.fetchone()     # Fetch the first result

    sql_student_class = f"SELECT class FROM {student_detail} WHERE username = ?"
    cur.execute(sql_student_class, (username,))
    info_class = cur.fetchone()

    sql_student_email = f"SELECT email FROM {student_detail} WHERE username = ?"
    cur.execute(sql_student_email, (username,))
    info_email = cur.fetchone()

    # Profile frame
    profile_frame = CTkFrame(main_second_frame_student_win, border_width=0, corner_radius=0)
    profile_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)
    
    pfp_frame = CTkFrame(profile_frame, border_width=0, corner_radius=0, fg_color="#2b2b2b")
    pfp_frame.place(relx=0.4, rely=0.06, relwidth=0.2, relheight=0.6)
    # Create a label to display the pfp
    pfp_label = CTkLabel(pfp_frame, text='', image = pfp_image)
    pfp_label.place(relx=0, rely=-0, relwidth=1, relheight=1)

    name_label = CTkLabel(profile_frame,text='Username : ',font=('Roboto',20))
    name_label.place(relx=0.1, rely=0.66)
    name_entry = CTkEntry(profile_frame, border_width=0,corner_radius=0, font=('Roboto',18,),)
    name_entry.place(relx=0.2, rely=0.66, relwidth=0.3, relheight=0.1)
    name_entry.insert(0,info_username)
    name_entry.configure(state="disabled")

    class_label = CTkLabel(profile_frame,text='Class : ',font=('Roboto',20))
    class_label.place(relx=0.6, rely=0.66)
    class_entry = CTkEntry(profile_frame, border_width=0,corner_radius=0,font=('Roboto',18,),)
    class_entry.place(relx=0.67, rely=0.66, relwidth=0.1, relheight=0.1)
    class_entry.insert(0,info_class)
    class_entry.configure(state="disabled")

    email_label = CTkLabel(profile_frame,text='Email : ',font=('Roboto',20))
    email_label.place(relx=0.1, rely=0.8)
    email_entry = CTkEntry(profile_frame, border_width=0,corner_radius=0,font=('Roboto',18,),)
    email_entry.place(relx=0.2, rely=0.8, relwidth=0.4, relheight=0.1)
    email_entry.insert(0,info_email)
    email_entry.configure(state="disabled")
    
    text_label = CTkLabel(profile_frame,text='Borrowed Books : ',font=('Roboto',20))
    text_label.place(relx=0.05, rely=0.9)


    # Borrowed Books Frame
    tree_frame_borrowedbooks = CTkFrame(main_second_frame_student_win, border_width=0, corner_radius=0)
    tree_frame_borrowedbooks.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    # Create a ttk.Treeview widget inside the tree_frame_borrowedbooks
    scrollbar = CTkScrollbar(tree_frame_borrowedbooks, orientation='vertical')
    tree = ttk.Treeview(tree_frame_borrowedbooks, show="headings", style="Custom.Treeview", )
    tree["columns"] = ("bid","title","subject","author",)
    # Define column headings
    tree.heading("bid", text="BID")
    tree.heading("title", text="Title")
    tree.heading("subject", text="Subject")
    tree.heading("author", text="Author")

    tree.column("bid", width=50, anchor="center",)
    tree.column("title", width=250, anchor="w",)
    tree.column("subject", width=100, anchor="w",)
    tree.column("author", width=100, anchor="w",)

    #######    Inserting Data into the treeview
    sql_borrowed_books = f"""SELECT {books_detail}.bid, {books_detail}.title, {books_detail}.subject, {books_detail}.author
    FROM {books_detail}
    JOIN {book_issue_detail} ON {books_detail}.bid = {book_issue_detail}.bid
    JOIN {student_detail} ON {book_issue_detail}.username = {student_detail}.username
    WHERE studentdetail.username = ?;"""
    cur.execute(sql_borrowed_books, (username,))
    borrowed_books = cur.fetchall()

    if borrowed_books:
        # Remove existing items in the Treeview
        try:
            for item in tree.get_children():
                tree.delete(item)
        except:
            pass
        # Insert data into the Treeview
        for row in borrowed_books:
            tree.insert("", "end", values=row)
            
        # Filling empty space into the Treeview
        for i in range(20 - get_treeview_length(tree)):
            tree.insert("", "end", values=['-','-','-','-'])
    else:
        # Insert data into the Treeview
        for i in range(20):
            tree.insert("", "end", values=['-','-','-','-'])
    
    # Defining a custom style
    style = ttk.Style()
    style.configure("Custom.Treeview", foreground="white", font=("Arial", 10))
    # Applying the style to the TreeView
    tree.tag_configure("Custom.Treeview",)
    # Changing the color of the even rows
    style.configure("evenrow", background="#2b2b2b")
    # Changing the color of the odd rows
    style.configure("oddrow", background="#3a3a3a")
    # Applying tags to all items
    for i in tree.get_children():
        index = tree.index(i)
        if index % 2 == 0:
            tree.tag_configure("evenrow", background="#3a3a3a")
            tree.item(i, tags=("evenrow",))
        else:
            tree.tag_configure("oddrow", background="#2b2b2b")
            tree.item(i, tags=("oddrow",))

    # Changing the color of selected row
    style.map("Treeview",
            foreground=[('selected', 'white')],
            background=[('selected', '#ff3535')])
    # Binding the selection event
    tree.bind("<ButtonRelease-1>", on_select)

    scrollbar.pack(side='right', fill='y')
    scrollbar.configure(command= tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(expand=True, fill="both")

def student_main_win_allbooks():
    # Remove all the widgets from the main_second_frame_student_win
    try:
        for widget in main_second_frame_student_win.winfo_children():
            widget.destroy()
    except:
        pass

    def on_select(event):
        selected_item = tree_student_allbooks.selection()

    tree_frame_allbooks = CTkFrame(main_second_frame_student_win, border_width=0, corner_radius=0)
    tree_frame_allbooks.place(relx=0, rely=0.04, relwidth=1, relheight=0.86)

    # Create a ttk.Treeview widget inside the CTkFrame with a CTkScrollbar
    scrollbar = CTkScrollbar(tree_frame_allbooks, orientation='vertical')
    tree_student_allbooks = ttk.Treeview(tree_frame_allbooks, show="headings", style="Custom.Treeview", )
    tree_student_allbooks["columns"] = ("bid","title","subject","author","status")
    # Define column headings
    tree_student_allbooks.heading("bid", text="BID")
    tree_student_allbooks.heading("title", text="Title")
    tree_student_allbooks.heading("subject", text="Subject")
    tree_student_allbooks.heading("author", text="Author")
    tree_student_allbooks.heading("status", text="Status")

    tree_student_allbooks.column("bid", width=50, anchor="center",)
    tree_student_allbooks.column("title", width=250, anchor="w",)
    tree_student_allbooks.column("subject", width=100, anchor="w",)
    tree_student_allbooks.column("author", width=100, anchor="w",)
    tree_student_allbooks.column("status", width=50, anchor="center",)

    #######    Inserting Data into the treeview
    cur.execute(f"SELECT * FROM {books_detail}")
    data = cur.fetchall()
    # Remove existing items in the Treeview
    try:
        for item in tree_student_allbooks.get_children():
            tree_student_allbooks.delete(item)
    except:
        pass
    # Insert data into the Treeview
    for row in data:
        tree_student_allbooks.insert("", "end", values=row)

    # Defining a custom style
    style = ttk.Style()
    style.configure("Custom.Treeview", foreground="white", font=("Arial", 10))
    # Applying the style to the TreeView
    tree_student_allbooks.tag_configure("Custom.Treeview",)
    # Changing the color of the even rows
    style.configure("evenrow", background="#2b2b2b")
    # Changing the color of the odd rows
    style.configure("oddrow", background="#3a3a3a")
    # Applying tags to all items
    for i in tree_student_allbooks.get_children():
        index = tree_student_allbooks.index(i)
        if index % 2 == 0:
            tree_student_allbooks.tag_configure("evenrow", background="#3a3a3a")
            tree_student_allbooks.item(i, tags=("evenrow",))
        else:
            tree_student_allbooks.tag_configure("oddrow", background="#2b2b2b")
            tree_student_allbooks.item(i, tags=("oddrow",))

    # Changing the color of selected row
    style.map("Treeview",
            foreground=[('selected', 'white')],
            background=[('selected', '#ff3535')])
    # Binding the selection event
    tree_student_allbooks.bind("<ButtonRelease-1>", on_select)

    scrollbar.pack(side='right', fill='y')
    scrollbar.configure(command= tree_student_allbooks.yview)
    tree_student_allbooks.configure(yscrollcommand=scrollbar.set)
    # tree_student_allbooks.place(relx=0, rely=0, relwidth=0.9, relheight=1)
    tree_student_allbooks.pack(expand=True, fill="both")

    ###   Filter Frame   ###
    filter_frame = CTkFrame(main_second_frame_student_win, border_width=0, corner_radius=0)
    filter_frame.place(relx=0, rely=0, relwidth=1, relheight=0.04)
    
    button_filter_frame_down = CTkButton(filter_frame, text='⬇ Filter ⬇',border_width=4,corner_radius=0,border_color='#818181',
        fg_color='#5353ff', hover_color='#0000f0',font=('Roboto',22,),command=None)
    button_filter_frame_down.place(relx=0, rely=0, relwidth=1, relheight=1)


    ###   Borrow Frame   ###
    borrow_frame = CTkFrame(main_second_frame_student_win, border_width=0, corner_radius=0)
    borrow_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

    label_borrow = CTkLabel(borrow_frame,text='Borrow Book : ',font=('Roboto',20))
    label_borrow.place(relx=0.1, rely=0.3)

    entry_borrow_bid = CTkEntry(borrow_frame, placeholder_text=' '*3+'Enter BID', border_width=2,corner_radius=0, font=('Roboto',18,),)
    entry_borrow_bid.place(relx=0.23, rely=0.3, relwidth=0.2, relheight=0.5)

    button_borrow_bid = CTkButton(borrow_frame, text='Borrow',border_width=1,corner_radius=4,border_color='#818181',
        fg_color='#3333ff', hover_color='#0000f0',font=('Roboto',22,),command=None)
    button_borrow_bid.place(relx=0.5, rely=0.3, relwidth=0.1, relheight=0.5)


def student_main_win_return_books():
    # Remove all the widgets from the main_second_frame_student_win
    try:
        for widget in main_second_frame_student_win.winfo_children():
            widget.destroy()
    except:
        pass

#  Side frame button clicks for Students
def profile_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.5)
    all_books_button.place(relx=0,rely=0.5, relwidth=1, relheight=0.2)
    return_books_button.place(relx=0,rely=0.7, relwidth=1, relheight=0.2)
    
    student_main_win_profile(pfp_image=pfp_image, username=username)

def all_books_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.2)
    all_books_button.place(relx=0,rely=0.2, relwidth=1, relheight=0.5)
    return_books_button.place(relx=0,rely=0.7, relwidth=1, relheight=0.2)
    
    student_main_win_allbooks()

def return_books_button_click():
    profile_button.place(relx=0,rely=0, relwidth=1, relheight=0.2)
    all_books_button.place(relx=0,rely=0.2, relwidth=1, relheight=0.2)
    return_books_button.place(relx=0,rely=0.4, relwidth=1, relheight=0.5)
    
    student_main_win_return_books()

def back_button_click():
    # Remove all the widgets from the main_frame
    try:
        for widget in main_frame_student_win.winfo_children():
            widget.destroy()
    except:
        pass
    
    main_win()


main_win()
# student_main_win()

root.mainloop()
