from flask import Flask, render_template, request, jsonify
import re
import string
import os
import pyodbc
from datetime import datetime
from flask import Flask, Request,redirect, render_template, request, flash

application = app = Flask(__name__)
app.secret_key = "Secret Key"

app = Flask(__name__)
app.config["image_folder"] = "./static/"
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif']
app.secret_key = "Secret Key"


DRIVER = '{ODBC Driver 18 for SQL Server}'
SERVER = 'adbserver.database.windows.net'
DATABASE = 'chetanadb'
USERNAME = 'chetanbalaji'
PASSWORD = 'Springadb123'

cnxn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
crsr = cnxn.cursor()

conn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
cursor = conn.cursor()


app = Flask(__name__, template_folder="templates")
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbsai.database.windows.net,1433;Database=adb;Uid=sainath;Pwd=Shiro@2018;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
cursor = connection.cursor() 
question = ""
answer = ""
score = 0
totalScore = 0
@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')

@app.route('/Student', methods=['POST', 'GET'])
def Student():
    cursor = connection.cursor()
    query_str = "select * from MSGS a " 
    print(query_str)    
    cursor.execute(query_str+" ORDER BY a.DATE")
    data = cursor.fetchall()
    return render_template('student.html', data = data, )

@app.route('/SetTime', methods=['POST', 'GET'])
def SetTime():
   global time
   time = int(request.form.get('time'))
   return redirect("https://adbsainathquiz5.azurewebsites.net/Admin")

    

@app.route('/StudentMessage', methods=['POST', 'GET'])
def StudentMessage():
    cursor = connection.cursor()
    msg = request.form.get("Message")
    query_str = "select * from MSGS a " 
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    query_str = "INSERT INTO MSGS(ROLE, MESSAGE, DATE) VALUES('STUDENT','"+msg+"','"+formatted_date+"')"
    print(query_str)
    cursor.execute(query_str)
    cursor.commit()

    query_str = "select top 1 * from MSGS a where a.ROLE = 'TEACHER'" 
    print(query_str)
    cursor.execute(query_str+" ORDER BY a.DATE DESC")
    data = cursor.fetchone()
    question = data[1]

    query_str = "select top 1 * from MSGS a where a.ROLE = 'STUDENT'" 
    print(query_str)
    cursor.execute(query_str+" ORDER BY a.DATE DESC")
    data = cursor.fetchone()
    answer = data[1]

    actualWords = []
    score = 0
    totalScore = 0
    words = question.split(" ")
    print("Words :",words)
    for i in words:
        print(i,i.isalpha())
        if i.isalpha():
            actualWords.append(i)
            totalScore+=10
    answerWords = answer.split(" ")
    
    for i in range(0, len(answerWords)):
        print("Substrings are ",answerWords[i][1:])
        if answerWords[i][1:] in actualWords:
            score+=10


    

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    scoreStr = "Score : "+str(score)+" Total Score : "+str(totalScore)
    query_str = "INSERT INTO MSGS(ROLE, MESSAGE, DATE) VALUES('ADMIN','"+scoreStr+"','"+formatted_date+"')"
    print(query_str)
    cursor.execute(query_str)
    cursor.commit()
    
   
    return redirect("https://adbsainathquiz5.azurewebsites.net/Student")


@app.route('/TeacherMessage', methods=['POST', 'GET'])
def TeacherMessage():
    cursor = connection.cursor()
    msg = request.form.get("Message")
    query_str = "select * from MSGS a " 
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    query_str = "INSERT INTO MSGS(ROLE, MESSAGE, DATE) VALUES('TEACHER','"+msg+"','"+formatted_date+"')"
    print(query_str)
    cursor.execute(query_str)
    cursor.commit()

    
    return redirect("https://adbsainathquiz5teacher.azurewebsites.net/Teacher")

@app.route('/Teacher', methods=['POST', 'GET'])
def Teacher():
    cursor = connection.cursor()
    query_str = "select * from MSGS a " 
    print(query_str)
    cursor.execute(query_str+" ORDER BY a.DATE")
    data = cursor.fetchall()
    return render_template('teacher.html', data = data)

@app.route('/Admin', methods=['POST', 'GET'])
def Admin():
    cursor = connection.cursor()

    
    query_str = "select * from MSGS a " 
    print(query_str)
    cursor.execute(query_str+" ORDER BY a.DATE")
    data = cursor.fetchall()




    return render_template('admin.html', data = data)


    

if __name__ == '__main__':
    app.run(debug=True)