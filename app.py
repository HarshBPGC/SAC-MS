
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
import datetime
import functools

app = Flask(__name__)
app.secret_key = "some_random_secret_key"  # For session security if needed

# Database config for sac_admin (read/write but no CREATE user privilege)
db_config = {
    'host': 'localhost',
    'user': 'sac_admin',
    'password': 'AdminPassword',
    'database': 'SAC'
}

# Database config for read-only user
db_config_readonly = {
    'host': 'localhost',
    'user': 'sac_viewer',
    'password': 'ViewerPassword',
    'database': 'SAC'
}

# Database config for database admin with all privileges
db_config_dba = {
    'host': 'localhost',
    'user': 'sac_dba',
    'password': 'Dbapassword',
    'database': 'SAC'
}

# Test the database connection at startup
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("Database connected successfully!")
    cursor.close()
    conn.close()
except Exception as e:
    print("Error connecting to the database:", e)


# Decorator for requiring admin privileges
def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({"error": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function


# Decorator for requiring database admin privileges
def dba_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'dba':
            return jsonify({"error": "Database admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    """
    Default route: We'll render a simple login page.
    """
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """
    Simple login route (DEMO):
    Checks if the user typed 'admin/admin123' or 'viewer/view123'
    just to show different roles.
    In reality, you'd have a USER table with hashed passwords.
    """
    data = request.json or request.form
    username = data.get('username')
    password = data.get('password')

    # Demo logic:
    if username == "admin" and password == "admin123":
        session["role"] = "admin"
        return jsonify({"message": "Login successful", "role": "admin"}), 200
    elif username == "viewer" and password == "view123":
        session["role"] = "viewer"
        return jsonify({"message": "Login successful", "role": "viewer"}), 200
    elif username == "dba" and password == "dba123":
        session["role"] = "dba"
        return jsonify({"message": "Login successful", "role": "dba"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route('/dashboard')
def dashboard():
    """
    Renders a dashboard page after login.
    """
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    """
    Logs out the user by clearing the session and redirects to the login page.
    """
    session.clear()
    return redirect(url_for('home'))


@app.route('/equipment', methods=['GET'])
def get_equipment():
    """
    Returns all equipment in JSON.
    """
    try:
        # Use the appropriate database connection based on user role
        if session.get('role') == 'viewer':
            conn = mysql.connector.connect(**db_config_readonly)
        elif session.get('role') == 'dba':
            conn = mysql.connector.connect(**db_config_dba)
        else:
            conn = mysql.connector.connect(**db_config)
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM EQUIPMENT")
        equipment_list = cursor.fetchall()
        return jsonify(equipment_list), 200
    except Exception as e:
        print("Error in /equipment GET:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/booking', methods=['POST'])
@admin_required
def create_booking():
    """
    Create a new booking record.
    Expect JSON with booking_time, status, bits_id, timeslot_id, location_id
    Example: { "booking_time":"2025-03-20 10:00:00", "status":"Pending", "bits_id":1, "timeslot_id":1, "location_id":1 }
    """
    try:
        data = request.json
        booking_time = data['booking_time']
        status = data['status']
        bits_id = data['bits_id']
        timeslot_id = data['timeslot_id']
        location_id = data['location_id']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO BOOKING (booking_time, status, bits_id, timeslot_id, location_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (booking_time, status, bits_id, timeslot_id, location_id))
        conn.commit()

        return jsonify({"message": "Booking created!", "booking_id": cursor.lastrowid}), 201
    except Exception as e:
        print("Error in /booking POST:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    # For local development
    app.run(debug=True)
