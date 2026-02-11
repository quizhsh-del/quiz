from django.shortcuts import render,redirect,HttpResponse
from Common.models import FeedbackAndNotification
from Common.forms import FeedbackAndNotificationForm

def Performance(request):
    return render(request,"performance.html")  

# Create your views here.
def feedback(request):
    fb=FeedbackAndNotificationForm()
    return render(request,"feedback.html",{'form':fb})

def feedback_action(request):
    if request.method == "POST":
        form = FeedbackAndNotificationForm(request.POST)
        if form.is_valid():
         form.save()
    return HttpResponse("feedback submitted")     

def header_c(request):
    return render(request,"header_c.html",)

def commonhome(request):
    return render(request,"commonhome.html",)
