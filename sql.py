import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)
