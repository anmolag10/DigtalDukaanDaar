from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth as dj_auth
import os
from pathlib import Path
import uuid
from google.cloud import firestore
import pyrebase

# fire-base init
config =  {
  "apiKey" : "AIzaSyA5Du-AtnXcSQ1FSXTBS8iekZMegj3BpLY",
  "authDomain" : "pacmanbytes-8b0c7.firebaseapp.com",
  "databaseURL" : "https://pacmanbytes-8b0c7-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId" : "pacmanbytes-8b0c7",
  "storageBucket" : "pacmanbytes-8b0c7.appspot.com",
  "messagingSenderId" : "225279737696",
  "appId" : "1:225279737696:web:e12a66d59c760ab8a2e805",
  "measurementId": "G-PEDDL109QZ"
}
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, "FireBase_Creds\\KeyFile.json")
print(os.path.join(BASE_DIR, "FireBase_Creds\\KeyFile.json"))
fireBase = pyrebase.initialize_app(config)
fb_auth = fireBase.auth()
dataBase = fireBase.database()
FireStore = firestore.Client()

# Redirecting variables #




def authView(request, *args, **kwargs):
	return render(request, "auth/auth_page.html")

def postAuthView(request, is_signin, *args, **kwargs):

	# Redirecting variables #
	redirect_auth = redirect('/auth/')
	redirect_home = redirect('/home/')
	# sign in #
	if(is_signin == '1'):
		email = request.POST.get("signInEmail")
		password = request.POST.get("signInPassword")
		if(email and password):
			try:
				user = fb_auth.sign_in_with_email_and_password(email, password)
			except Exception as e:
				messages.error(request, "Invalid credentials", extra_tags = "INVALID_CREDS_SIGNIN")
				return redirect_auth
		else:
			messages.error(request, "Enter the required fields", extra_tags = "INSUFFICIENT_DATA_SIGNIN")
			return redirect_auth

	# sign up #
	else:
		
		pin_code = request.POST.get('pinCode')
		user_name = request.POST.get('userName')
		new_email = request.POST.get('signUpEmail')
		new_password = request.POST.get('signUpPassWord')
		user_type = request.POST.get('userType')
		
		if(user_name and new_email and new_password and pin_code and user_type):
			try:
				user = fb_auth.create_user_with_email_and_password(new_email, new_password)

				#adding the user into the database
				uid = user['localId']
				data = {u"User_Name": user_name, 
						u"Uid":uid, 
						u"Email": new_email,
						u"User_Type": user_type,
						}
				fb_auth.send_email_verification(user['idToken'])
				FireStore.collection(u'Users').document(uid).set(data)
				

			except Exception as e:
				print(e)
				messages.error(request, "Invalid credentials", extra_tags = "INVALID_CREDS_SIGNUP")
				return redirect_auth

		else:
			messages.error(request, "Enter the required fields", extra_tags = "INSUFFICIENT_DATA_SIGNUP")
			return redirect_auth

	session_id = user["localId"]
	request.session["uid"] = str(session_id)
	return redirect_home


