from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def new(request):
    try:
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=sub.email,
            subject='Newsletter Confirmation',
            html_content='Thank you for signing up for my email newsletter! Please complete the process by <a href="http://127.0.0.1:8000/confirm/?email={}&conf_num={}">clicking here to confirm your registration</a>.'.format(sub.email, sub.conf_num))
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return HttpResponse(status=201)
    except:
        return HttpResponse(status=500)


def confirm(request):
    try:
        sub = Subscriber.objects.get(email=request.GET['email'])
        if sub.conf_num == request.GET['conf_num']:
            sub.confirmed = True
            sub.save()
            return render(request, 'index.html', {'email': sub.email, 'action': 'confirm'})
        else:
            return render(request, 'index.html', {'email': sub.email, 'action': 'deny'})
    except:
        return render(request, 'index.html')

def delete(request):
    try:
        sub = Subscriber.objects.get(email=request.GET['email'])
        if sub.conf_num == request.GET['conf_num']:
            sub.delete()
            return render(request, 'index.html', {'email': sub.email, 'action': 'delete'})
        else:
            return render(request, 'index.html', {'email': sub.email, 'action': 'deny'})
    except:
        return render(request, 'index.html')
