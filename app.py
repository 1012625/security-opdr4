from flask import Flask, render_template, jsonify, session, flash, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/overzichtspagina")
def overzicht():
    return render_template("overzichtspagina.html")

@app.route("/students/<int:meeting_id>")
def get_users(meeting_id):
    conn = sqlite3.connect("databases/aanwezigheid.db")
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM presence
        JOIN student ON student.student_id = presence.student_id
        JOIN meeting ON meeting.meeting_id = presence.meeting_id
        WHERE presence.meeting_id = ? AND student.klas = meeting.classes
    """, (meeting_id,))

    rows = c.fetchall()
    conn.close()

    return jsonify(rows)


@app.route("/studentsNotPresent/<int:meeting_id>")
def get_users_not_present(meeting_id):
    conn = sqlite3.connect("databases/aanwezigheid.db")
    c = conn.cursor()
    c.execute("""
        SELECT *
        FROM student
        WHERE student.klas IN (
            SELECT meeting.classes
            FROM meeting
            WHERE meeting.meeting_id = ?
        )
        AND student.student_id NOT IN (
            SELECT presence.student_id
            FROM presence
            WHERE presence.meeting_id = ?
        )
    """, (meeting_id, meeting_id))

    rows = c.fetchall()
    conn.close()

    return jsonify(rows)



def login(username, password):
    conn = sqlite3.connect("databases/aanwezigheid.db")
    c = conn.cursor()

    query = "SELECT * FROM user WHERE username=? AND password=?"
    c.execute(query, (username, password))
    row = c.fetchone()

    conn.close()

    if row:
        return True
    else:
        flash('Invalid username or password')
        return False

@app.route('/inlog', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login(username, password):
            session['username'] = username
            return redirect('/overzichtspagina')
        else:
            flash('Invalid username or password')

    return render_template('/login.html')

@app.route('/checkinpagina')
def show_checkinpagina():
    meetingid = request.args.get('meetingid')
    conn = sqlite3.connect("databases/aanwezigheid.db")
    c = conn.cursor()
    c.execute("SELECT student_id FROM meeting, student WHERE meeting_id = ? AND student.klas = meeting.classes", (meetingid,))
    students = c.fetchall()
    conn.close()
    return render_template('checkinpagina.html', students=students)

    
@app.route('/checkin', methods=['POST'])
def checkin():
    student_id = request.form['student-id']
    meeting_id = request.form['meeting-id']
    conn = sqlite3.connect("databases/aanwezigheid.db")
    c = conn.cursor()

    # Check if student already is present in meeting
    c.execute("SELECT * FROM presence WHERE student_id = ? AND meeting_id = ?", (student_id, meeting_id,))
    result = c.fetchone()

    if result is not None:
        conn.close()
        return jsonify({'message': 'Student has already checked in.'})
    # Add 1 if present
    c.execute("INSERT INTO presence (student_id, meeting_id, present) VALUES (?, ?, 1)", (student_id, meeting_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Checked in'})
    

@app.route("/create-meeting", methods=['GET', 'POST'])
def create_meeting():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        meeting_date = request.form['meeting_date']
        meeting_starttime = request.form['meeting_starttime']
        meeting_endtime = request.form['meeting_endtime']
        meeting_subject = request.form['meeting_subject']
        meeting_location = request.form['meeting_location']
        meeting_class = request.form['meeting_class']

        conn = sqlite3.connect("databases/aanwezigheid.db")
        c = conn.cursor()
        query = "INSERT INTO meeting (meeting_date, meeting_time, meeting_end, subject_id, meeting_location, classes) VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(query, (meeting_date, meeting_starttime, meeting_endtime, meeting_subject, meeting_location, meeting_class))
        conn.commit()
        conn.close()

        flash('Meeting created successfully')
        return redirect('/meetings')
    return render_template("create-meeting.html")

@app.route("/create-teacher", methods=['GET', 'POST'])
def create_teacher():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        teacher_firstname = request.form['teacher_firstname']
        teacher_surname = request.form['teacher_surname']
        teacher_email = request.form['teacher_email']

        conn = sqlite3.connect("databases/aanwezigheid.db")
        c = conn.cursor()
        query = "INSERT INTO teacher (teacher_firstname, teacher_surname, teacher_email) VALUES (?, ?, ?)"
        c.execute(query, (teacher_firstname, teacher_surname, teacher_email))
        conn.commit()
        conn.close()

        flash('Teacher created successfully')
        return redirect('/teacher')
    return render_template("create-teacher.html")

@app.route("/meetingjson")
def getmeetingjson():
    if 'username' not in session:
        return redirect('/login')
    else:
        conn = sqlite3.connect("databases/aanwezigheid.db")
        c = conn.cursor()

        c.execute("SELECT * FROM meeting ORDER BY meeting_id DESC")
        rows = c.fetchall()

        conn.close()

    return jsonify(rows)

@app.route("/subjects")
def getsubjects():
    if 'username' not in session:
        return redirect('/login')
    else:
        conn = sqlite3.connect("databases/aanwezigheid.db")
        c = conn.cursor()

        c.execute("SELECT * FROM subject")
        rows = c.fetchall()

        conn.close()

    return jsonify(rows)

@app.route('/subjectMeetings/<int:subject_id>', methods=['GET'])
def get_subject_meetings(subject_id):
    conn = sqlite3.connect("databases/aanwezigheid.db")
    c = conn.cursor()
    c.execute("SELECT * FROM meeting WHERE subject_id=?", (subject_id,))
    rows = c.fetchall()
    return jsonify(rows)

@app.route("/teacherjson")
def getteacherjson():
    if 'username' not in session:
        return redirect('/login')
    else:
        conn = sqlite3.connect("databases/aanwezigheid.db")
        c = conn.cursor()

        c.execute("SELECT * FROM teacher")
        rows = c.fetchall()

        conn.close()

    return jsonify(rows)

@app.route("/meetings")
def meetings():
    return render_template("/meetings.html")

@app.route("/teacher")
def teacher():
    return render_template("/teachers.html")

@app.route('/meeting/<int:meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    conn = sqlite3.connect('databases/aanwezigheid.db')
    c = conn.cursor()
    c.execute("DELETE FROM meeting WHERE meeting_id=?", (meeting_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Meeting deleted successfully"})

@app.route('/meeting/<int:meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    data = request.get_json()
    conn = sqlite3.connect('databases/aanwezigheid.db')
    c = conn.cursor()
    c.execute("UPDATE meeting SET meeting_date=?, meeting_time=?, meeting_location=? WHERE meeting_id=?",
              (data['meeting_date'], data['meeting_time'], data['meeting_location'], meeting_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Meeting updated successfully'})

@app.route('/teacher/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    data = request.get_json()
    conn = sqlite3.connect('databases/aanwezigheid.db')
    c = conn.cursor()
    c.execute("UPDATE teacher SET teacher_firstname=?, teacher_surname=?, teacher_email=? WHERE teacher_id=?",
              (data['teacher_firstname'], data['teacher_surname'], data['teacher_email'], teacher_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Teacher updated successfully'})

@app.route('/teacher/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    conn = sqlite3.connect('databases/aanwezigheid.db')
    c = conn.cursor()
    c.execute("DELETE FROM teacher WHERE teacher_id=?", (teacher_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Teacher deleted successfully"})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host="145.137.54.140",debug=True)