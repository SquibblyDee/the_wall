from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib import auth

import bcrypt

#  import our db
from .models import Users

def index(request):
    return render(request,'the_wall_app/index.html')

def process_register(request, methods=['POST']):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Users.objects.basic_validator(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/', id)
    else:
        # if the errors object is empty, that means there were no errors!
        # add our new record to the table , push what we need to session,
        # and redirect to /success to render our final page
        Users.objects.create(first_name=request.POST['input_first_name'], last_name=request.POST['input_last_name'], email=request.POST['input_email'], password=bcrypt.hashpw(request.POST['input_password'].encode('utf8'), bcrypt.gensalt()))
        query = Users.objects.filter(email=request.POST['input_email']).values('id')
        for row in query:
            request.session['isloggedin'] = row['id']
        request.session['welcomename'] = request.POST['input_first_name']
        request.session['welcomemessage'] = 'Successfully registered!'
        return redirect('/wall')

def process_login(request, methods=['POST']):
    # Query the data we need
    query = Users.objects.all().values('id', 'email', 'first_name', 'password')
    # Iterate through query until we find user email then verify password is legit
    for row in query:
        if row['email'] == request.POST['login_email'] and bcrypt.checkpw(request.POST['login_password'].encode(), row['password'].encode()): 
            request.session['isloggedin'] =  row['id']
            request.session['welcomename'] = row['first_name']
            request.session['welcomemessage'] = 'Successfully logged in!'
            return redirect('/wall')
    return redirect('/')

def process_post(request, methods=['POST']):
    print("WE IN PROCESSSSSS POSTTTTT")
    return redirect('/')

def success(request):
    # If the user has a isLoggedin session 
    if 'isloggedin' in request.session and request.session['isloggedin'] == True:
        return render(request,'the_wall_app/wall.html')
    else:
        return redirect('/')

def wall(request):
    
    return render(request,'the_wall_app/wall.html')

# Just clears out session
def logout(request):
    auth.logout(request)
    return redirect('/')