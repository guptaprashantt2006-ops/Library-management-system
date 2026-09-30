import mysql.connector
from mysql.connector import Error
from datetime import date



# connecting my sql databse with python


def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

        if connection.is_connected():
            print("Database server connected successfully.")
            return connection

    except Error as e:
        print("Error connecting to MySQL:", e)
        return None
# Creating database with the tables

def setup_database(connection):
    cursor = connection.cursor()

    try:
        # for creating the database

        cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
        cursor.execute("USE library_db")

        # Create books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(150) NOT NULL,
                author VARCHAR(100) NOT NULL,
                quantity INT NOT NULL
            )
        """)

        # Create members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15)
            )
        """)

        # Create issued_books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
                issue_id INT PRIMARY KEY AUTO_INCREMENT,
                book_id INT NOT NULL,
                member_id INT NOT NULL,
                issue_date DATE NOT NULL,
                return_date DATE DEFAULT NULL,

                FOREIGN KEY (book_id)
                    REFERENCES books(book_id)
                    ON DELETE CASCADE,

                FOREIGN KEY (member_id)
                    REFERENCES members(member_id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()

        print("Library database and tables are ready.")

    except Error as e:
        print("Error setting up database:", e)

    finally:
        cursor.close()

# Adding the books

def add_book(connection):
    cursor = connection.cursor()

    print("\n========== ADD BOOK ==========")

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()

    if title == "" or author == "":
        print("Title and author cannot be empty.")
        cursor.close()
        return

    try:
        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            cursor.close()
            return

        query = """
            INSERT INTO books (title, author, quantity)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (title, author, quantity))
        connection.commit()

        print("Book added successfully.")

    except ValueError:
        print("Please enter a valid number for quantity.")

    except Error as e:
        print("Error adding book:", e)

    finally:
        cursor.close()



# VIEW ALL BOOKS


def view_books(connection):
    cursor = connection.cursor()

    print("\n================ ALL BOOKS ================")

    try:
        cursor.execute("""
            SELECT book_id, title, author, quantity
            FROM books
            ORDER BY book_id
        """)

        books = cursor.fetchall()

        if not books:
            print("No books found.")
            return

        print("-" * 75)
        print(f"{'ID':<5}{'Title':<30}{'Author':<25}{'Quantity':<10}")
        print("-" * 75)

        for book in books:
            book_id, title, author, quantity = book

            print(
                f"{book_id:<5}"
                f"{title[:28]:<30}"
                f"{author[:23]:<25}"
                f"{quantity:<10}"
            )

        print("-" * 75)

    except Error as e:
        print("Error displaying books:", e)

    finally:
        cursor.close()



# SEARCH BOOK

def search_book(connection):
    cursor = connection.cursor()

    print("\n========== SEARCH BOOK ==========")

    search = input("Enter title or author to search: ").strip()

    if search == "":
        print("Search value cannot be empty.")
        cursor.close()
        return

    try:
        query = """
            SELECT book_id, title, author, quantity
            FROM books
            WHERE title LIKE %s OR author LIKE %s
        """

        search_value = "%" + search + "%"

        cursor.execute(query, (search_value, search_value))

        books = cursor.fetchall()

        if not books:
            print("No matching books found.")
            return

        print("\nSearch Results")
        print("-" * 75)
        print(f"{'ID':<5}{'Title':<30}{'Author':<25}{'Quantity':<10}")
        print("-" * 75)

        for book in books:
            book_id, title, author, quantity = book

            print(
                f"{book_id:<5}"
                f"{title[:28]:<30}"
                f"{author[:23]:<25}"
                f"{quantity:<10}"
            )

        print("-" * 75)

    except Error as e:
        print("Error searching book:", e)

    finally:
        cursor.close()



# DELETE BOOK

def delete_book(connection):
    cursor = connection.cursor()

    print("\n========== DELETE BOOK ==========")

    try:
        book_id = int(input("Enter Book ID to delete: "))

        # Check if book exists
        cursor.execute(
            "SELECT title FROM books WHERE book_id = %s",
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            print("Book not found.")
            return

        # Check if currently issued
        cursor.execute("""
            SELECT issue_id
            FROM issued_books
            WHERE book_id = %s AND return_date IS NULL
        """, (book_id,))

        issued = cursor.fetchone()

        if issued:
            print("This book is currently issued and cannot be deleted.")
            return

        confirm = input(
            f"Are you sure you want to delete '{book[0]}'? (y/n): "
        ).lower()

        if confirm == "y":
            cursor.execute(
                "DELETE FROM books WHERE book_id = %s",
                (book_id,)
            )

            connection.commit()

            print("Book deleted successfully.")

        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid Book ID.")

    except Error as e:
        print("Error deleting book:", e)

    finally:
        cursor.close()



# ADD MEMBER


def add_member(connection):
    cursor = connection.cursor()

    print("\n========== REGISTER MEMBER ==========")

    name = input("Enter member name: ").strip()
    phone = input("Enter phone number: ").strip()

    if name == "":
        print("Member name cannot be empty.")
        cursor.close()
        return

    try:
        query = """
            INSERT INTO members (name, phone)
            VALUES (%s, %s)
        """

        cursor.execute(query, (name, phone))
        connection.commit()

        print("Member registered successfully.")
        print("Member ID:", cursor.lastrowid)

    except Error as e:
        print("Error registering member:", e)

    finally:
        cursor.close()



# VIEW MEMBERS


def view_members(connection):
    cursor = connection.cursor()

    print("\n================ MEMBERS ================")

    try:
        cursor.execute("""
            SELECT member_id, name, phone
            FROM members
            ORDER BY member_id
        """)

        members = cursor.fetchall()

        if not members:
            print("No members registered.")
            return

        print("-" * 60)
        print(f"{'ID':<8}{'Name':<30}{'Phone':<20}")
        print("-" * 60)

        for member in members:
            member_id, name, phone = member

            print(
                f"{member_id:<8}"
                f"{name[:28]:<30}"
                f"{(phone or '')[:18]:<20}"
            )

        print("-" * 60)

    except Error as e:
        print("Error displaying members:", e)

    finally:
        cursor.close()


# ISSUE BOOK


def issue_book(connection):
    cursor = connection.cursor()

    print("\n========== ISSUE BOOK ==========")

    try:
        book_id = int(input("Enter Book ID: "))
        member_id = int(input("Enter Member ID: "))

        # Check book
        cursor.execute("""
            SELECT title, quantity
            FROM books
            WHERE book_id = %s
        """, (book_id,))

        book = cursor.fetchone()

        if not book:
            print("Book not found.")
            return

        title, quantity = book

        if quantity <= 0:
            print("Book is currently unavailable.")
            return

        # Check member
        cursor.execute("""
            SELECT name
            FROM members
            WHERE member_id = %s
        """, (member_id,))

        member = cursor.fetchone()

        if not member:
            print("Member not found.")
            return

        # Check whether this member already has this book
        cursor.execute("""
            SELECT issue_id
            FROM issued_books
            WHERE book_id = %s
              AND member_id = %s
              AND return_date IS NULL
        """, (book_id, member_id))

        already_issued = cursor.fetchone()

        if already_issued:
            print("This member already has this book.")
            return

        # Issue the book
        cursor.execute("""
            INSERT INTO issued_books
            (book_id, member_id, issue_date)
            VALUES (%s, %s, %s)
        """, (book_id, member_id, date.today()))

        # Reduce quantity
        cursor.execute("""
            UPDATE books
            SET quantity = quantity - 1
            WHERE book_id = %s
        """, (book_id,))

        connection.commit()

        print(f"Book '{title}' issued successfully.")
        print("Issue date:", date.today())

    except ValueError:
        print("Please enter valid numeric IDs.")

    except Error as e:
        connection.rollback()
        print("Error issuing book:", e)

    finally:
        cursor.close()


# RETURN BOOK


def return_book(connection):
    cursor = connection.cursor()

    print("\n========== RETURN BOOK ==========")

    try:
        issue_id = int(input("Enter Issue ID: "))

        # Find active issue
        cursor.execute("""
            SELECT book_id, member_id, issue_date
            FROM issued_books
            WHERE issue_id = %s
              AND return_date IS NULL
        """, (issue_id,))

        record = cursor.fetchone()

        if not record:
            print("Active issue record not found.")
            return

        book_id, member_id, issue_date = record

        # Set return date
        cursor.execute("""
            UPDATE issued_books
            SET return_date = %s
            WHERE issue_id = %s
        """, (date.today(), issue_id))

        # Increase book quantity
        cursor.execute("""
            UPDATE books
            SET quantity = quantity + 1
            WHERE book_id = %s
        """, (book_id,))

        connection.commit()

        print("Book returned successfully.")
        print("Return date:", date.today())

    except ValueError:
        print("Please enter a valid Issue ID.")

    except Error as e:
        connection.rollback()
        print("Error returning book:", e)

    finally:
        cursor.close()



# VIEW ISSUED BOOKS


def view_issued_books(connection):
    cursor = connection.cursor()

    print("\n================ ISSUED BOOKS ================")

    try:
        cursor.execute("""
            SELECT
                i.issue_id,
                b.title,
                m.name,
                i.issue_date,
                i.return_date
            FROM issued_books i
            INNER JOIN books b
                ON i.book_id = b.book_id
            INNER JOIN members m
                ON i.member_id = m.member_id
            ORDER BY i.issue_id
        """)

        records = cursor.fetchall()

        if not records:
            print("No issue records found.")
            return

        print("-" * 100)
        print(
            f"{'Issue ID':<10}"
            f"{'Book':<30}"
            f"{'Member':<25}"
            f"{'Issue Date':<15}"
            f"{'Return Date':<15}"
        )
        print("-" * 100)

        for record in records:
            issue_id, title, member_name, issue_date, return_date = record

            return_text = str(return_date) if return_date else "Not Returned"

            print(
                f"{issue_id:<10}"
                f"{title[:28]:<30}"
                f"{member_name[:23]:<25}"
                f"{str(issue_date):<15}"
                f"{return_text:<15}"
            )

        print("-" * 100)

    except Error as e:
        print("Error displaying issue records:", e)

    finally:
        cursor.close()


# MAIN MENU


def main():
    print("=" * 60)
    print("          LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)

    connection = connect_database()

    if connection is None:
        print("Could not connect to MySQL.")
        return

    setup_database(connection)

    # Select the database
    cursor = connection.cursor()
    cursor.execute("USE library_db")
    cursor.close()

    while True:

        print("\n")
        print("=" * 50)
        print("              MAIN MENU")
        print("=" * 50)

        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Delete Book")
        print("5. Register Member")
        print("6. View Members")
        print("7. Issue Book")
        print("8. Return Book")
        print("9. View Issued Books")
        print("10. Exit")

        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book(connection)

        elif choice == "2":
            view_books(connection)

        elif choice == "3":
            search_book(connection)

        elif choice == "4":
            delete_book(connection)

        elif choice == "5":
            add_member(connection)

        elif choice == "6":
            view_members(connection)

        elif choice == "7":
            issue_book(connection)

        elif choice == "8":
            return_book(connection)

        elif choice == "9":
            view_issued_books(connection)

        elif choice == "10":
            print("\nThank you for using the Library Management System.")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 10.")

    connection.close()
    print("Database connection closed.")



# PROGRAM START


if __name__ == "__main__":
    main()
