from flask import Flask, render_template, request, jsonify
import re
import string
import os
import pyodbc
import random 
import time
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

connection = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
cursor = connection.cursor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/judge_home', methods=['POST'])
def judge_home():
    return render_template('judge.html')

@app.route('/judge', methods=['POST'])
def judge():
    low_range = int(request.form['low_range'])
    high_range = int(request.form['high_range'])
    tolerance = int(request.form['tolerance'])
    countdown = int(request.form['countdown'])
    print(low_range,high_range)
    crsr.execute("INSERT INTO [dbo].[game_settings] values(?,?,?,?,?,?)",'judge',low_range,high_range,countdown,tolerance,0)
    crsr.commit()
    p1='player1'
    crsr.execute("select secret_val from [dbo].[game_settings] where name = '"+p1+"'")
    try:
        p1_secret = crsr.fetchall()[0][0]
    except:
        p1_secret = 0
    # p1_secret=55
    return render_template('judge_stay.html',p1_secret=p1_secret)


@app.route('/player1_home', methods=['POST'])
def player1_home():
    return render_template('player1.html')

@app.route('/player1', methods=['POST'])
def player1():
    secret = int(request.form['secret'])
    crsr.execute("INSERT INTO [dbo].[game_settings] values(?,?,?,?,?,?)",'player1',0,0,0,0,secret)
    crsr.commit()
    return render_template('player1_stay.html',secret=secret)

@app.route('/player99_home', methods=['POST'])
def player99_home():
    return render_template('player99.html')

@app.route('/player99', methods=['POST'])
def player99():
    secret_guess = int(request.form['secret_guess'])
    p1='player1'
    crsr.execute("select secret_val from [dbo].[game_settings] where name = '"+p1+"'")
    p1_secret = crsr.fetchall()[0][0]
    print('guess',secret_guess,'secret',p1_secret)
    # guess_diff = abs(p1_secret - secret_guess)
    feedback = ''
    j='judge'
    crsr.execute("select tolerance from [dbo].[game_settings] where name = '"+j+"'")
    tolerance = crsr.fetchall()[0][0]
    print('tolerance=',tolerance)
    # give feedback to P99
    tol_high = p1_secret + tolerance
    tol_low = p1_secret - tolerance
    print('tol_high',tol_high,'tol_low',tol_low)
    
    if secret_guess == p1_secret:
        feedback = 'You guessed exact value (+50 points)'
    elif secret_guess > tol_low and secret_guess < tol_high:
        feedback = 'You guessed within tolerance (+10 points)'
    else:
        feedback = 'try again'
    
    return render_template('player99.html',feedback=feedback)


@app.route('/play', methods=['POST'])
def play():
    p1_name = request.form['p1_name']
    p99_name = request.form['p99_name']
    low_range = int(request.form['low_range'])
    high_range = int(request.form['high_range'])
    tolerance = int(request.form['tolerance'])
    countdown = int(request.form['countdown'])
    
    # generate a random secret value
    secret_value = random.randint(low_range, high_range)
    
    # initialize variables
    guess = None
    guess_diff = None
    score = 0
    
    # start countdown timer
    start_time = time.time()
    
    # loop until time is up or guess is within tolerance
    while guess_diff is None or guess_diff > tolerance:
        # get guess from P99
        guess = int(request.form['guess'])
        
        # calculate difference between guess and secret value
        guess_diff = abs(secret_value - guess)
        
        # give feedback to P99
        if guess_diff > tolerance:
            if guess < secret_value:
                feedback = 'Low'
            else:
                feedback = 'High'
        else:
            feedback = None
        
        # check if time is up
        elapsed_time = time.time() - start_time
        if elapsed_time >= countdown:
            break
    
    # calculate score
    if guess_diff <= tolerance:
        if guess == secret_value:
            score = 50
        else:
            score = 10
    
    # render results template
    return render_template('results.html', p1_name=p1_name, p99_name=p99_name, 
                           secret_value=secret_value, guess=guess, feedback=feedback, 
                           score=score, elapsed_time=elapsed_time)
    

if __name__ == '__main__':
    app.run(debug=True)