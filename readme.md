📚 Library Management System
Overview

A console-based Library Management System developed using Python and MySQL. It helps managing books, members, and book issue/return records through a simple menu-driven interface.

Features

Add, view, search, and delete books

Register and view library members

Issue and return books

Track issue and return dates

Automatically update book quantity

Prevent duplicate book issues

MySQL database integration

Input validation and error handling

Technology Used


IDLE PYTHON

MySQL

MySQL Connector/Python

Datetime module

REQUIREMENTS

Python 3.x

MySQL Server

MySQL Connector/Python

A Python IDE or code editor

How to Run

Install Python and MySQL on your system.

Make sure the MySQL server is running.

Install MySQL Connector/Python.

Configure your MySQL username and password in the program.

Run the Python application.

Select the required option from the main menu.

The application automatically creates the library_db database and required tables when it starts.

Testing

The system was tested for:

Adding and viewing books

Searching and deleting books

Registering and viewing members

Issuing and returning books

Updating book quantities

Preventing duplicate book issues

Handling invalid inputs

Handling database errors

Project Structure

Library-Management-System

library_management.py — Main Python application

README.md — Project documentation

Database

The project uses a MySQL database named library_db.

It contains three tables:

Books — Stores book details and quantity

Members — Stores member details

Issued Books — Stores book issue and return records

Author

PRASHANT KUMAR GUPTA
