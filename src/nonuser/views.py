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


BASE_DIR = Path(__file__).resolve().parent.parent
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, "FireBase_Creds\\KeyFile.json")

config =  {
  "apiKey" : "AIzaSyA5Du-AtnXcSQ1FSXTBS8iekZMegj3BpLY",
  "authDomain" : "pacmanbytes-8b0c7.firebaseapp.com",
  "databaseURL" : "https://pacmanbytes-8b0c7-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId" : "pacmanbytes-8b0c7",
  "storageBucket" : "pacmanbytes-8b0c7.appspot.com",
  "messagingSenderId" : "225279737696",
  "appId" : "1:225279737696:web:e12a66d59c760ab8a2e805",
  "measurementId": "G-PEDDL109QZ",
  "serviceAccount": os.path.join(BASE_DIR, "FireBase_Creds\\KeyFile.json"),
}



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
	
def homeView(request, *args, **kwargs):
	user_name, logged_in, user_uid = checkLogIn(request)
	context = {
		"user_name":user_name[:17],
		"logged_in":logged_in,
		"def_pin": "574101",
		"user_type": "3",
		"toggle": 1,
	}
	if(logged_in):
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		context["user_type"] = user["User_Type"]
		context['def_pin'] = user["Pin_Code"]

	if request.method == "POST":
		pin_filter = request.POST.get("pinFilter")
		print(pin_filter)
		if(pin_filter):
			context["def_pin"] = pin_filter
	
	print(context["def_pin"])

	stores = []
	user_ref = FireStore.collection(u'Users')
	for doc in user_ref.stream():
		this_user = doc.to_dict()
		#print(this_user)
		if(this_user["User_Type"] == '2' and this_user["Pin_Code"] == context["def_pin"]):
			stores.append(this_user)

	print(stores)

	context["stores"] = stores

	return render(request, 'home_view.html', context)

def itemsView(request, *args, **kwargs):
	return

def profileView(request, *args, **kwargs):
	redirect_auth = redirect('/auth/')
	redirect_home = redirect('/home/')

	base = Path(__file__).resolve().parent.parent
	image_dir = os.path.join(base, "ExampleImages\\users")

	user_name, logged_in, user_uid = checkLogIn(request)
	context = {
		"user_name":user_name[:17],
		"logged_in":logged_in,
		"def_pin": "574101",
		"user_type": "3",
		"toggle": 0,
	}

	if(logged_in):
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		context["user_type"] = user["User_Type"]
		context['def_pin'] = user["Pin_Code"]
		context["user_data"] = user
	else:
		return redirect_auth
	print(1)
	up_user_name = request.POST.get("upUserName")
	up_pin_code = request.POST.get("upPinCode")
	up_gst = request.POST.get("upGst")
	up_img = request.POST.get("upImg")
	if(up_user_name and up_pin_code):
		try:
			user_old = FireStore.collection(u'Users').document(user_uid).get().to_dict()
			if(up_img):
				image_dir = os.path.join(image_dir, up_img)
				storage = fireBase.storage()
				img_id = uuid.uuid1()
				storage.child("profile_img/"+str(img_id.hex)+".jpg").put(image_dir)
				img_url = storage.child("images/"+str(img_id.hex)+".jpg").get_url(None)
				user_old["Img_Url"] = img_url

			user_old["User_Name"] = up_user_name
			user_old["Pin_Code"] = up_pin_code
			if(up_gst):
				user_old["GSTIN"] = up_gst
			FireStore.collection(u'Users').document(user_uid).set(user_old)
			return redirect_home
		except Exception as e:
			print(e)
			messages.error(request, "Network Error", extra_tags = "NETWORK_ERROR_UPDATE")

	else:
		messages.error(request, "Enter all the fields", extra_tags = "INSUFFICIENT_DATA_UPDATE") 

	return render(request, 'edit_profile_form.html', context)

def searchView(request, *args, **kwargs):
	redirect_auth = redirect('/auth/')
	redirect_home = redirect('/home/')

	user_name, logged_in, user_uid = checkLogIn(request)
	context = {
		"user_name":user_name[:17],
		"logged_in":logged_in,
		"def_pin": "574101",
		"user_type": "3",
		"toggle": 0,
	}

	if(logged_in):
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		context["user_type"] = user["User_Type"]
		context['def_pin'] = user["Pin_Code"]
		context["user_data"] = user
	else:
		return redirect_auth

	return render(request, 'customer-store-search.html', context)

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