from django.shortcuts import render,redirect,HttpResponse
from Common.models import student_registration,quiz, result,question_bank,questions
from Common.forms import student_registrationForm,quizForm,PYQFilterForm
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
    roll_no = request.session.get('roll_no')

    if not roll_no:
        return HttpResponse("Login required")

    student = student_registration.objects.get(roll_no=roll_no)

    difficulty = request.session.get('difficulty')

    if not difficulty:
        return redirect('select_option')

    questions = quiz.objects.filter(Difficulty_Level=difficulty)

    if request.method == "POST":
        score = 0
        correct = 0
        wrong = 0

        for q in questions:
            selected = request.POST.get(q.question_id)
            if selected == q.correct_option:
                correct += 1
                score += 1
            elif selected:
                wrong += 1

        remarks = "PASS" if score >= questions.count() / 2 else "FAIL"

        result.objects.create(
            roll_no=student,
            score=score,
            correct_answer=correct,
            wrong_answer=wrong,
            remarks=remarks
        )

        # Clear difficulty after submit
        del request.session['difficulty']

        return render(request, "quizresult.html", {
            "student": student,
            "total": questions.count(),
            "correct": correct,
            "wrong": wrong,
            "score": score,
            "remarks": remarks
        })

    return render(request, "quizattempt.html", {
        "questions": questions
    })


       
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




def result_history(request):
    roll_no = request.session.get('roll_no')

    if not roll_no:
        return HttpResponse("Login required")

    student = student_registration.objects.get(roll_no=roll_no)

    results = result.objects.filter(roll_no=student).order_by('-id')

    return render(request, "result_history.html", {
        "student": student,
        "results": results
    })

def select_option(request):
    if request.method == "POST":
        choice = request.POST.get('choice')

        # 🔒 Hidden mapping
        difficulty_map = {
            "A": "Easy",
            "B": "Medium",
            "C": "Hard"
        }

        request.session['difficulty'] = difficulty_map.get(choice)

        return redirect('quiz_attempt')

    return render(request, "select_option.html")
    from .models import questions



# nlp code
