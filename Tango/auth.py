from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, SignUpForm
from .models import User
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

bd = Blueprint('auth',__name__)

@bd.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    error = None

    if(form.validate_on_submit()):
       print('Form validated')
       user_email = form.email.data
       password = form.password.data
       u1 = User.query.filter_by(email = user_email).first()
       print(user_email)
       print(password)
       print(check_password_hash(u1.password_hash, password)) 
         #if there is no user with that email
       if u1 is None:
        error = "no account assosiated with that email"

        #if password does not match    
       elif not check_password_hash(u1.password_hash, password):
        error = "Incorrect Password"

       if error is None:
         print("user is logged in")
         #login user
         login_user(u1)
         return redirect('/')
        
       else:
         print(error)
         flash(error)
        
    return render_template('Login.html', form=form)

@bd.route('/logout')
def logout():
   logout_user()
   return redirect('/')

@bd.route('/signup', methods=['GET', 'POST'])
def signup():
    SignUp_form = SignUpForm()
    if SignUp_form.validate_on_submit():
        print("Form has been Validated")

        f_name = SignUp_form.first_name.data
        l_name = SignUp_form.last_name.data
        user_number = SignUp_form.phone.data
        user_email = SignUp_form.email.data
        pwd_hash = generate_password_hash(SignUp_form.password.data)
        user_address = SignUp_form.address.data

        new_user = User(first_name=f_name, 
                        last_name=l_name,
                        phone_number=user_number, 
                        email=user_email, 
                        password_hash=pwd_hash,
                        address=user_address)
        
        
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    return render_template('SignUp.html', form=SignUp_form)

