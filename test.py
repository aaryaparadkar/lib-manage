# SOURCE CODE FOR LIBRARY

print("""****************************
*                          *
****   LIBRARY CODES    ****    
*                          *
****************************""")

# CREATING DATABASE CONNECTION TO DB4FREE
import mysql.connector
from mysql.connector import Error

# Replace these with your DB4Free credentials
mydb = mysql.connector.connect(
    host="db4free.net",     # DB4Free host
    user="kronos12",   # Your DB4Free username
    passwd="password", # Your DB4Free password
    database="librarymanagemen",
    # port=3306      # Your DB4Free database name
)

print(mydb)

# Test the connection by executing a simple query
mycursor = mydb.cursor()
mycursor.execute("SELECT VERSION()")
result = mycursor.fetchone()
print(f"Database version: {result[0]}")

# mycursor = mydb.cursor()

# CREATING REQUIRED TABLES
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS library_master (
        cardno CHAR(10) PRIMARY KEY,
        name_of_person VARCHAR(30),
        phone_no CHAR(10),
        address VARCHAR(30),
        dob DATE
    )
""")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_name VARCHAR(30),
        book_no CHAR(5) PRIMARY KEY,
        genre VARCHAR(10),
        authors_name VARCHAR(15),
        language VARCHAR(15)
    )
""")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS library_transaction (
        cardno CHAR(10),
        FOREIGN KEY(cardno) REFERENCES library_master(cardno),
        book_name VARCHAR(20),
        date_of_lend DATE,
        date_of_return DATE
    )
""")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS buy_new_books (
        orderno VARCHAR(6) PRIMARY KEY,
        name_of_book VARCHAR(20),
        del_date DATE,
        price CHAR(4)
    )
""")
mydb.commit()

