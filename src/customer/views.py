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


def cartView(request):
	return


def storesView(request, store_id, *args, **kwargs):
	redirect_auth = redirect("/auth/")

	user_name, logged_in, user_uid = checkLogIn(request)
	context = {
		"user_name":user_name[:17],
		"logged_in":logged_in,
		"def_pin": 574101,
		"user_type": "3",
		"toggle": 0,
	}
	if(logged_in):
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		context["user_type"] = user["User_Type"]
		context['def_pin'] = user["Pin_Code"]
	else:
		return redirect_auth

	retail_products_ref = FireStore.collection(u'Retail_Product')
	products = []
	for doc in retail_products_ref.stream():
		product = doc.to_dict()
		if(product["Seller_Uid"] == store_id):
			products.append(product)

	store = FireStore.collection(u'Users').document(store_id).get().to_dict()
	context["products"] = products
	context["store_name"] = store["User_Name"]

	return render(request, 'customer-store-item.html', context)

def itemsView(request):
	return
