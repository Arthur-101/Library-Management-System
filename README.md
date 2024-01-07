# Library-Management-System 

## Overview
The Library Management System (LMS) is a comprehensive software solution designed to efficiently manage library 
operations, catering to both students and administrators. The system provides a user-friendly graphical interface for 
students to register, log in, borrow, and return books. Administrators, on the other hand, can oversee library 
statistics, manage students, and control the library's book inventory.

## ->  Table of Contents
1.  Introduction
2.  Features
3.  Requirements
4.  Installation
5.  Usage
  *  Student Interface
  *  Admin Interface
6.  Database Structure
7.  Modules Used
8.  File Structure
9.  Contribution

##  1.  Introduction
The Library Management System is a Python-based application developed to streamline library processes. It consists of 
two main interfaces: one for students and another for administrators. Students can register, log in, borrow, and 
return books, while administrators can manage library statistics, oversee book inventory, and handle student 
information.

##  2.  Features
### For Students:
*  User registration and login.
*  View profile information.
*  Display borrowed books.
*  Browse and search for available books.
*  Borrow and return books.

### For Admins:
*  Admin registration and login.
*  View profile information and library statistics.
*  Manage student information.
*  Browse and search for all books in the library.
*  Add, remove, and update books in the library.

##  3.  Requirements
1. **`Python 3.11`**
2. *`customtkinter`* module
3. *`time`* module
4. *`PIL`* (Python Imaging Library) module
5. *`sqlite3`* module
6. *`os`* module
7. *`hashlib`* module
8. *`random`* module

##  4.  Installation
1. Run packageinstaller.py to install the necessary packages.
2. Execute lib_sys.py to start the Library Management System.

##  5.  Usage
### > Student Interface
* Click the "Student" button.
* Register with User ID, password, class, and email.
* Login with the registered username and password.
* View profile, borrowed books, and available books.
* Borrow and return books as needed.

### > Admin Interface
* Click the "Admin" button.
* Register with username, password, email, and unique library ID.
* Login with the registered username and password.
* View profile, library statistics, and manage students.
* Browse, search, and manage all books in the library.

##  6.  Database Structure
The system uses an SQLite database named mydatabase.db with the following tables:

### admindetail:
- admname,
- password,
- email,
- pfp 

### studentdetail:
- username,
- password,
- class,
- email,
- pfp 

### booksdetail:
- bid,
- title,
- subject,
- author,
- status 

### bookissuedetail:
- bid (foreign key connected with booksdetail),
- username (foreign key connected with studentdetail)

##  7.  Modules Used
1. `customtkinter`: Customized graphical user interface.
2. `time`: Time-related functions.
3. `PIL`: Python Imaging Library for image processing.
4. `sqlite3`: SQLite database management.
5. `os`: Operating system interaction.
6. `hashlib`: Hashing passwords for security.
7. `random`: Generating random values.

##  8.  File Structure
1. `Main.py`: Main program file.
2. `packageinstaller.py`: Installs required packages.
3. `pfp/`: Folder containing profile pictures for students.
4. `admpfp/`: Folder containing profile pictures for administrators.
5. `Items/`: Folder containing icons, `booksdata.txt`, and `about.txt`.
6. `booksdata.txt`: Initial data for books.
7. `about.txt`: Information about the library management system.

##  9.  Contribution
The Library Management System project was developed by 
[Saurav Kumar]
as a school project.

