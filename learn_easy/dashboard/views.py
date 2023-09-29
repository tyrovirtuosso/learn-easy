from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pprint import pprint
import re


@login_required
def dashboard(request):
    user = request.user
    
    # Check if the user has a first name
    if user.first_name:
        display_name = user.first_name
    else:
        # If the user doesn't have a first name, use the part of the email before the '@' symbol
        email_parts = re.split('@', user.email)
        display_name = email_parts[0]

    context = {'user': user, 'display_name': display_name}
    return render(request, 'dashboard/dashboard.html', context)