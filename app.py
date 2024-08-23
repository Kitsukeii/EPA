from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
#Session key
app.secret_key = 'your_secret_key'

#Check username function
def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_user(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Please press back and try again :)"
    return render_template('login.html')

#Logout Button Function
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#Register User Function
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

#User Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

#Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

#User Profile Page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)