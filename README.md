# # Library Management System

## Overview

This is a simple Library Management System developed using Python and SQLite. The system allows staff members to manage books and students to issue and return books through a menu-driven interface.

## Features

### User Management

* User Registration
* User Login
* Role-Based Access (Staff / Student)

### Staff Functions

* Add Book
* View Books
* Update Book Details
* Delete Book
* View Issued Books

### Student Functions

* View Books
* Issue Book
* Return Book
* View Issue History

## Database Tables

### User Table

Stores user information.

| Field    | Type               |
| -------- | ------------------ |
| username | TEXT (Primary Key) |
| password | TEXT               |
| usertype | TEXT               |

### Books Table

Stores book details.

| Field   | Type                  |
| ------- | --------------------- |
| book_id | INTEGER (Primary Key) |
| title   | TEXT                  |

### Issue Table

Stores issued book records.

| Field    | Type                  |
| -------- | --------------------- |
| issue_id | INTEGER (Primary Key) |
| book_id  | INTEGER (Foreign Key) |
| username | TEXT (Foreign Key)    |

## Technologies Used

* Python
* SQLite3

## Database Features

* Foreign Key Constraints
* ON DELETE CASCADE
* Data Persistence using SQLite

## How to Run

1. Install Python.
2. Save the program as `lib.py`.
3. Open Terminal or Command Prompt.
4. Navigate to the project folder.
5. Run:

```bash
python lib.py
```

## Menu Structure

### Main Menu

1. Register
2. Login
3. Exit

### Staff Menu

1. Add Book
2. View Books
3. Update Book
4. Remove Book
5. View Issued Books
6. Logout

### Student Menu

1. View Books
2. Issue Book
3. Return Book
4. View Book Issue History
5. Logout

## Future Enhancements

* Due Date Management
* Fine Calculation for Late Returns
* Available Books View
* Search Books
* Book Categories

## Author

Arjun S Murali
