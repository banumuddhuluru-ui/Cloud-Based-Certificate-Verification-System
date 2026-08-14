from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "certificates.db"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            course TEXT NOT NULL,
            institution TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HTML + CSS ----------------

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Digital Certificate Verification</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            background: #f4f7fb;
            color: #222;
        }

        header {
            background: #182848;
            color: white;
            padding: 20px;
            text-align: center;
        }

        header h1 {
            margin-bottom: 8px;
        }

        nav {
            background: #263b73;
            padding: 12px;
            text-align: center;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-weight: bold;
        }

        nav a:hover {
            color: #ffd166;
        }

        .container {
            width: 90%;
            max-width: 1000px;
            margin: 40px auto;
        }

        .hero {
            background: white;
            padding: 40px;
            text-align: center;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .hero h2 {
            color: #182848;
            margin-bottom: 15px;
        }

        .hero p {
            margin-bottom: 25px;
            color: #555;
        }

        .btn {
            display: inline-block;
            background: #182848;
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            text-decoration: none;
            margin: 5px;
            border: none;
            cursor: pointer;
        }

        .btn:hover {
            background: #263b73;
        }

        .card {
            background: white;
            padding: 30px;
            margin-top: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        .card h2 {
            margin-bottom: 20px;
            color: #182848;
        }

        input {
            width: 100%;
            padding: 13px;
            margin: 8px 0 15px;
            border: 1px solid #ccc;
            border-radius: 7px;
            font-size: 15px;
        }

        label {
            font-weight: bold;
        }

        .success {
            background: #d4edda;
            color: #155724;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .certificate {
            border: 3px solid #182848;
            padding: 30px;
            margin-top: 20px;
            border-radius: 10px;
            background: #fff;
        }

        .certificate h2 {
            text-align: center;
            color: #182848;
            margin-bottom: 25px;
        }

        .certificate p {
            margin: 12px 0;
            font-size: 17px;
        }

        .valid {
            text-align: center;
            color: green;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #182848;
            color: white;
        }

        footer {
            margin-top: 50px;
            background: #182848;
            color: white;
            text-align: center;
            padding: 20px;
        }

        @media(max-width: 600px) {
            .container {
                width: 95%;
            }

            nav a {
                display: block;
                margin: 8px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>☁️ Digital Certificate Verification</h1>
    <p>Cloud-Based Certificate Authentication System</p>
</header>

<nav>
    <a href="/">Home</a>
    <a href="/verify">Verify Certificate</a>
    <a href="/add">Add Certificate</a>
    <a href="/certificates">View Certificates</a>
</nav>

<div class="container">

    {% block content %}{% endblock %}

</div>

<footer>
    <p>© 2026 Digital Certificate Verification System</p>
</footer>

</body>
</html>
"""


# ---------------- HOME ----------------

HOME = """
{% extends "base" %}

{% block content %}

<div class="hero">

    <h2>Digital Certificate Verification System</h2>

    <p>
        Verify the authenticity of digital certificates quickly
        and securely using a unique certificate ID.
    </p>

    <a href="/verify" class="btn">🔍 Verify Certificate</a>

    <a href="/add" class="btn">➕ Add Certificate</a>

</div>

<div class="card">

    <h2>How It Works</h2>

    <p>1️⃣ Certificate is registered in the system.</p>
    <br>

    <p>2️⃣ Each certificate receives a unique Certificate ID.</p>
    <br>

    <p>3️⃣ Anyone can enter the Certificate ID.</p>
    <br>

    <p>4️⃣ The system checks the database.</p>
    <br>

    <p>5️⃣ Certificate details are displayed if valid.</p>

</div>

{% endblock %}
"""


# ---------------- VERIFY ----------------

VERIFY = """
{% extends "base" %}

{% block content %}

<div class="card">

    <h2>🔍 Verify Certificate</h2>

    <form method="POST">

        <label>Certificate ID</label>

        <input
            type="text"
            name="certificate_id"
            placeholder="Example: CERT1001"
            required
        >

        <button class="btn" type="submit">
            Verify Certificate
        </button>

    </form>

    {% if certificate %}

    <div class="success">

        <div class="valid">
            ✓ CERTIFICATE IS VALID
        </div>

        <div class="certificate">

            <h2>Digital Certificate</h2>

            <p>
                <b>Certificate ID:</b>
                {{ certificate[1] }}
            </p>

            <p>
                <b>Student Name:</b>
                {{ certificate[2] }}
            </p>

            <p>
                <b>Course:</b>
                {{ certificate[3] }}
            </p>

            <p>
                <b>Institution:</b>
                {{ certificate[4] }}
            </p>

            <p>
                <b>Issue Date:</b>
                {{ certificate[5] }}
            </p>

            <p>
                <b>Grade:</b>
                {{ certificate[6] }}
            </p>

        </div>

    </div>

    {% elif searched %}

    <div class="error">

        ❌ <b>Certificate Not Found</b>

        <p>
            The entered Certificate ID does not exist
            in our database.
        </p>

    </div>

    {% endif %}

</div>

{% endblock %}
"""


# ---------------- ADD CERTIFICATE ----------------

ADD = """
{% extends "base" %}

{% block content %}

<div class="card">

    <h2>➕ Register Digital Certificate</h2>

    {% if message %}

    <div class="success">
        {{ message }}
    </div>

    {% endif %}

    {% if error %}

    <div class="error">
        {{ error }}
    </div>

    {% endif %}

    <form method="POST">

        <label>Certificate ID</label>

        <input
            type="text"
            name="certificate_id"
            placeholder="Example: CERT1001"
            required
        >

        <label>Student Name</label>

        <input
            type="text"
            name="student_name"
            placeholder="Enter student name"
            required
        >

        <label>Course</label>

        <input
            type="text"
            name="course"
            placeholder="Example: B.Tech Computer Science"
            required
        >

        <label>Institution</label>

        <input
            type="text"
            name="institution"
            placeholder="Enter institution name"
            required
        >

        <label>Issue Date</label>

        <input
            type="date"
            name="issue_date"
            required
        >

        <label>Grade</label>

        <input
            type="text"
            name="grade"
            placeholder="Example: A+"
            required
        >

        <button class="btn" type="submit">
            Add Certificate
        </button>

    </form>

</div>

{% endblock %}
"""


# ---------------- VIEW CERTIFICATES ----------------

CERTIFICATES = """
{% extends "base" %}

{% block content %}

<div class="card">

    <h2>📄 Registered Certificates</h2>

    <table>

        <tr>
            <th>Certificate ID</th>
            <th>Student Name</th>
            <th>Course</th>
            <th>Institution</th>
            <th>Issue Date</th>
            <th>Grade</th>
        </tr>

        {% for certificate in certificates %}

        <tr>

            <td>{{ certificate[1] }}</td>

            <td>{{ certificate[2] }}</td>

            <td>{{ certificate[3] }}</td>

            <td>{{ certificate[4] }}</td>

            <td>{{ certificate[5] }}</td>

            <td>{{ certificate[6] }}</td>

        </tr>

        {% endfor %}

    </table>

</div>

{% endblock %}
"""


# ---------------- TEMPLATE LOADER ----------------

from jinja2 import DictLoader

app.jinja_loader = DictLoader({
    "base": HTML,
    "home": HOME,
    "verify": VERIFY,
    "add": ADD,
    "certificates": CERTIFICATES
})


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template_string(HOME)


# ---------------- VERIFY ROUTE ----------------

@app.route("/verify", methods=["GET", "POST"])
def verify():

    certificate = None
    searched = False

    if request.method == "POST":

        certificate_id = request.form["certificate_id"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM certificates WHERE certificate_id = ?",
            (certificate_id,)
        )

        certificate = cursor.fetchone()

        conn.close()

        searched = True

    return render_template_string(
        VERIFY,
        certificate=certificate,
        searched=searched
    )


# ---------------- ADD ROUTE ----------------

@app.route("/add", methods=["GET", "POST"])
def add_certificate():

    message = None
    error = None

    if request.method == "POST":

        certificate_id = request.form["certificate_id"]
        student_name = request.form["student_name"]
        course = request.form["course"]
        institution = request.form["institution"]
        issue_date = request.form["issue_date"]
        grade = request.form["grade"]

        try:

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO certificates
                (certificate_id, student_name, course,
                 institution, issue_date, grade)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                certificate_id,
                student_name,
                course,
                institution,
                issue_date,
                grade
            ))

            conn.commit()
            conn.close()

            message = "✓ Certificate successfully registered!"

        except sqlite3.IntegrityError:

            error = "❌ Certificate ID already exists!"

    return render_template_string(
        ADD,
        message=message,
        error=error
    )


# ---------------- VIEW ALL CERTIFICATES ----------------

@app.route("/certificates")
def certificates():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM certificates ORDER BY id DESC"
    )

    certificates = cursor.fetchall()

    conn.close()

    return render_template_string(
        CERTIFICATES,
        certificates=certificates
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    init_db()

    print("======================================")
    print(" Digital Certificate Verification")
    print(" Server Started Successfully!")
    print("======================================")
    print("Open: http://127.0.0.1:5000")

    app.run(debug=True)