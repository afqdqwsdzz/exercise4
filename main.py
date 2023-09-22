import sqlite3

# Connect to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS Books (
                BookID INTEGER PRIMARY KEY,
                Title TEXT,
                Author TEXT,
                ISBN TEXT,
                Status TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY,
                Name TEXT,
                Email TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                ReservationID INTEGER PRIMARY KEY,
                BookID INTEGER,
                UserID INTEGER,
                ReservationDate TEXT,
                FOREIGN KEY (BookID) REFERENCES Books(BookID),
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )''')

# Function to validate input and determine the search type
def determine_search_type(input_text):
    if input_text.startswith('LB'):
        return 'BookID'
    elif input_text.startswith('LU'):
        return 'UserID'
    elif input_text.startswith('LR'):
        return 'ReservationID'
    else:
        return 'Title'

# Function to add a new book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")

    c.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
              (title, author, isbn, status))

    conn.commit()
    print("Book added successfully!")

# Function to find a book's detail based on BookID
def find_book_details():
    book_id = input("Enter the BookID: ")

    c.execute('''SELECT Books.Title, Books.Status, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))

    result = c.fetchone()

    if result:
        title, status, name, email = result
        print("Title:", title)
        print("Reservation Status:", status)
        if name and email:
            print("Reserved by:", name)
            print("Email:", email)
    else:
        print("Book not found!")

# Function to find a book's reservation status based on BookID, Title, UserID, or ReservationID
def find_reservation_status():
    search_text = input("Enter the BookID, Title, UserID, or ReservationID: ")
    search_type = determine_search_type(search_text)

    if search_type == 'Title':
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.Title = ?''', (search_text,))
    else:
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.BookID = ? OR Users.UserID = ? OR Reservations.ReservationID = ?''',
                  (search_text, search_text, search_text))

    results = c.fetchall()

    if results:
        for result in results:
            book_id, title, status, name, email = result
            print("BookID:", book_id)
            print("Title:", title)
            print("Reservation Status:", status)
            if name and email:
                print("Reserved by:", name)
                print("Email:", email)
            print("---")
    else:
        print("Book not found!")

# Function to find all the books in the database
def find_all_books():
    c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID''')

    results = c.fetchall()

    if results:
        for result in results:
            book_id, title, status, name, email = result
            print("BookID:", book_id)
            print("Title:", title)
            print("Reservation Status:", status)
            if name and email:
                print("Reserved by:", name)
                print("Email:", email)
            print("---")
    else:
        print("No books found!")

# Function to modify/update book details based on BookID
def modify_book_details():
    book_id = input("Enter the BookID: ")

    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = c.fetchone()

    if result:
        print("Current Book Details:")
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])

        choice = input("Choose the field to modify (Title/Author/ISBN/Status): ")

        if choice == "Title":
            new_title = input("Enter the new title: ")
            c.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (new_title, book_id))
        elif choice == "Author":
            new_author = input("Enter the new author: ")
            c.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (new_author, book_id))
        elif choice == "ISBN":
            new_isbn = input("Enter the new ISBN: ")
            c.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (new_isbn, book_id))
        elif choice == "Status":
            new_status = input("Enter the new status: ")
            c.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
        else:
            print("Invalid choice!")

        conn.commit()
        print("Book details updated successfully!")
    else:
        print("Book not found!")

# Function to delete a book based on its BookID
def delete_book():
    book_id = input("Enter the BookID: ")

    c.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = c.fetchone()

    if result:
        c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found!")

# Main program loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all the books")
    print("5. Modify/update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_details()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        modify_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice!")

# Close the database connection
conn.close()