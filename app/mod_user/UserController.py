from flask import render_template,Flask, session, redirect, url_for, escape, request,g
import json
from app.mod_user.User import User
from app.mysql.MysqlService import MysqlService
from app import app


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    id = request.form['userid']
    name = request.form['username']
    password = request.form['password']
    phone = request.form['userphone']
    role = request.form['userrole']
    user = User(id, password, name, phone, role)
    # add this  user to database
    mysql = MysqlService()
    mysql.addUser(id, password, name, phone, role)
    return render_template('login.html')


@app.route('/user/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    print(request.get_data())
    session['userid']=request.form['username']
    print('save userid in session ')
    id = request.form['username']
    password = request.form['password']
    # get the password from database
    mysql = MysqlService()
    rea_pass = mysql.getPassById(id)
    print(id)
    print(rea_pass)
    if password == rea_pass:
        return redirect(url_for('search_goods'))
    else:
        return render_template('fail.html')

@app.route('/user/logout')
def logout():
    session.pop('userid',None)
    return redirect(url_for('login'))

@app.route('/user/edit', methods=['GET', 'POST'])
def editUser():
    id = request.form['userid']
    username = request.form['username']
    userphone = request.form['userphone']
    mysql = MysqlService()
    mysql.UpdateMessage(username,userphone, id)
    if hasattr(g, 'userid'):
        return redirect(url_for('userInfor'))




