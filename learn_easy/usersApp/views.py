from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import OneTimeToken, CustomUser
from django.contrib.auth import login


def login_request(request: HttpRequest) -> HttpResponse:
    """
    Handle login request and send a one-time login link via email.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Response for rendering a page.
    """
    if request.method == 'POST':
        email = request.POST['email']
        user, created = CustomUser.objects.get_or_create(email=email)
        token = OneTimeToken.objects.create(user=user)
        login_url = request.build_absolute_uri(reverse('login_link')) + '?token=' + str(token.token)
        send_mail('Your login link', login_url, 'from@example.com', [email])
        return render(request, 'account/login_request_sent.html')
    else:
        return render(request, 'account/login_request.html')

def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle login using a one-time token.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Response for rendering a page.
    """
    token = request.GET.get('token')
    if token is not None:
        try:
            token = OneTimeToken.objects.get(token=token)
            if token.is_valid():
                login(request, token.user)
                token.delete()
                return redirect('dashboard')
            else:
                return render(request, 'account/login_link.html', {'error': 'Invalid or expired login link.'})
        except OneTimeToken.DoesNotExist:
            pass
    return render(request, 'account/login_link.html', {'error': 'Invalid login link.'})
