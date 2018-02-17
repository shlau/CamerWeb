import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL
import bcrypt
app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'surpass1'
app.config['MYSQL_DB'] = 'Camer'
app.config['MYSQL_CURSORCLASS']='DictCursor'

@app.route('/home')
def homepage():
    return 'SUCCESS'
@app.route('/', methods = ['POST','GET'])
def login():
    if(request.method == 'POST'):
        enteredUsername = request.form['username']
        enteredPassword = request.form['password']
        cur = mysql.connection.cursor()
        res = cur.execute("SELECT * FROM users WHERE name = %s", [enteredUsername])
        if res > 0:
            data = cur.fetchone()
            hashedPass = data['password']
            if bcrypt.checkpw(enteredPassword.encode('utf-8'),hashedPass.encode('utf-8')):
                return redirect(url_for('homepage'))
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/register', methods = ['POST','GET'])
def register():
    if(request.method == 'POST'):
        app.logger.info('posting')
        username = request.form['username']
        password = request.form['password']
        app.logger.info('%s registered in successfully', username)
        hashedpw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(name,password) VALUES(%s,%s)', (username, hashedpw))
  
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    else:
        app.logger.info('unsuccessful registration')
        return render_template('register.html')
if __name__ == "__main__":
    app.run(debug=True)
