from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB Connection
def connect_db():
    return sqlite3.connect('students.db')

# Initialize DB (run once)
def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    course TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        conn = connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = connect_db()
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        c.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?", (name, email, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()
    conn.close()
    return render_template("edit.html", student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
