from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def home(request):
	emenities = Emenitites.objects.all()
	context = {'emenities': emenities}
	return render(request, 'home.html', context)

@login_required(login_url="/login/")
def api_blogs(request):
	blogs_objs = Blog.objects.all()
	
	price = request.GET.get('price')
	if price :
		blogs_objs = blogs_objs.filter(price__lte=price) 
		
	emenities = request.GET.get('emenities')
	if emenities:
		emenities = emenities.split(',')
		em = []
		for e in emenities:
			try:
				em.append(int(e))
			except Exception as e:
				pass
		# print(em)
		blogs_objs = blogs_objs.filter(emenities__in=em).distinct()
	payload = []
	for blog_obj in blogs_objs:
		result = {}
		result['blog_name'] = blog_obj.blog_name
		result['blog_description'] = blog_obj.blog_description
		result['price'] = blog_obj.price
		payload.append(result)
		
	return JsonResponse(payload, safe=False)

def login_page(request):
	if request.method == "POST":
		
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user_obj = User.objects.filter(username=username)
			if not user_obj.exists():
				messages.error(request, "Username not found")
				return redirect('/login/')
			user_obj = authenticate(username=username, password = password)
			if user_obj:
				login(request, user_obj)
				return redirect('/')
			messages.error(request, "Wrong Password")
			return redirect('/login/')
			
		except Exception as e:
			messages.error(request, " Somthing went wrong")
			return redirect('/register/')
		
	return render(request, "login.html")


def register_page(request):
	if request.method == "POST": 
		try: 
			username = request.POST.get('username')
			password = request.POST.get('password')
			user_obj = User.objects.filter(username=username)
			if user_obj.exists():
				messages.error(request, "Username is taken")
				return redirect('/register/')
			user_obj = User.objects.create(username=username)
			user_obj.set_password(password)
			user_obj.save()
			messages.success(request, "Account created")
			return redirect('/login/')

		except Exception as e:
			messages.error(request, " Somthing went wrong")
			return redirect('/register/')
		
	return render(request, "register.html")
