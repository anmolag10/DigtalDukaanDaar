from django.shortcuts import render

# Create your views here.
def storesView(request, *args, **kwargs):
	return
def homeView(request, *args, **kwargs):
	return render(request, 'dummy.html')

def itemsView(request, *args, **kwargs):
	return

def profileView(request, *args, **kwargs):
	return render(request, 'edit_profile_form.html')


def aboutView(request, *args, **kwargs):
	return