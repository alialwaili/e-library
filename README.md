Ali Alwaili's Archive - E-Library
Ali ALwaili's Archive is a feature-rich, themed digital library web application built with Python and the Flask framework. It presents a unique "hacker" or "dark web" aesthetic, providing a secure and clandestine repository for digital books. The application is designed with a clear separation between the public-facing library and a secure, hidden administrative backend for content management.

Features
User-Facing Features
Homepage: Displays the most recently uploaded books for quick access.

Book Collection: A dedicated page to browse the entire collection of available books.

Search Functionality: A client-side search to quickly filter books by title, author, or description.

Book Downloads: Users can download books directly from the library.

Download Counter: Each book displays a counter showing how many times it has been downloaded.

Administrative Features
Obscured Admin Portal: The login page for the admin dashboard is located at a non-standard, difficult-to-guess URL to prevent unauthorized discovery.

Secure Authentication: The admin portal is protected by a username, a hashed password, and a unique security token.

Admin Dashboard: A central hub for administrators that provides:

System status and key statistics.

A form to upload new books.

A management panel to view and delete existing books.

Content Management: Full control over the library's content, including adding and removing books.

Secure Logout: A dedicated logout function to securely terminate the admin session.

Technologies Used
Backend:

Python 3

Flask (Web Framework)

Werkzeug (Password Hashing)

Database:

SQLite 3

Frontend:

HTML5

CSS3 (with custom "hacker" theme)

JavaScript (for dynamic effects and search functionality)

Project Structure
e-library/
│
├── app.py                  # Main Flask application file
├── library.db              # SQLite database file (created on run)
├── requirements.txt        # Python dependencies
│
├── static/
│   ├── css/
│   │   ├── admin.css       # Styles for the admin dashboard
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── script.js       # Main JavaScript file
│
├── templates/
│   ├── admin_dashboard.html  # Admin management page
│   ├── base.html             # Base template for all pages
│   ├── books.html            # Page to display all books
│   ├── index.html            # Homepage
│   └── login.html            # Admin login page
│
└── uploads/
    └── ...                   # Directory for uploaded book files (PDFs)


Setup and Installation
Follow these steps to get the project running on your local machine.

Prerequisites
Python 3.6 or higher

pip (Python package installer)

1. Clone the Repository
Clone the project to your local machine (or download the source code).

git clone <your-repository-url>
cd e-library


2. Install Dependencies
Install the required Python packages using the requirements.txt file.

pip install -r requirements.txt


3. Initialize the Database
Before running the application for the first time, you may need to delete any existing library.db file to ensure the latest database schema is created.

The application is configured to automatically create and initialize the library.db file when it starts if one doesn't already exist.

4. Run the Application
Start the Flask development server.

python app.py


The application will be running at http://127.0.0.1:5000/.

Usage
Accessing the Library
Homepage: Navigate to http://127.0.0.1:5000/ to see the latest books.

All Books: Go to http://127.0.0.1:5000/books to view the entire collection.

Accessing the Admin Portal
The admin login page is intentionally hidden to enhance security.

Navigate to the secret URL:
http://127.0.0.1:5000/s_2a7_d_4m_9i_1n_3_b_
