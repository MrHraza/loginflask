import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/login', methods=['GET', 'POST']) 
def login(): 


    return render_template('login.html') 

@app.route('/submit_details', methods=['GET', 'POST']) 
def submit_details(): 
    if request.method == 'POST': 
        name = request.form['name'] 
        email = request.form['email'] 
        message = request.form['message'] 

        conn = sqlite3.connect('contact.db') 
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO contact (name, email, message) VALUES (?, ?, ?)", (name, email, message)) 
        conn.commit() 
        conn.close() 

    return redirect(url_for('home'))

@app.route('/contacts', methods=['GET']) 

def contacts(): 
    conn = sqlite3.connect('contact.db') 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM contact") 
    contacts = cursor.fetchall() 
    conn.close() 
    contacts = "" 
    return render_template('contacts.html', contacts=contacts)


def init_db(): 
    conn = sqlite3.connect('contact.db') 
    cursor = conn.cursor() 
    # Check if the table already exists 
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contact'") 
    table_exists = cursor.fetchone() 

    if table_exists: 
        print("Table 'contact' already exists.") 
    else: 
        cursor.execute(""" 
        CREATE TABLE contact ( 
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            email TEXT NOT NULL, 
            message TEXT NOT NULL 
        ); 
        """) 
        print("Table 'contact' created.") 

    conn.commit() 
    conn.close() 


if __name__ == "__main__":  
    init_db()  
    app.run(debug=True)