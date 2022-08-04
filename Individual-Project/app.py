from flask import session as login_session
import pyrebase
from flask import Flask, render_template, request, redirect, url_for, session

import re
config = {
  "apiKey": "AIzaSyCX84OrQELbghcSHyPrTHWYfhXkDoHRCGg",
  "authDomain": "no-one-know.firebaseapp.com",
  "projectId": "no-one-know",
  "storageBucket": "no-one-know.appspot.com",
  "messagingSenderId": "406182260968",
  "appId": "1:406182260968:web:cd452a6a3db6e32319995d",
  "measurementId": "G-WV1ZB2P2GH",
  "databaseURL": "https://no-one-know-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



@app.route('/', methods=['GET', 'POST'])
def mainpage():
	return render_template("mainpage.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error=""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session ["user"] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('shop'))
		except:
			error = "Authentication failed"
		
	return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error=""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		try:
			user = {"name": name, "email":email, "password": password}
			login_session['user'] = auth.create_user_with_email_and_password(email,password)
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('shop'))

		except:
			error = "Sign up failed. Maybe user exists already?"

	return render_template("signup.html",error=error)


@app.route('/shop', methods=['GET', 'POST'])
def shop():
	user = db.child("Users").child(login_session['user']['localId']).get().val()
	return render_template("shop.html",name=user["name"])



if __name__ == '__main__':
	app.run(debug=True)