from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import os


#Table Names 
empTable = "empdetail" #Employee Table
stuTable = "studetail" #Student Table
bookTable = "books" # Book Table
issueTable = "issuedetail" #Issue Table

root = Tk()

root.title("Library Management System")
root.state("zoomed")
root.geometry("1920x1080")
root.iconbitmap(r'Icon.ico')
state1='disabled'
state2='disabled'
state3='disabled'
allRoll = [] #List To store all Roll Numbers
allEmpId = [] #List To store all Employee IDs
allBid = [] #List To store all Book IDs
num=0


#Creating Directory for database
path=os.environ["userprofile"]
try:
    os.mkdir(path+"\\Documents\\Library Database")
except FileExistsError:
    pass

con = sqlite3.connect(path+"\\Documents\\Library Database\mydatabase.db")
cur = con.cursor()



#Creating Tables
con.execute("create table if not exists empdetail   (empid varchar(20) primary key,name varchar(30),password varchar(30));")
con.execute("create table if not exists studetail   (rollno varchar(20) primary key,name varchar(30),password varchar(30));")
con.execute("create table if not exists books (bid varchar(20) primary key,title varchar(30),subject varchar(30),author varchar(30),status varchar(30) not null default 'Available');")
con.execute("create table if not exists issuedetail (bid varchar(20) primary key,issueto varchar(30),issueby varchar(30));")



def logout():
    global num,state1,state2,state3

    
    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass



    state1="disabled"
    state2="disabled"
    state3="disabled"
    Menu()
    messagebox.showinfo("Logged out", "You have Successfully logged out")


def gettingDetails():
    
    Id = ent1.get()
    name = ent2.get()
    password = ent3.get()
    role=ent4.get()
    
    if role=="Admin Staff":
        try:
            if (type(int(Id)) == int):
                pass
            else:
                messagebox.showinfo("Invalid Value","Unique ID should be an integer")
                return
        except:
            messagebox.showinfo("Invalid Value","Unique ID should be an integer")
            return


        sql = "insert into "+empTable+" values ('"+Id+"','"+name+"','"+password+"')" 
        try:
            cur.execute(sql)
            con.commit()
            messagebox.showinfo("Success", "Successfully registered")
        except:
            messagebox.showinfo("Error inserting","Cannot add data to Database")

    else:
        try:
            if (type(int(Id)) == int):
                pass
            else:
                messagebox.showinfo("Invalid Value","Unique ID should be an integer")
                return
        except:
            messagebox.showinfo("Invalid Value","Unique ID should be an integer")
            return

    
        sql = "insert into "+stuTable+" values ('"+Id+"','"+name+"','"+password+"')" 
        try:
            cur.execute(sql)
            con.commit()
            messagebox.showinfo("Success", "Successfully registered")
        except:
            messagebox.showinfo("Error inserting","Cannot add data to Database")
        
    
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent4.delete(0, END)


