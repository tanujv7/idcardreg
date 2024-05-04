from flask import Flask, request, render_template
import pyodbc
import os
app = Flask(__name__)
app.config['UPLOAD_PATH'] = r'$PWD/uploads/'

@app.route('/',methods=["GET", "POST"])




def IDCARDFORM():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        student_id = request.form.get("student_id")
        program = request.form.get("program")
        filePhoto = request.files.get('photo','')
        SERVER = 'localhost'
        DATABASE = 'StudentsList'
        USERNAME = 'tanuj'
        PASSWORD = 'Tanuj1234'

        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME}; PWD={PASSWORD};TrustServerCertificate=yes'
        conn = pyodbc.connect(connectionString)
        if (conn):
            print("Connection Made Successfully!!")
            fileName = filePhoto.filename
            if fileName != '':
                fileName = first_name + "_" + student_id +".jpg" 
                filePath = os.path.join(app.config['UPLOAD_PATH'], fileName)
                filePhoto.save(filePath)

            
            SQL_QUERY = """CREATE TABLE STULIST(student_id varchar(8) PRIMARY KEY, first_name varchar(20), last_name varchar(20), program varchar(50), photo varchar(200));"""
            INSERT_QUERY = """INSERT INTO STULIST(student_id, first_name, last_name, program,photo) VALUES(?,?,?,?,?)"""

            cursor = conn.cursor()

            try:
                if(cursor.execute(SQL_QUERY)):
                    print("Command Executed Successfully")
                    cursor.commit()
            except pyodbc.ProgrammingError :
                print("Table Already Exists!, Moving Forward ...")

                if(cursor.execute(INSERT_QUERY, student_id, first_name, last_name, program, filePath)):
                    cursor.commit()
                    print("Data Commited Succesfully")
                    cursor.close()
                    first_n = first_name
                    return render_template('thankyou.html',fname=first_n, sid=student_id)
                    
                else:
                    print("Data Failed To Transfer")


               
        else :
            print("Connection Failed!!")
    return render_template("IDCardform.html")


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
