import mysql.connector


conn = mysql.connector.connect(
    host='localhost',
    user='root@gmail.com',
    password='abc',
    database='st_database'
)
c=conn.cursor()
c = conn.cursor()
c.execute('''CREATE DATABASE st_database''' )

c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255),
    student_id INT,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
''')

def insert_students(student_list):
    c.executemany('INSERT INTO students (name, age) VALUES (%s, %s)', student_list)
    conn.commit()

def get_all_students():
    c.execute('SELECT * FROM students')
    for row in c.fetchall():
        print(row)

def get_students_above_20():
    c.execute('SELECT * FROM students WHERE age > 20')
    for row in c.fetchall():
        print(row)

def update_student_name(id, new_name):
    c.execute('UPDATE students SET name = %s WHERE id = %s', (new_name, id))
    conn.commit()


