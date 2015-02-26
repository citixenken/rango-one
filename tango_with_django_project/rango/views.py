from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.bing_search import run_query
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import redirect

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):

	#Query the database  for a list of all categories currently stored.
	#Order categories by no. likes in descending order
	#Retrieve top 5 only - or all if less than 5
	#Place list in our context_dict dictionary which will be passed to the template engine
	
	#category_list = Category.objects.order_by('-likes')[:5]
	#context_dict = {'categories':category_list}
	
	#context_dict = {'boldmessage':"I am bold font from the context"}
	
	#return render(request, 'rango/index.html', context_dict)
	
	#return HttpResponse("Rango says heeey there WORLD!! <br/> <a href='/rango/about'> About </a>")
	
	#category_list = Category.objects.all()
	category_list = Category.objects.order_by('-likes')[:7]
	page_list = Page.objects.order_by('-views')[:7]
	
	context_dict = {'categories': category_list, 'pages': page_list}
	
	#get the number of visits to the site.
	#we use the COOKIES.get() function to obtain the visits cookie.
	#if the cookie exists, the value returned is casted to an integer.
	#if the cookie doesnt exist, we default to zero and cast that.
	#visits = int(request.COOKIES.get('visits', '1'))
	
	visits = request.session.get('visits')
	
	if not visits:
		visits = 1
	reset_last_visit_time = False
	
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).seconds > 0:
			#...reassign the value of the cookie to +1 of what it was before...
			visits = visits + 1
			#...and update the last visit cookie too.
			reset_last_visit_time = True
			
	else:
		#cookie last_visit doesnt exist so create it to the current date/time.
		reset_last_visit_time = True
			
	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	context_dict['visits'] = visits
	
	
	response = render(request, 'rango/index.html', context_dict)
	
	return response
	
	#reset_last_visit_time = False
	#response = render(request, 'rango/index.html', context_dict)
	#does the cookie last visit exist?
	#if 'last_visit' in request.COOKIES:
		#yes it does! get the cookie's value.
	#	last_visit = request.COOKIES['last_visit']
		#cast the value to a python date/time object.
	#	last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		
		#if its been more than a day since the last visit...
	#	if (datetime.now() - last_visit_time).days > 0:
	#		visits = visits + 1
			#and flag that the cookie last visit needs to be updated.
	#		reset_last_visit_time = True
			
	#else:
		#cookie last visit doesnt exist,so flag that it should be set.
	#	reset_last_visit_time = True
		
	#	context_dict['visits'] = visits
		
		#obtain our Response object early so we can add cookie info.
	#	response = render(request, 'rango/index.html', context_dict)
		
	#if reset_last_visit_time:
	#	response.set_cookie('last_visit', datetime.now())
	#	response.set_cookie('visits', visits)
		
	#return response back to user, updating any cookies that need changed.
	#return response

def about(request):
	context_dict = {'boldmessage':"I am bold font from the context"}
	
	# If the visits session varible exists, take it and use it.
	# If it doesn't, we haven't visited the site so set the count to zero.
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0

	# remember to include the visit data
	return render(request, 'rango/about.html', {'visits': count})
	
	#return render(request, 'rango/about.html', context_dict)
	
	#return HttpResponse("Rango says here is the about page <br/> <a href='/rango/'> Index </a>")
	
def category(request, category_name_slug):
	
		
	#create a context dictionary which we can pass to the template rendering engine.
	context_dict = { 'category_name_slug': category_name_slug }
	#context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None
	if request.method == 'POST':
		query = request.POST['query'].strip()
		
		if query:
			#run your bing fn to get results list.
			result_list = run_query(query)
			
			context_dict['result_list'] = result_list
			context_dict['query'] = query
			
	
	try:
	
		#can we find a category name slug with the given name?
		#if we cant, the .get() method raises a DoesNotExist exception.
		#so the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug = category_name_slug)
		
		context_dict['category_name'] = category.name
		
		#retrieve all of the associated pages.
		#note that filter returns >=1 model instance.
		pages = Page.objects.filter(category = category).order_by('-views')
		
		#adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		#we also add the category object from the database to the context dictionary.
		#we'll use this in the template to verify that the category exists.
		context_dict['category'] = category
		
		
	except Category.DoesNotExist:
		#we get here if we didnt find the specified category.
		#dont do anything - the template displays the 'no category' message for us.
		pass
	
	if not context_dict['query']:
		context_dict['query'] = category.name
		
	#go render the response and return it to the client.
	
	return render(request, 'rango/category.html', context_dict)
	

