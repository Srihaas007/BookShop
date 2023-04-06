# Bookstore Web Application
This is a simple Flask web application that simulates a bookstore. It allows users to view and purchase books, and administrators to add and manage books.

## Installation
To use this application, you need to have Python 3 and Flask installed on your computer. You can download and install Python from the official website, and install Flask using the following command:

### pip install flask
You also need to create a SQLite database file named products.db in the root directory of the project. You can do this using any SQLite database management tool or by running the following command:

### sqlite3 products.db < schema.sql

## Usage
To run the application, open a terminal or command prompt and navigate to the root directory of the project. Then run the following command:


### python app.py
This will start the Flask development server, and you can access the application by opening a web browser and navigating to http://localhost:5000/.

## Features
The application has the following features:

View a list of books
View details of a book
Add a book to the cart
Remove a book from the cart
Checkout the cart
Login as a user or administrator
Logout from the application
Add a new book (administrator only)
Edit a book (administrator only)
Delete a book (administrator only)
## Contributing
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request.
