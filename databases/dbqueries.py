import sqlite3
import random



conn = sqlite3.connect('databases/aanwezigheid.db')

c = conn.cursor()




# query = '''

#             CREATE TABLE presence (
#             student_id INTEGER ,
#             meeting_id INTEGER,
#             present INTEGER
#             );
#             CREATE TABLE teacher (
#             teacher_id INTEGER UNIQUE,
#             teacher_firstname TEXT,
#             teacher_surname TEXT,
#             teacher_email TEXT
#             );

#             CREATE TABLE user (
#             user_id INTEGER PRIMARY KEY,
#             username TEXT UNIQUE,
#             password TEXT
#             );
            
#             CREATE TABLE meeting (
#             meeting_id INTEGER PRIMARY KEY,
#             meeting_date TEXT,
#             meeting_time TEXT,
#             meeting_location TEXT
#             );

#             CREATE TABLE class (
#             class_id INTEGER PRIMARY KEY,
#             class_name TEXT
#             );
#             CREATE TABLE subject (
#             subject_id INTEGER PRIMARY KEY,
#             subject_name TEXT
#             );

#             CREATE TABLE student (
#             student_id INTEGER UNIQUE,
#             student_firstname TEXT,
#             student_surname TEXT,
#             student_email TEXT


#         '''

# c.execute(query)

# first_names = ['Mo', 'Ferdi', 'Yassine', 'Ezel', 'Adam']
# last_names = ['De Jong', 'Visser', 'Van Dijk', 'Brown', 'De Vries']


# for i in range(10):

#     student_id = random.randint(1000000, 9999999)
#     student_email = str(student_id) + "@hr.nl"
#     print(student_email)

#     first_name = random.choice(first_names)
#     last_name = random.choice(last_names)

#     query = "INSERT INTO student (student_id, student_firstname, student_surname, student_email) VALUES (?, ?, ?, ?);"
#     values = (student_id, first_name, last_name, student_email)
#     c.execute(query, values)

# query = "INSERT INTO subject (subject_name) VALUES ('Databases');"

# query = """
# ALTER TABLE meeting
# ADD COLUMN meeting_end TIME;
# ALTER TABLE meeting
# ADD COLUMN subject_id INTEGER;
# """
# query = "ALTER TABLE meeting RENAME COLUMN meeting_end TO meeting_end_old;"
# query += "ALTER TABLE meeting ADD COLUMN meeting_end TEXT;"
# query += "UPDATE meeting SET meeting_end = strftime('%H:%M', meeting_end_old);"
# query += "ALTER TABLE meeting DROP COLUMN meeting_end_old;"
# c.executescript(query)
    
conn.commit()
# Close the database connection
conn.close()