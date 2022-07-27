from crypt import methods
from flask import Flask
from flask_app import app
from flask import render_template, session, redirect,request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.User import User


@app.route('/')
def test():
    return render_template('index.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/login_page')
def login_page():
    return render_template('log_in.html')

# register stuff

@app.route('/register', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    if not User.validate(request.form):
        return redirect('/register_page')
    data = {
        'first_name':request.form['first_name'],
        'gender':request.form['gender'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password': pw_hash,
        'confirm':request.form['confirm']
    }
    user_id = User.save(data)
    session['user_id']=user_id
    return redirect('/dash')

@app.route('/dash')
def main_page():
    if 'user_id' not in session:
        return redirect('/')
    else:
        id={"id":session['user_id']}
        
        logged_user= User.get_by_id(id)
        
        
    return render_template('main_page.html', users=logged_user)

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    data = {'email':request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid email or password')
        return redirect('/login_page')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email or password')
        return redirect('/login_page')
    session['user_id']=user_in_db.id
    return redirect('/dash')