while True:
    print("""
    ***************
    1 = Create a new account
    ***************
    """)
    print("""
    ***************
    2 = See the account info
    ***************
    """)
    print("""
    ***************
    3 = Update card holder info
    ***************
    """)
    print("""
    ***************
    4 = Delete the account
    ***************
    """)
    print("""
    ***************
    5 = Add new book
    ***************
    """)
    print("""
    ***************
    6 = See books
    ***************
    """)
    print("""
    ***************
    7 = Update book details
    ***************
    """)
    print("""
    ***************
    8 = Delete book
    ***************
    """)
    print("""
    ***************
    9 = Lend a book
    ***************
    """)
    print("""
    ***************
    10 = Return the book
    ***************
    """)
    print("""
    ***************
    11 = Display lending history
    ***************
    """)
    print("""
    ***************
    12 = Order a new book
    ***************
    """)
    print("""
    ***************
    13 = Update order details
    ***************
    """)
    print("""
    ***************
    14 = Display ordering history
    ***************
    """)
    print("""
    ***************
    15 = EXIT
    ***************
    """)

    ch = int(input("Enter your choice: "))

    # TO CREATE A LIBRARY ACCOUNT
    if ch == 1:
        print("If you want to go back, press 1")
        print("If you want to continue, press 2")
        a = int(input("Enter your choice: "))
        if a == 1:
            continue
        if a == 2:
            print("FILL ALL PERSONAL DETAILS OF ACCOUNT HOLDER")
            cardno = str(input("Enter card no: "))
            name_of_person = str(input("Enter name (limit 30 characters): "))
            phone_no = str(input("Enter phone no: "))
            address = str(input("Enter the address (max 30 words): "))
            dob = str(input("Enter the date of birth (yyyy-mm-dd): "))
            mycursor.execute("INSERT INTO library_master VALUES (%s, %s, %s, %s, %s)", 
                             (cardno, name_of_person, phone_no, address, dob))
            mydb.commit()
            print("ACCOUNT IS SUCCESSFULLY CREATED!!!")
    
    # TO SEE DETAILS OF CARD HOLDER
    if ch == 2:
        cardno = str(input("Enter card no: "))
        mycursor.execute("SELECT * FROM library_master WHERE cardno = %s", (cardno,))
        for i in mycursor:
            print(i)
    
    # TO UPDATE CARD HOLDER INFORMATION
    if ch == 3:
        print("Press 1 to update name:")
        print("Press 2 to update phone no:")
        print("Press 3 to update address:")
        print("Press 4 to update date of birth:")
        ch1 = int(input("Enter your choice: "))

        # TO UPDATE NAME
        if ch1 == 1:
            mycursor.execute("SELECT * FROM library_master")
            for i in mycursor:
                print(i)
            cardno = str(input("Enter card no: "))
            name_of_person = str(input("Enter new name: "))
            mycursor.execute("UPDATE library_master SET name_of_person = %s WHERE cardno = %s", 
                             (name_of_person, cardno))
            mydb.commit()
            print("*Name has been updated*")

        # TO UPDATE PHONE NUMBER
        elif ch1 == 2:
            cardno = str(input("Enter card no: "))
            phone_no = str(input("Enter new phone no: "))
            mycursor.execute("UPDATE library_master SET phone_no = %s WHERE cardno = %s", 
                             (phone_no, cardno))
            mydb.commit()
            print("*Number has been updated*")

        # TO UPDATE ADDRESS
        elif ch1 == 3:
            cardno = str(input("Enter card no: "))
            address = str(input("Enter new address: "))
            mycursor.execute("UPDATE library_master SET address = %s WHERE cardno = %s", 
                             (address, cardno))
            mydb.commit()
            print("*Address has been updated*")

        # TO UPDATE DATE OF BIRTH
        elif ch1 == 4:
            cardno = str(input("Enter card no: "))
            dob = str(input("Enter new date of birth (yyyy-mm-dd): "))
            mycursor.execute("UPDATE library_master SET dob = %s WHERE cardno = %s", 
                             (dob, cardno))
            mydb.commit()
            print("*Date of birth has been updated*")

    # TO DELETE AN ACCOUNT
    if ch == 4:
        cardno = str(input("Enter the card number of the account you wish to delete: "))
        mycursor.execute("DELETE FROM library_master WHERE cardno = %s", (cardno,))
        mydb.commit()
        print("Account deleted successfully.")

    # TO ADD NEW BOOK
    if ch == 5:
        book_name = str(input("Enter book name: "))
        book_no = str(input("Enter book number: "))
        genre = str(input("Enter genre: "))
        authors_name = str(input("Enter author's name: "))
        language = str(input("Enter language: "))
        mycursor.execute("INSERT INTO books VALUES (%s, %s, %s, %s, %s)", 
                         (book_name, book_no, genre, authors_name, language))
        mydb.commit()
        print("Book added successfully.")

    # TO SEE ALL BOOKS
    if ch == 6:
        mycursor.execute("SELECT * FROM books")
        for book in mycursor:
            print(book)

    # TO UPDATE BOOK DETAILS
    if ch == 7:
        book_no = str(input("Enter the book number of the book to update: "))
        print("Press 1 to update book name")
        print("Press 2 to update genre")
        print("Press 3 to update author's name")
        print("Press 4 to update language")
        ch2 = int(input("Enter your choice: "))
        
        if ch2 == 1:
            new_name = str(input("Enter new book name: "))
            mycursor.execute("UPDATE books SET book_name = %s WHERE book_no = %s", 
                             (new_name, book_no))
        elif ch2 == 2:
            new_genre = str(input("Enter new genre: "))
            mycursor.execute("UPDATE books SET genre = %s WHERE book_no = %s", 
                             (new_genre, book_no))
        elif ch2 == 3:
            new_author = str(input("Enter new author's name: "))
            mycursor.execute("UPDATE books SET authors_name = %s WHERE book_no = %s", 
                             (new_author, book_no))
        elif ch2 == 4:
            new_language = str(input("Enter new language: "))
            mycursor.execute("UPDATE books SET language = %s WHERE book_no = %s", 
                             (new_language, book_no))
        mydb.commit()
        print("Book details updated successfully.")

    # TO DELETE A BOOK
    if ch == 8:
        book_no = str(input("Enter the book number of the book to delete: "))
        mycursor.execute("DELETE FROM books WHERE book_no = %s", (book_no,))
        mydb.commit()
        print("Book deleted successfully.")

    # TO LEND A BOOK
    if ch == 9:
        cardno = str(input("Enter card number: "))
        book_name = str(input("Enter book name: "))
        date_of_lend = str(input("Enter date of lend (yyyy-mm-dd): "))
        mycursor.execute("INSERT INTO library_transaction (cardno, book_name, date_of_lend) VALUES (%s, %s, %s)", 
                         (cardno, book_name, date_of_lend))
        mydb.commit()
        print("Book lent successfully.")

    # TO RETURN A BOOK
    if ch == 10:
        cardno = str(input("Enter card number: "))
        book_name = str(input("Enter book name: "))
        date_of_return = str(input("Enter date of return (yyyy-mm-dd): "))
        mycursor.execute("UPDATE library_transaction SET date_of_return = %s WHERE cardno = %s AND book_name = %s", 
                         (date_of_return, cardno, book_name))
        mydb.commit()
        print("Book returned successfully.")

    # TO DISPLAY LENDING HISTORY
    if ch == 11:
        cardno = str(input("Enter card number: "))
        mycursor.execute("SELECT * FROM library_transaction WHERE cardno = %s", (cardno,))
        for transaction in mycursor:
            print(transaction)

    # TO ORDER A NEW BOOK
    if ch == 12:
        orderno = str(input("Enter order number: "))
        name_of_book = str(input("Enter the name of the book: "))
        del_date = str(input("Enter the delivery date (yyyy-mm-dd): "))
        price = str(input("Enter the price of the book: "))
        mycursor.execute("INSERT INTO buy_new_books VALUES (%s, %s, %s, %s)", 
                         (orderno, name_of_book, del_date, price))
        mydb.commit()
        print("Book ordered successfully.")

    # TO UPDATE ORDER DETAILS
    if ch == 13:
        orderno = str(input("Enter the order number: "))
        print("Press 1 to update book name")
        print("Press 2 to update delivery date")
        print("Press 3 to update price")
        ch3 = int(input("Enter your choice: "))
        
        if ch3 == 1:
            new_book_name = str(input("Enter new book name: "))
            mycursor.execute("UPDATE buy_new_books SET name_of_book = %s WHERE orderno = %s", 
                             (new_book_name, orderno))
        elif ch3 == 2:
            new_del_date = str(input("Enter new delivery date (yyyy-mm-dd): "))
            mycursor.execute("UPDATE buy_new_books SET del_date = %s WHERE orderno = %s", 
                             (new_del_date, orderno))
        elif ch3 == 3:
            new_price = str(input("Enter new price: "))
            mycursor.execute("UPDATE buy_new_books SET price = %s WHERE orderno = %s", 
                             (new_price, orderno))
        mydb.commit()
        print("Order details updated successfully.")

    # TO DISPLAY ORDERING HISTORY
    if ch == 14:
        mycursor.execute("SELECT * FROM buy_new_books")
        for order in mycursor:
            print(order)

    # TO EXIT THE SYSTEM
    if ch == 15:
        print("Exiting the Library Management System.")
        break
