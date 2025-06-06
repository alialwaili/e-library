from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'library.db'
app.config['ADMIN_USER'] = 'shadowadmin'
app.config['ADMIN_PASS'] = generate_password_hash('darkweb123!')  # Change this in production

# Create directories if they don't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 description TEXT,
                 category TEXT NOT NULL,
                 access_level INTEGER NOT NULL,
                 file_path TEXT NOT NULL,
                 upload_date TEXT NOT NULL)''')
    
    # Create admin table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS admin
                 (id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    
    # Insert default admin if not exists
    c.execute("SELECT * FROM admin WHERE username = ?", (app.config['ADMIN_USER'],))
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", 
                  (app.config['ADMIN_USER'], app.config['ADMIN_PASS']))
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM books ORDER BY upload_date DESC LIMIT 6")
    recent_books = c.fetchall()
    c.execute("SELECT COUNT(*) FROM books")
    book_count = c.fetchone()[0]
    conn.close()
    
    return render_template('index.html', recent_books=recent_books, book_count=book_count)

@app.route('/books')
def books():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM books ORDER BY title")
    all_books = c.fetchall()
    conn.close()
    
    return render_template('books.html', books=all_books)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/shadow-login', methods=['GET', 'POST'])
def shadow_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = request.form['token']
        
        # Validate credentials
        if (username == app.config['ADMIN_USER'] and 
            check_password_hash(app.config['ADMIN_PASS'], password) and 
            token == '7X9P2R'):  # Change token in production
            
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials! Access denied.', 'danger')
    
    return render_template('login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('shadow_login'))
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM books ORDER BY upload_date DESC")
    books = c.fetchall()
    c.execute("SELECT COUNT(*) FROM books")
    book_count = c.fetchone()[0]
    conn.close()
    
    return render_template('admin_dashboard.html', books=books, book_count=book_count)

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin-upload', methods=['POST'])
def admin_upload():
    if not session.get('admin_logged_in'):
        return redirect(url_for('shadow_login'))
    
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    category = request.form['category']
    access_level = request.form['access_level']
    file = request.files['file']
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        conn = get_db()
        c = conn.cursor()
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO books (title, author, description, category, access_level, file_path, upload_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (title, author, description, category, access_level, filename, upload_date))
        conn.commit()
        conn.close()
        
        flash('Book uploaded successfully!', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin-delete/<int:book_id>', methods=['POST'])
def admin_delete(book_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('shadow_login'))
    
    conn = get_db()
    c = conn.cursor()
    
    # Get file path before deleting
    c.execute("SELECT file_path FROM books WHERE id = ?", (book_id,))
    book = c.fetchone()
    
    if book:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], book['file_path'])
        
        # Delete the book record
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        
        # Delete the file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        flash('Book deleted successfully!', 'success')
    
    conn.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)