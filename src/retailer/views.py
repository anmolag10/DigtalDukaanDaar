from django.shortcuts import render, redirect
import os
from pathlib import Path
import uuid
from google.cloud import firestore
import pyrebase
from django.contrib import messages
from django.http import HttpResponseRedirect

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
def cartView(request):
	return

def supplyView(request):
	return

def itemsView(request):
	return

def createProductView(request):

	redirect_home = redirect('/home/')
	redirect_auth = redirect('/auth/')

	user_name, logged_in, user_uid = checkLogIn(request)

	context = {
		"user_name":user_name[:17],
		"logged_in":logged_in,
		"def_pin": 574101,
		"user_type": "3",
	}

	if(not logged_in):
		return redirect_auth
	else:
		user = FireStore.collection(u'Users').document(user_uid).get().to_dict()
		context["user_type"] = user["User_Type"]
		context['def_pin'] = user["Pin_Code"]
		if(user['User_Type'] not in ["1","2"] ):
			return redirect_home



	prod_name = request.POST.get("prodName")
	prod_desc = request.POST.get("prodDesc")
	prod_price = request.POST.get("prodPrice")
	prod_cat = request.POST.get("prodCategory")
	prod_type = request.POST.get("prodType")
	prod_quant = request.POST.get("prodQuatity")

	if(prod_name and prod_desc and prod_price and prod_cat and prod_quant and prod_type):
		try:
			gen_id = uuid.uuid1()
			product = {
				"Product_Id": str(gen_id.hex),
				"Product_Name": prod_name,
				"Prodct_Desc": prod_desc,
				"Product_Price": prod_price, 
				"Product_Category": prod_cat,
				"Product_Type": prod_type,
				"Product_Quantity": prod_quant,
				"Seller_Uid": user_uid,
			}
			Fire_Store.collection(u'Blog-Posts').document(str(gen_id.hex)).set(Blog_Post)
			return HttpResponseRedirect("/retailer/manage_items/")

		except Exception as e:
			print(e)
			messages.error(request, "Network Error", extra_tags = "NETWORK_ERROR")

	else:
		messages.error(request, "Enter all the fields", extra_tags = "INSUFFICIENT_DATA_PRODUCT")


	return render(request, 'Retailer/retailform.html', context)


def manageItemView(request):
	return render(request, 'Retailer/Manage-Items.html')

def analyticsView(request):
	return