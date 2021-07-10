from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth as dj_auth
import os
from pathlib import Path
import uuid
from google.cloud import firestore
import pyrebase

# allows you to import stuff from higer levels #
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), '..'))
# allows you to import stuff from higer levels #
import utils


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

# global vars #


def checkLogIn(request):
	user_name = ""
	user_uid = ""
	if(not utils.check_key(request.session, 'uid')):
		logged_in = 0
	else:
		user_uid = request.session['uid']
		logged_in = 1
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["User_Name"]

	return user_name, logged_in, user_uid

# Create your views here.
def storesView(request, *args, **kwargs):
	return
	
def homeView(request, *args, **kwargs):
	user_name, logged_in, user_uid = checkLogIn(request)
	context = {
		"user_name":user_name,
		"logged_in":logged_in,
		"def_pin": 574101,
	}
	if(logged_in):
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		request.session["curr_pin"] = user["Pin_Code"]
		context['def_pin'] = user["Pin_Code"]
		

	return render(request, 'home_view.html', context)

def itemsView(request, *args, **kwargs):
	return

def profileView(request, *args, **kwargs):
	return render(request, 'edit_profile_form.html')

def aboutView(request, *args, **kwargs):
	return

def redirectHome(request, *args, **kwargs):
	redirect_home = redirect('/home/')
	return redirect_home

def logout(request):
	if(not utils.check_key(request.session, 'uid')):
		return redirect("/auth/")
	else:
		user_uid = request.session['uid']
	dj_auth.logout(request)
	return redirect('/home/')