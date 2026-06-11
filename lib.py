import sqlite3
con=sqlite3.connect("project.db")
c=con.cursor()

c.execute("PRAGMA foreign_keys = ON")

c.execute("""CREATE TABLE IF NOT EXISTS user(username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        usertype TEXT NOT NULL);""")
c.execute("""CREATE TABLE IF NOT EXISTS books 
        (book_id INTEGER PRIMARY KEY,
        title TEXT);""")
c.execute("""CREATE TABLE IF NOT EXISTS issue(issue_id INTEGER PRIMARY KEY,
        book_id INTEGER,username TEXT,FOREIGN KEY(book_id) REFERENCES books(book_id)ON DELETE CASCADE,
        FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE);""")
con.commit()
def available_books():
    c.execute("""
    SELECT * FROM books
    WHERE book_id NOT IN (
        SELECT book_id FROM issue
    )
    """)

    rows = c.fetchall()

    if rows:
        print("Available Books")
        print("BookID \tTitle")
        print("--------------------------")

        for row in rows:
            print(f"{row[0]}\t{row[1]}")
    else:
        print("No Books Available")
def add_book():
    try:
        bid=int(input("enter book_id"))
        name=input("enter title")
        c.execute("INSERT INTO books(book_id,title) VALUES(?,?)",(bid,name))
        con.commit()
        print("BOOK ADDED")
    except sqlite3.IntegrityError:
        print("BOOK ID ALREADY EXISTS")
def view_book():
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    if rows:
        print("BookID \tTitle")
        print("---------------------")
        for row in rows:
            print(row[0], "\t", row[1])
            print("---------------------")

    else:
        print("Empty Book Library")


def update_book():
    bid = int(input("Enter Book ID: "))
    n = input("Enter New Title: ")

    c.execute(
        "UPDATE books SET title=? WHERE book_id=?",
        (n, bid)
    )
    con.commit()

    if c.rowcount > 0:
        print("BOOK UPDATED")
    else:
        print("BOOK NOT FOUND")
def delete_book():
    view_book()
    bid = int(input("Enter Book ID:\n"))
    c.execute("DELETE FROM books WHERE book_id=?",(bid,))
    con.commit()
    if c.rowcount > 0:
        print("Book Deleted Successfully")
    else:
        print("Book Not Found")


def view_issue():
    c.execute("""
    SELECT issue.username, books.book_id, books.title
    FROM issue
    JOIN books ON issue.book_id = books.book_id
    """)

    rows = c.fetchall()

    if rows:
        print("Username\tBookID \t Book Name")
        print("------------------------------------------")

        for i in rows:
            print(f"{i[0]}\t\t{i[1]}\t{i[2]}")
    else:
        print("No Books Issued")
def issue_book(username):
    available_books()
    book_id = int(input("Enter BookID: "))
    c.execute(
        "SELECT * FROM issue WHERE book_id=?",
        (book_id,)
    )
    if c.fetchone():
        print("BOOK ALREADY ISSUED")
        return
    try:
        c.execute(
            "INSERT INTO issue(book_id,username) VALUES(?,?)",
            (book_id, username)
        )
        con.commit()
        print("BOOK ISSUED")
    except sqlite3.IntegrityError:
        print("INVALID BOOK ID")
def return_book(username):
    bid = int(input("Enter Book ID: "))
    c.execute(
        "DELETE FROM issue WHERE book_id=? AND username=?",
        (bid, username)
    )
    con.commit()
    if c.rowcount > 0:
        print("BOOK RETURNED")
    else:
        print("NO SUCH ISSUED BOOK")
def view_my_issue_history(username):
    c.execute("""
    SELECT issue.issue_id, books.book_id, books.title
    FROM issue
    JOIN books ON issue.book_id = books.book_id
    WHERE issue.username=?
    """, (username,))
    rows = c.fetchall()
    if rows:
        print("IssueID\tBookID\tTitle")
        print("-------------------------------------")
        for row in rows:
            print(f"{row[0]}\t\t{row[1]}\t{row[2]}")
    else:
        print("NO ISSUE HISTORY")
def staff():
    while True:
        print("1.Add Book")
        print("2.View Books")
        print("3.Update Books")
        print("4.Remove Book")
        print("5.View Issued Book")
        print("6.Logout")
        staff_choice=int(input("Enter Choice(1/2/3/4/5/6)"))
        if staff_choice==1:
            add_book()
        elif staff_choice==2:
            view_book()
        elif staff_choice==3:
            update_book()
        elif staff_choice==4:
            delete_book()
        elif staff_choice==5:
            view_issue()
        elif staff_choice==6:
            break
        else:
            print("Invalid Choice")
def student(username):
    while True:
        print("STUDENT MENU")
        print("1.View Books")
        print("2.Issue Book")
        print("3.Return Book")
        print("4.View Book Issue History")
        print("5.Logout")

        st = int(input("Enter Choice(1/2/3/4/5): "))

        if st == 1:
            view_book()
        elif st == 2:
            issue_book(username)
        elif st == 3:
            return_book(username)
        elif st == 4:
            view_my_issue_history(username)
        elif st == 5:
            break
def reg():
    user=input("Enter Username:\n")
    pa=input("Enter Password:\n")
    while True:
        t = input("Enter UserType(STAFF/STUDENT): ").lower()

        if t in ["staff", "student"]:
            break

        print("Invalid UserType")

    try:
        c.execute(
            "INSERT INTO user(username,password,usertype) VALUES(?,?,?)",
            (user, pa, t)
        )

        con.commit()
        print("Registration Successful")

    except sqlite3.IntegrityError:
        print("Username Already Exists")

def login():
    user=input("Enter Username:\n")
    pa=input("Enter Password:\n")

    c.execute(
        "SELECT * FROM user WHERE username=? AND password=?",
        (user,pa)
    )

    v=c.fetchone()

    if v:
        print("Login Successful\n")
        print("Welcome",v[0])

        if v[2]=="staff":
            print("STAFF ACCESS")
            staff()

        elif v[2]=="student":
            print("STUDENT ACCESS")
            student(v[0])

    else:
        print("Invalid Username or Password")

while True:
    print("LIBRARY MANAGEMENT SYSTEM")
    print("1.Register ")
    print("2.Login ")
    print("3.Exit ")
    x=int(input("Enter Your Choice(1/2/3):"))
    if x==1:
        reg()
    elif x==2:
        login()
    elif x==3:
        print("\n-----Exiting---------\n")
        break
    else :
        print("Invalid Command")