def add_category(request):
	#a http post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		#have we been provided with a valid form?
		if form.is_valid():
			#save new category to database.
			form.save(commit=True)
			#print cat, cat.slug
			
			#now call the index() view.
			#user will be shown the homepage.
			return index(request)
		else:
			#the supplied form contained errors - print them to the terminal.
			print form.errors
	else:
		#if request was not a POST, display form to enter details.
		form = CategoryForm()
		
	#bad form (or form details), no form supplied ...
	#render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})
	
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None
		
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views =0
				page.save()
				
				#probably better to use a redirect here.
				return category(request, category_name_slug)
				
		else:
			print form.errors
	else:
		form = PageForm()
		
	context_dict = {'form':form, 'category':cat}
	
	return render(request, 'rango/add_page.html', context_dict)
	
def register(request):
	
	
	#a boolean value for telling the template whether the registration was successful.
	#set to False initially. Code changes value to True when registration succeeds.
	
	registered = False
	
	#if it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		#attempt to grab data from raw form info.
		#we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		#if the two forms are valid....
		if user_form.is_valid() and profile_form.is_valid():
			#save user's form to the database.
			user = user_form.save()
			
			#now we hash the password with the set_password method.
			#once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			
			#now sort out UserProfile instance.
			#since we need to set the user attribute ourselves, we set commit=False.
			#this delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user
			
			#did user provide a profile picture?
			#if so, we need to get it from the input form and put in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			#now we save the UserProfile model instance.
			profile.save()
			
			#update our variable to tell the template registration was successful.
			registered = True
			
		#invalid form or forms - mistakes or something else?
		#print problems to the terminal.
		#they will also be shown to the user.
		else:
			print user_form.errors, profile_form.errors
			
	#not a HTTP POST, so we render our form using two ModelForm instances.
	#these forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	#render the template depending on the context.
	return render(request,
			'rango/register.html',
			{'user_form':user_form, 'profile_form':profile_form,'registered':registered})
			
def user_login(request):

	#if the request is a HTTP POST, try to pull out the relevant info.
	if request.method == 'POST':
		#gather username and password provided by user.
		#this info is obtained from login form.
		username = request.POST['username']
		password = request.POST['password']
		
		#use django machinery to attempt to see if the username/password
		#combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		
		#if we have a User object, the details are correct.
		#if None (python's way of representing the absence of a value), no 
		#user with matching credentials was found.
		if user:
			#is the account active? it could have been disabled.
			if user.is_active:
				#if the account is valid and active, we can log the user in.
				#we'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				#an inactive account was used - no logging in!
				return HttpResponse("Your Rango Account is disabled.")
		else:
			#bad login details were provided, so we cant log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
			
	#the request is not a HTTP POST, so display the login form.
	#this scenario will most likely be a HTTP GET.
	else:
		#no context variables to pass to the template system, hence the blank
		#dictionary object...
		return render(request, 'rango/login.html',{})


@login_required
def restricted(request):
	#return HttpResponse("Since you're logged in, you can see this text!")
	return render(request, 'rango/restricted.html',{})

#use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	#since we know the user is logged in, we can now just log them out.
	logout(request)
	
	#take user back to the homepage.
	return HttpResponseRedirect('/rango/')
	
#def search(request):
	
	#result_list = []
	
	#if request.method == 'POST':
		#query = request.POST['query'].strip()
		
		#if query:
		#	#run our bing function to get the results list!
		#	result_list = run_query(query)
			
	#return render(request, 'rango/search.html', { 'result_list': result_list})
	

def track_url(request):
	page_id = None
	url = '/rango/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	
	return redirect(url)

	
@login_required
def like_category(request):
	
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		
	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()
			
	return HttpResponse(likes)
	
	
def get_category_list(max_results = 0, starts_with = ''):
	cat_list = []
	if starts_with:	
		cat_list = Category.objects.filter(name__istartswith=starts_with)
		
	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]
			
	return cat_list


def suggest_category(request):
		cat_list = []
		starts_with = ''
		if request.method == 'GET':
			starts_with = request.GET['suggestion']
			
		cat_list = get_category_list(8, starts_with)
		
		return render(request, 'rango/cats.html', {'cat_list': cat_list})
		
		
@login_required
def auto_add_page(request):
    #context = RequestContext(request)
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)

            pages = Page.objects.filter(category=category).order_by('-views')

            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages

    return render_to_response('rango/page_list.html', context_dict, context)