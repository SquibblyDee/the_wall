from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

#  import our db
#from .models import User

def index(request):

    return render(request,'the_wall_app/index.html')