def gettingLoginDetails():

    global role,state1,state2,btn1,btn2,btn3,btn4,btn5,btn6,state3

    
    Id = ent1.get()
    name = ent2.get()
    password = ent3.get()
    role=ent4.get()
    
    if role=='Admin Staff':
        sqlLoginID = "select empid from "+empTable+" where password = '"+password+"'"
        sqlName = "select name from "+empTable+" where password = '"+password+"'"

        try:
            cur.execute(sqlLoginID)
            for i in cur:
                getLoginID = i[0]
            cur.execute(sqlName)
            for i in cur:
                getName = i[0]
            
            if(getLoginID == Id and getName == name):
                messagebox.showinfo("SUCCESS","You have successfully logged in")
                btn1.destroy()
                btn2.destroy()
                btn3.destroy()
                btn4.destroy()
                btn5.destroy()
                btn6.destroy()
                
                state1='normal'
                state2='normal'
                state3='normal'
                Menu()
                
            else:
                messagebox.showerror("Failure","Can't log in, check your credentials")
        except:
            messagebox.showinfo("FAILED","Please check your credentials")
            
    else:
        sqlLoginID = "select rollno from "+stuTable+" where password = '"+password+"'"
        sqlName = "select name from "+stuTable+" where password = '"+password+"'"
        
        try:
            cur.execute(sqlLoginID)
            for i in cur:
                getLoginID = i[0]
            cur.execute(sqlName)
            for i in cur:
                getName = i[0]
            
            if(getLoginID == Id and getName == name):
                btn1.destroy()
                btn2.destroy()
                btn3.destroy()
                btn4.destroy()
                btn5.destroy()
                btn6.destroy()
                
                state2='normal'
                state3='normal'
                Menu()
                messagebox.showinfo("SUCCESS","You have successfully logged in")
            else:
                messagebox.showerror("Failure","Can't log in, check your credentials")
        except:
            messagebox.showinfo("FAILED","Please check your credentials")
        
    
        
    
        
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    
def Menu():

    global state1,state2,btn1,btn2,btn3,btn4,btn5,btn6,photoimage1, photoimage2, photoimage3, photoimage4, photoimage5, photoimage6
    
    photo1 = PhotoImage(file =r"icons\Add book.png")
    photoimage1 = photo1.subsample(3, 3)
    btn1 = Button(moduleFrame,text="Add Book Details",font=("arial",12,'bold'),image=photoimage1,compound = LEFT, command=addBooks, state=state1)
    btn1.place(relx=0,rely=0.17, relwidth=1,relheight=0.12)
    
    photo2 = PhotoImage(file =r"icons\delete book.png")
    photoimage2 = photo2.subsample(3,3)
    btn2 = Button(moduleFrame,text="Delete Book",font=("arial",12,'bold'),image=photoimage2, compound= LEFT, command=delete,state=state1)
    btn2.place(relx=0,rely=0.31, relwidth=1,relheight=0.12)
    
    photo3 = PhotoImage(file =r"icons\view book.png")
    photoimage3 = photo3.subsample(3,3)
    btn3 = Button(moduleFrame,text="View Book List",font=("arial",12,'bold'),image=photoimage3, compound= LEFT, command=View,state=state2)
    btn3.place(relx=0, rely=0.44, relwidth=1,relheight=0.12)
    
    photo4 = PhotoImage(file =r"icons\search book.png")
    photoimage4 = photo4.subsample(3,3)
    btn4 = Button(moduleFrame,text="Search Book",font=("arial",12,'bold'),image=photoimage4, compound= LEFT, command=searchBook,state=state2)
    btn4.place(relx=0,rely=0.58, relwidth=1,relheight=0.12)
    
    photo5 = PhotoImage(file =r"icons\issue book.png")
    photoimage5 = photo5.subsample(3,3)
    btn5 = Button(moduleFrame,text="Issue Book to Student",font=("arial",12,'bold'),image=photoimage5, compound = LEFT, command = issueBook,state=state1)
    btn5.place(relx=0,rely=0.72, relwidth=1,relheight=0.12)
    
    photo6 = PhotoImage(file =r"icons\return book.png")
    photoimage6 = photo6.subsample(3,3)
    btn6 = Button(moduleFrame, text="Return Book",font=("arial",12,'bold'), image=photoimage6, compound = LEFT, command=ReturnBook,state=state1)
    btn6.place(relx=0,rely=0.86, relwidth=1,relheight=0.12)

    logoutBtn=Button(headingFrame, text="LOGOUT", font=('arial',10,'bold'), command=logout, state=state3)
    logoutBtn.place(relx=0.87, rely=0.7, relwidth=0.1)


    
    
############################################################## Add Boook ###################################################################################################################
def bookRegister():

    global en1,en2,en3,en4
    
    bid = en1.get()
    
    title = en2.get()
    title=title.title()
    
    subject = en3.get()
    subject=subject.title()
    
    author = en4.get()
    author=author.title()
    
    
    insertBooks = "insert into "+bookTable+" (bid,title,subject,author) values('"+bid+"','"+title+"','"+subject+"','"+author+"')"

    if bid=="" or title=="" or subject=="" or author=="":
        messagebox.showinfo("Error", "Please fill all the details")

    else:
        try:
            cur.execute(insertBooks)
            con.commit()
            messagebox.showinfo("Sucess","Book added")
        
        except:
            messagebox.showinfo("Error","Can't add data into Database")
    
    
    en1.delete(0, END)
    en2.delete(0, END)
    en3.delete(0, END)
    en4.delete(0, END)

    
