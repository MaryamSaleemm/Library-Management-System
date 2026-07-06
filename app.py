"""
app.py

Purpose:
---------
Command Line Interface (CLI) for the Library Management System.

This file only handles user input and calls the appropriate
functions from library_service.py.
"""

from library_service import (
    add_book,list_books,search_book, remove_book,register_member,list_members,loan_book,return_book,list_loans

)


while True:

    print("\n---- Library Management System -----")
    print("1. Add Book")
    print("2. List Books")
    print("3. Search Book")
    print("4. Remove Book")
    print("5. Register Member")
    print("6. Loan Book")
    print("7. Return Book")
    print("8. List Members")
    print("9. List Loans")
    print("10. Exit")

    choice = input("\nEnter choice: ")
    
    # Add Book
 
    if choice == "1":

        title = input("Book Title: ")
        author = input("Author: ")

        add_book(title, author)

    # List Books

    elif choice == "2":

        list_books()

    # Search Book
    
    elif choice == "3":

        title = input("Book Title: ")

        search_book(title)
        
    # Remove Book
    
    elif choice == "4":

        book_id = int(input("Book ID: "))

        remove_book(book_id)

    # Register Member

    elif choice == "5":

        name = input("Member Name: ")
        email = input("Email: ")
        phone = input("Phone: ")

        register_member(name, email, phone)


    # Loan Book
    
    elif choice == "6":

        book_id = int(input("Book ID: "))
        member_id = int(input("Member ID: "))

        loan_book(book_id, member_id)


    # Return Book
    
    elif choice == "7":

        book_id = int(input("Book ID: "))

        return_book(book_id)


    # Exit
    
    elif choice == "8":

        list_members()
        
        
        
    elif choice == "9":

        list_loans()
        
        
    elif choice == "10":

        print("Goodbye!")

        break