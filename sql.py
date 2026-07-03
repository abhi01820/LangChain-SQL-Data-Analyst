import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)


cursor.execute("""INSERT INTO STUDENT VALUES ('Abhi', 'Computer Science', 'A', 90)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Khila', 'Data Science', 'B', 100)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Hardik', 'Computer Science', 'A', 86)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Aggarwal', 'DEVOPS', 'A', 50)""")
cursor.execute("""INSERT INTO STUDENT VALUES ('Lilly', 'DEVOPS', 'A', 35)""")


print("The inserted records are : ")

data=cursor.execute('''Select * From STUDENT''')

for row in data:
    print(row)


connection.commit()
connection.close()