def addBooks(): 
    
    global en1,en2,en3,en4,lb1,lb2,lb3,lb4,SubmitBtn,lb,num

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass

    lb=Label(displayFrame,text='Add Book Details',font=("Times New Roman",26,'bold'),bg='white')
    lb.place(relx=0.34,rely=0)

    # Book ID
    lb1 = Label(displayFrame,text="Book ID : ",font=("arial",12,'bold'),bg='white')
    lb1.place(relx=0.05,rely=0.2)
        
    en1 = Entry(displayFrame,font=("arial",12,'bold'),bg='#FFDFA4')
    en1.place(relx=0.3,rely=0.2, relwidth=0.62)
        
    # Title
    lb2 = Label(displayFrame,text="Title : ",font=("arial",12,'bold'),bg='white')
    lb2.place(relx=0.09,rely=0.35)
        
    en2 = Entry(displayFrame,font=("arial",12,'bold'),bg='#FFDFA4')
    en2.place(relx=0.3,rely=0.35, relwidth=0.62)
        
    # Book Subject
    lb3 = Label(displayFrame,text="Subject :",font=("arial",12,'bold'),bg='white')
    lb3.place(relx=0.05,rely=0.5)
        
    en3 = Entry(displayFrame, font=("arial",12,'bold'), bg='#FFDFA4')
    en3.place(relx=0.3,rely=0.5, relwidth=0.62)
        
    # Book Author
    lb4 = Label(displayFrame,text="Author : ",font=("arial",12,'bold'),bg='white')
    lb4.place(relx=0.05,rely=0.65)
        
    en4 = Entry(displayFrame,font=("arial",12,'bold'), bg='#FFDFA4')
    en4.place(relx=0.3,rely=0.65, relwidth=0.62)
        
    #Submit Button
    SubmitBtn = Button(displayFrame,text="SUBMIT",font=("arial",12,'bold'),bg='white',command=bookRegister)
    SubmitBtn.place(relx=0.65,rely=0.8, relwidth=0.18,relheight=0.08)

    num=1


    

################################################### Delete BOOK ############################################################################################################################

def deleteBook():
    
    bid = en1.get()
    
    deleteSql = "delete from "+bookTable+" where bid = '"+bid+"'"

    if bid=='':
        messagebox.showinfo("","Please enter Book ID")

    else:
        try:
            cur.execute(deleteSql)
            con.commit()
            messagebox.showinfo("Success","Book Deleted Successfully") 
        except:
            messagebox.showinfo("Check Credentials","Please check Book ID")
    

    en1.delete(0, END)

    
def delete(): 
    
    global en1, lb1, SubmitBtn,lb,num

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass

    lb = Label(displayFrame,text='Delete Book',font=("Times New Roman",26,'bold'),bg='white')
    lb.place(relx=0.37,rely=0)
        
    # Book ID to Delete
    lb1 = Label(displayFrame,text="Book ID : ",font=("arial",12,'bold'), bg='white')
    lb1.place(relx=0.05,rely=0.5)
        
    en1 = Entry(displayFrame,font=("arial",12,'bold'),bg='#FFDFA4')
    en1.place(relx=0.3,rely=0.5, relwidth=0.62)
    
    #Submit Button
    SubmitBtn = Button(displayFrame,text="SUBMIT", font=("arial",12,'bold'),bg='white',command=deleteBook)
    SubmitBtn.place(relx=0.6,rely=0.75, relwidth=0.18,relheight=0.08)

    num=2



############################################## View Issued Books ###########################################################

