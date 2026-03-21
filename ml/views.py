import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from .models import 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import logging
from django.shortcuts import render, Http404
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from .models import Result

def home(request) :
    return render(request,"ml/home.html")