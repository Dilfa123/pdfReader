import sqlite3

con=sqlite3.connect('schood.db')
cursor=con.cursor()
cursor.execute('''
               CREATE TABLE students(id INTEGER PRIMARY KEY,name TEXT,age INTEGER,grade TEXT)''')
student_data=[
    (1,'Dilfa',21,"BCA"),
    (2,'Najiya',22,'BCA'),
    (3,'Thafneem',21,'CS'),
    (4,'Shameena',22,'CS')

]
cursor.execute(''' INSERT INTO students(id,name,age,grade)VALUES(?,?,?,?)''',student_data)
cursor.execute('SELECT * FROM students')
all_stud=cursor.fetchall()
for stud in all_stud:
    print(stud)

def searchByGrade(grade):
    cursor.execute('SELECT * FROM students WHERE grade=?',(grade))
    result=cursor.fetchall()
    for stud in result:
        print(stud)
print("student in bca is : ")
searchByGrade('BCA')
def update_age(student_id, new_age):
    cursor.execute('UPDATE students SET age = ? WHERE id = ?', (new_age, student_id))
    con.commit()
    print(f"Student with id {student_id} age updated to {new_age}")


update_age(3, 14)
def delete_student(student_id):
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    con.commit()
    print(f"Student with id {student_id} deleted")


delete_student(5)
con.close()