def displayissuedbooks():

    global scroll_y,issue_table,num

    
    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()
       

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass

    show= "select issuedetail.bid, books.title, issuedetail.issueto, issuedetail.issueby  from " +bookTable+ " inner join issuedetail on issuedetail.bid=books.bid"

    scroll_y=Scrollbar(displayFrame,orient=VERTICAL)
    issue_table=ttk.Treeview(displayFrame,columns=("bid","bname","issuedto","issueby"),yscrollcommand=scroll_y.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_y.config(command=issue_table.yview)
    issue_table.heading("bid",text="Book ID")
    issue_table.heading("bname",text="Title")
    issue_table.heading("issuedto",text="Issued To")
    issue_table.heading("issueby",text="Issued By")
    issue_table["show"]="headings"
    issue_table.column("bid",width=50)
    issue_table.column("bname",width=50)
    issue_table.column("issuedto",width=50)
    issue_table.column("issueby",width=50)
    issue_table.pack(fill=BOTH,expand=1)

    try:
        cur.execute(show)
        con.commit()
        for i in cur:
            issue_table.insert('',END,values=i)

    except:
        messagebox.showinfo("Error","Failed to fetch data")

    num=4

    

############################################### Issue BOOK #################################################################################################################################

def issue():
    
    #global lb1,lb2,lb3,en1,en2,en3,status,scroll_y,issue_table,num
    
    bid = en1.get()
    issueto = en2.get()
    issueby = en3.get()


    extractBid = "select bid from "+bookTable
    try:
        cur.execute(extractBid)
        con.commit()
        for i in cur:
            allBid.append(i[0])
        
        if bid in allBid:
            checkAvail = "select status from "+bookTable+" where bid = '"+bid+"'"
            cur.execute(checkAvail)
            con.commit()
            for i in cur:
                check = i[0]
                
            if check == 'Available':
                status = True
            else:
                status = False
        else:
            messagebox.showinfo("Error","Book ID not present")
    except:
        messagebox.showinfo("Error","Can't fetch Book IDs")
    
    extractRollno = "select rollno from "+stuTable
    try:
        cur.execute(extractRollno)
        con.commit()
        for i in cur:
            allRoll.append(i[0])
        
        if issueto in allRoll:
            pass
        else:
            messagebox.showinfo("Error","Roll No not present")
    except:
        messagebox.showinfo("Error","Can't fetch Roll No")
        
    extractEmpID = "select empid from "+empTable
    try:
        cur.execute(extractEmpID)
        con.commit()
        for i in cur:
            allEmpId.append(i[0])
        
        if issueby in allEmpId:
            pass
        else:
            messagebox.showinfo("Error","Emp ID not present")
    except:
        messagebox.showinfo("Error","Can't fetch Emp IDs")
    
    
    
    

    issueSql = "insert into "+issueTable+" values ('"+bid+"','"+issueto+"','"+issueby+"')"
    
    
    updateStatus = "update "+bookTable+" set status = 'issued' where bid = '"+bid+"'"
    try:
        if bid in allBid and issueto in allRoll and issueby in allEmpId and status == True:
            cur.execute(issueSql)
            con.commit()
            cur.execute(updateStatus)
            con.commit()
            messagebox.showinfo("Success"," Issued Book successfully") 

            
        else:
            allBid.clear()
            allEmpId.clear()
            allRoll.clear()
            return
        
        
    except:
        messagebox.showinfo("Search Error","The value entered is wrong, Try again")
    
    en1.delete(0,END)
    en2.delete(0,END)
    en3.delete(0,END)
    
    allBid.clear()
    allEmpId.clear()
    allRoll.clear()
    
    

    
def issueBook(): 
    
    global en1,en2,en3,issueBtn,lb1,lb2,lb3,en1,en2,en3,lb,num,issuedBooks

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass
   
    lb = Label(displayFrame,text="Issue Book to Student", font=('Times New Roman',26,'bold'), bg='white')
    lb.place(relx=0.27,rely=0)
    # Book ID
    lb1 = Label(displayFrame,text="Book ID : ",font=('arial', 12,'bold'), bg='white')
    lb1.place(relx=0.05,rely=0.2)
        
    en1 = Entry(displayFrame,font=('arial', 12,'bold'),bg='#FFDFA4')
    en1.place(relx=0.4,rely=0.2, relwidth=0.55)
    
    # Issued To Roll Number 
    lb2 = Label(displayFrame,text="Issued To(Student Unique ID) : ",font=('arial', 12,'bold'),bg='white')
    lb2.place(relx=0.05,rely=0.4)
        
    en2 = Entry(displayFrame,font=('arial', 12,'bold'),bg='#FFDFA4')
    en2.place(relx=0.4,rely=0.4, relwidth=0.55)
    
    # Issued By Employee Number
    lb3 = Label(displayFrame,text="Issued By(Admin Unique ID) : ",font=('arial', 12,'bold'), bg='white')
    lb3.place(relx=0.05,rely=0.6)
        
    en3 = Entry(displayFrame,font=('arial', 12,'bold'),bg='#FFDFA4')
    en3.place(relx=0.4,rely=0.6, relwidth=0.55)
    
    #Issue Button
    issueBtn = Button(displayFrame,text="Issue",bg='white',font=("arial",12,'bold'), command=issue)
    issueBtn.place(relx=0.7,rely=0.75, relwidth=0.18,relheight=0.08)
    
    #View Issued Books
    issuedBooks= Button(displayFrame,text="View Issued Books",bg='white',font=("arial",12,'bold'), command=displayissuedbooks)
    issuedBooks.place(relx=0.15,rely=0.75, relwidth=0.28,relheight=0.08)

    

    num=3


############################################################# Return Book ######################################################################################################################################
def Return():
    
    global ReturnBtn,labelFrame,lb1,en1,en2,status
    
    bookid = en1.get()
    Returnby = en2.get()
    
   
    
    extractBid = "select bid from "+bookTable
    try:
        cur.execute(extractBid)
        con.commit()
        for i in cur:
            allBid.append(i[0])
        
        if bookid in allBid:
            checkAvail = "select status from "+bookTable+" where bid = '"+bookid+"'"
            cur.execute(checkAvail)
            con.commit()
            for i in cur:
                check = i[0]
                
            if check == 'Available':
                status = True
            else:
                status = False
        else:
            messagebox.showinfo("Error","Book ID not present in  database")
    except:
        messagebox.showinfo("Error","Can't fetch Book IDs")
    
    extractRollno = "select rollno from "+stuTable
    try:
        cur.execute(extractRollno)
        con.commit()
        for i in cur:
            allRoll.append(i[0])
        
        if Returnby in allRoll:
            pass
        else:
            messagebox.showinfo("Error","Student ID not present")
    except:
        messagebox.showinfo("Error","Can't fetch Student ID")
        
    
    
    
    ReturnSql = "delete from "+issueTable+" where bid="+bookid
    
    updateStatus = "update "+bookTable+" set status ='Available' where bid="+bookid
    try:
        if bookid in allBid and Returnby in allRoll  and status == False:
            cur.execute(ReturnSql)
            con.commit()
            cur.execute(updateStatus)
            con.commit()
            messagebox.showinfo("Successs","Book returned successfully")
            
            
        else:
            allBid.clear()
            allRoll.clear()
            
        
    except:
        messagebox.showinfo("Search Error","The value entered is wrong, Try again")
        
    
    en1.delete(0, END)
    en2.delete(0, END)
    
    allBid.clear()
    allRoll.clear()
    
    

    
def ReturnBook(): 
    
    global en1,en2,ReturnBtn,lb1,lb2,headingLabel,num

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass
        
        
    headingLabel = Label(displayFrame, text="RETURN BOOK",font=('Times New Roman',26,'bold'),bg='white')
    headingLabel.place(relx=0.35,rely=0.05)   
        
    # Book ID
    lb1 = Label(displayFrame,text="Book ID : ",font=('arial',12,'bold'),bg='white')
    lb1.place(relx=0.05,rely=0.3)
        
    en1 = Entry(displayFrame,font=('arial',12,'bold'),bg='#FFDFA4')
    en1.place(relx=0.3,rely=0.3, relwidth=0.62)
    
    
    # Student ID
    lb2 = Label(displayFrame,text="Student ID : ",font=('arial',12,'bold'),bg='white')
    lb2.place(relx=0.05,rely=0.6)
        
    en2 = Entry(displayFrame,font=('arial',12,'bold'),bg='#FFDFA4')
    en2.place(relx=0.3,rely=0.6, relwidth=0.62)
    
    #Return Button
    ReturnBtn = Button(displayFrame,text="Return",font=('arial',12,'bold'),bg='white',command=Return)
    ReturnBtn.place(relx=0.7,rely=0.75, relwidth=0.18,relheight=0.08)

    

    num=5



########################################## Search Book #####################################################################################################################################
    
def search():
    
    global SearchBtn,labelFrame,lb1,en1,scroll_y, books_table,num
    
    sub = en1.get()
    sub=sub.title()

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass
    
   
    
    scroll_y=Scrollbar(displayFrame,orient=VERTICAL)
    books_table=ttk.Treeview(displayFrame,columns=("bid","title","subject","author","status"),yscrollcommand=scroll_y.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_y.config(command=books_table.yview)
    books_table.heading("bid",text="Book ID")
    books_table.heading("title",text="Title")
    books_table.heading("subject",text="Subject")
    books_table.heading("author",text="Author")
    books_table.heading("status",text="Status")
    books_table["show"]="headings"
    books_table.column("bid",width=50)
    books_table.column("title",width=50)
    books_table.column("subject",width=50)
    books_table.column("author",width=50)
    books_table.column("status",width=50)
    books_table.pack(fill=BOTH,expand=1)

    num=7
    
    searchSql = "select * from "+bookTable+" where subject = '"+sub+"'"
    try:
        cur.execute(searchSql)
        con.commit()
        rows=cur.fetchall()
        for row in rows:
            books_table.insert('',END,values=row)
    except:
        messagebox.showinfo("Search Error","The value entered is wrong, Try again")
    
    

    
def searchBook(): 
    
    global en1,SearchBtn,lb1, headingLabel,num

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass
        
    headingLabel = Label(displayFrame, text="Search Book",font=("Times New Roman",26,'bold'), bg='white')
    headingLabel.place(relx=0.35,rely=0.05)   
        
    # Book ID to Delete
    lb1 = Label(displayFrame,text="Enter Subject : ",font=("arial",12,'bold'), bg='white')
    lb1.place(relx=0.05,rely=0.4)
        
    en1 = Entry(displayFrame,font=("arial",12,'bold'),bg='#FFDFA4')
    en1.place(relx=0.3,rely=0.4, relwidth=0.62)
    
    #Submit Button
    SearchBtn = Button(displayFrame,text="Search",font=('arial',12,'bold'),bg='white',command=search)
    SearchBtn.place(relx=0.66,rely=0.55, relwidth=0.18,relheight=0.08)

    

    num=6
    
  
###################################################### View Books ############################################
def View():
    global scroll_y, books_table,num,headingLabel

    if num==1:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        lb4.destroy()
        en3.destroy()
        en4.destroy()
        SubmitBtn.destroy()

    elif num==2:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        SubmitBtn.destroy()

    elif num==3:
        lb.destroy()
        lb1.destroy()
        en1.destroy()
        lb2.destroy()
        en2.destroy()
        lb3.destroy()
        en3.destroy()
        issueBtn.destroy()
        issuedBooks.destroy()

    elif num==4:
        scroll_y.destroy()
        issue_table.destroy()

    elif num==5:
        en1.destroy()
        en2.destroy()
        ReturnBtn.destroy()
        lb1.destroy()
        lb2.destroy()
        headingLabel.destroy()

    elif num==6:
        en1.destroy()
        lb1.destroy()
        headingLabel.destroy()
        SearchBtn.destroy()

    elif num==7 or num==8:
        scroll_y.destroy()
        books_table.destroy()

    else:
        pass
        
    
    scroll_y=Scrollbar(displayFrame,orient=VERTICAL)
    books_table=ttk.Treeview(displayFrame,columns=("bid","title","subject","author","status"),yscrollcommand=scroll_y.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_y.config(command=books_table.yview)
    books_table.heading("bid",text="Book ID")
    books_table.heading("title",text="Title")
    books_table.heading("subject",text="Subject")
    books_table.heading("author",text="Author")
    books_table.heading("status",text="Status")
    books_table["show"]="headings"
    books_table.column("bid",width=50)
    books_table.column("title",width=50)
    books_table.column("subject",width=50)
    books_table.column("author",width=50)
    books_table.column("status",width=50)
    books_table.pack(fill=BOTH,expand=1)

    num=8


    getBooks = "select * from "+bookTable
    try:
        cur.execute(getBooks)
        con.commit()
        rows=cur.fetchall()
        for row in rows:
            books_table.insert('',END,values=row)
    except:
        messagebox.showinfo("Error","Can't fetch data from database")


    
################################## Frames #########################################################################
       
headingFrame = Frame(root,bd=20, relief=RIDGE)
headingFrame.place(relx=0,rely=0,relwidth=1,relheight=0.2)

heading=Label(headingFrame,font=('Times New ROman', 40, 'bold'), text="Library Management System")
heading.place(relx=0, rely=0.2)

moduleFrame = Frame(root,bd=20, relief=RIDGE)
moduleFrame.place(relx=0,rely=0.2,relwidth=0.2,relheight=0.8)

headingLabel = Label(moduleFrame, text="MENU",font=("Times New Roman",26,'bold'))
headingLabel.place(relx=0,rely=0, relwidth=1, relheight=0.15)

dFrame= Frame(root,bd=20, relief=RIDGE)
dFrame.place(relx=0.2,rely=0.2,relwidth=0.8,relheight=0.8)

displayFrame=Frame(dFrame, bd=10, relief=SOLID, bg='white')
displayFrame.place(relx=0.2,rely=0.05, relwidth=0.6, relheight=0.9)

########################################### Interface for login and registration ############################################

# ID
lb1=Label(headingFrame,text='Unique ID:',font=('arial', 12,'bold'))
lb1.place(relx=0.63, rely=0.01)

ent1=Entry(headingFrame, font=('arial', 12,'bold'))
ent1.place(relx=0.7, rely=0.01, relwidth=0.15)

#Name
lb2=Label(headingFrame,text='Name:',font=('arial', 12,'bold'))
lb2.place(relx=0.63, rely=0.25)

ent2=Entry(headingFrame, font=('arial', 12,'bold'))
ent2.place(relx=0.7, rely=0.25, relwidth=0.15)

#Password
lb3=Label(headingFrame,text='Password:',font=('arial', 12,'bold'))
lb3.place(relx=0.63, rely=0.48)

ent3=Entry(headingFrame, font=('arial', 12,'bold'),show="\u2022")
ent3.place(relx=0.7, rely=0.48, relwidth=0.15)

#Role Combobox
lb4=Label(headingFrame,text='Role:',font=('arial', 12,'bold'))
lb4.place(relx=0.63, rely=0.73)

ent4=ttk.Combobox(headingFrame, font=('arial', 12, 'bold'), state='readonly', width=23)
ent4['value']=('','Admin Staff', 'Student')
ent4.current(0)
ent4.place(relx=0.7,rely=0.73,relwidth=0.15)

loginBtn = Button(headingFrame,text="LOGIN", font=("arial",10,'bold'),command=gettingLoginDetails)
loginBtn.place(relx=0.87,rely=0.4, relwidth=0.1)

regBtn=Button(headingFrame,text="REGISTER", font=("arial",10,'bold'),command=gettingDetails)
regBtn.place(relx=0.87,rely=0.1, relwidth=0.1)



Menu()
root.mainloop()




