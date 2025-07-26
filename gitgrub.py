from flask import Flask, request, redirect, url_for, render_template
from seed import *
import hashlib    

app = Flask(__name__)

@app.route("/")
def home():
    user_id = request.cookies.get('YourSessionCookie')
    if user_id:
        user = db.get(user_id)
        if user:
            # Success!
            return render_template('welcome.html', user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # You should really validate that these fields
        # are provided, rather than displaying an ugly
        # error message, but for the sake of a simple
        # example we'll just assume they are provided

        email = request.form.get('email')
        password = request.form.get('password')

        user = find_by_name_and_password(email, password)

        if not user:
            # Again, throwing an error is not a user-friendly
            # way of handling this, but this is just an example
            raise ValueError("Invalid username or password supplied")

        # Note we don't *return* the response immediately
        response = redirect(url_for("do_that"))
        response.set_cookie('YourSessionCookie', user.id)
        return response
    else:
        response = render_template('login.html')
        return response 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('register.html', message="All fields are required.")

        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Check if user already exists
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', message="User already exists.")

        # Insert new user
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password_hash))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))  # Assuming you have a login route

    return render_template('register.html')
 

if __name__ == '__main__':
    db = db_make_connection()
    init_db(db)
    app.run(debug=True)
   