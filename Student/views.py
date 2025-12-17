from django.shortcuts import render,redirect,HttpResponse
from Common.models import student_registration,quiz
from Common.forms import student_registrationForm,quizForm
from .util import send_email
import random

def stlogin(request):
    reg=student_registrationForm()
    return render(request,"stlogin.html",{'forms':reg})
    


def stregister(request):
    regs=student_registrationForm()
    return render(request,"stregister.html",{'forms':regs})
def passwordchange(request):
    return render(request,"passwordchange.html")
def quizattempt(request):
    questions = quiz.objects.all()
    return render(request, "quizattempt.html", {"questions": questions})
       
def pyq(request):
    return render(request,"pyq.html")    

def home(request):
    return render(request,"shome.html")    


def email_otp(request):
    return render(request,'email_otp.html')

def student_email_page(request):
    if request.method == "POST":
        form = student_registrationForm(request.POST)
        email = request.POST.get('email_id')
        print(email)
        
        try:
            student=student_registration.objects.get(email_id = email)
            request.session['email_id'] = student.email_id
            subject="quiz app password reset"
            otp=random.randint(1000,9999)
            body=f"otp for your password reset = {otp}"
            sent = send_email(email,subject,body)
            return HttpResponse("otp sended")
        except student_registration.DoesNotExist:
            return HttpResponse("no student in this email id")





# password reset


      



def student_reg(request):
    if request.POST:

      form = student_registrationForm(request.POST)
      if form.is_valid():
        form.save()
        return HttpResponse("registerd")
    return HttpResponse("invalid")
def sloginaction(request):
    
    if request.method == "POST":
       roll_no= request.POST.get('roll_no')
       password=request.POST.get('password')

   
      
    try:
                student = student_registration.objects.get(roll_no=roll_no,password=password)
                request.session['roll_no']=student.roll_no
                request.session['password']=student.password
                return redirect('student_home')
    except student_registration.DoesNotExist:
                
      return HttpResponse("invalid login")     


# Create your views here.



