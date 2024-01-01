## Library-Management-System

# Overview
The Library Management System (LMS) is a comprehensive software solution designed to efficiently manage library 
operations, catering to both students and administrators. The system provides a user-friendly graphical interface for 
students to register, log in, borrow, and return books. Administrators, on the other hand, can oversee library 
statistics, manage students, and control the library's book inventory.

# ->  Table of Contents
1.  Introduction
2.  Features
3.  Requirements
4.  Installation
5.  Usage
     >  Student Interface
     >  Admin Interface
6.  Database Structure
7.  Modules Used
8.  File Structure
9.  Contribution

#  1.  Introduction
The Library Management System is a Python-based application developed to streamline library processes. It consists of 
two main interfaces: one for students and another for administrators. Students can register, log in, borrow, and 
return books, while administrators can manage library statistics, oversee book inventory, and handle student 
information.

#  2.  Features<a name="features"></a>
# For Students:
> User registration and login.
> View profile information.
> Display borrowed books.
> Browse and search for available books.
> Borrow and return books.

# For Admins:
> Admin registration and login.
> View profile information and library statistics.
> Manage student information.
> Browse and search for all books in the library.
> Add, remove, and update books in the library.

#  3.  Requirements
> `Python 3.11`
> `customtkinter` module
> `time` module
> `PIL` (Python Imaging Library) module
> `sqlite3` module
> `os` module
> `hashlib` module
> `random` module

#  4.  Installation<a name="installation"></a>
1. Run packageinstaller.py to install the necessary packages.
2. Execute lib_sys.py to start the Library Management System.

#  5.  Usage<a name="usage"></a>
# > Student Interface<a name="student-interface"></a>
1. Click the "Student" button.
2. Register with User ID, password, class, and email.
3. Login with the registered username and password.
4. View profile, borrowed books, and available books.
5. Borrow and return books as needed.

# > Admin Interface<a name="admin-interface"></a>
1. Click the "Admin" button.
2. Register with username, password, email, and unique library ID.
3. Login with the registered username and password.
4. View profile, library statistics, and manage students.
5. Browse, search, and manage all books in the library.

#  6.  Database Structure
The system uses an SQLite database named mydatabase.db with the following tables:

> admindetail:
admname
password
email
pfp (profile picture)

>studentdetail:
username
password
class
email
pfp (profile picture)

> booksdetail:
bid (Book ID)
title
subject
author
status (available or unavailable)

> bookissuedetail:
bid (foreign key connected with booksdetail)
username (foreign key connected with studentdetail

#  7.  Modules Used
`customtkinter`: Customized graphical user interface.
`time`: Time-related functions.
`PIL`: Python Imaging Library for image processing.
`sqlite3`: SQLite database management.
`os`: Operating system interaction.
`hashlib`: Hashing passwords for security.
`random`: Generating random values.

#  8.  File Structure
`lib_sys.py`: Main program file.
`packageinstaller.py`: Installs required packages.
`pfp/`: Folder containing profile pictures for students.
`admpfp/`: Folder containing profile pictures for administrators.
`Items/`: Folder containing icons, `booksdata.txt`, and `about.txt`.
`booksdata.txt`: Initial data for books.
`about.txt`: Information about the library management system.

#  9.  Contribution
The Library Management System project was developed by 
Saurav Kumar,
Raj Verma,
Pallav,
Zeeshan
as a school project.

