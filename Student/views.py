from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from Common.models import StudentRegistration,Quiz, Result,QuestionBank,QuizAnswer,QuizAttempt,QuizOption,QuizQuestion,Department
from Common.forms import StudentRegistrationForm,StudentLoginForm,DepartmentForm,CourseForm,SubjectForm,QuestionBankForm,QuizAnswerForm,QuizAttemptForm,QuizOptionForm,QuizQuestionForm
import random


from .utils import detect_intent, extract_topic, rebuild_mcq_stem
from django.http import JsonResponse
from django.contrib import messages

from django.http import JsonResponse 

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from Common.util import  send_emails



def stlogin(request):
    reg=StudentRegistrationForm()
    return render(request,"shome.html",{'forms':reg})


# def student_reg(request):
#     print("hitted")
#     if request.method == "POST":
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("Saved successfully")
#             return redirect('student_login')
#         else:
#             print(form.errors)  
#     else:
#         form = StudentRegistrationForm()

#     return render(request, 'student/stregister.html', {'form': form})
def student_reg(request):

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            student = form.save()

            # Get form data
            email = form.cleaned_data.get('email_id')
            roll_no = form.cleaned_data.get('roll_no')
            password = form.cleaned_data.get('password')

            subject = "Registration Info"
            body = f"""Registration on quiz
Student ID: {roll_no}
Email: {email} 
"password : {password}
"""

            if email:
                print("Email is:", email)
                send_emails(receiver=email, subject=subject, body=body)
                print("Email function executed")
            messages.success(request, "Registration successful. Please login.")
            return redirect('student_login')

        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:

        form = StudentRegistrationForm()

    return render(request, 'student/stregister.html', {'form': form})

def sloginaction(request):
    error = None
    form = StudentLoginForm()

    if request.method == "POST":
        print("hitted")
        form = StudentLoginForm(request.POST)
        roll_no = request.POST.get('roll_no')
        password = request.POST.get('password')
        print(roll_no,password)

        try:
            student = StudentRegistration.objects.get(
                roll_no=roll_no,
                password=password
            )
            print(student)

            request.session['student_roll'] = roll_no
            print("redirected")
            return redirect('student_home')
            

        except StudentRegistration.DoesNotExist:
            error = "Invalid Roll Number or Password"

    return render(request, 'student/stlogin.html', {
        'forms': form,
        'error': error
    })



# def stregister(request):
#     regs=StudentRegistrationForm()
#     return render(request,"student/stregister.html",{'forms':regs})


def student_home(request):

    student = StudentRegistration.objects.get(
        roll_no=request.session['student_roll']
    )

    return render(request, 'shome.html', {
        'student': student
    })


def student_logout(request):
    request.session.flush()   
    return redirect('commonhome')


def student_pyq_questions(request):

    pyqs = QuestionBank.objects.select_related(

        'course_name',
        'course_name__department',
        'subject',
        'subject__course',
        'subject__course__department'

    ).order_by(

        '-year',
        'course_name__department__department_name',
        'course_name__course_name',
        'subject__subject_name'

    )


    return render(request, 'student/pyq_questions.html', {

        'pyqs': pyqs

    })


def passwordchange(request):
    return render(request,"passwordchange.html")
    

def student_quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'student/quiz_list.html', {'quizzes': quizzes})


import random
from django.shortcuts import get_object_or_404, render, redirect
from .utils import rebuild_mcq_stem



def result_history(request):
    roll_no = request.session.get('student_roll')
    student = StudentRegistration.objects.get(roll_no=roll_no)

    attempts = QuizAttempt.objects.filter(
        student=student,
        is_mock=True
    ).order_by('-attempted_at')

    return render(request, 'student/result_history.html', {
        'attempts': attempts,
        'student': student
    })


from django.db import IntegrityError

import random
from django.shortcuts import render, redirect, get_object_or_404
from .utils import rebuild_mcq_stem
from Common.models import Quiz, QuizAttempt, QuizAnswer, QuizOption


def student_quiz_attempt(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    roll_no = request.session.get("student_roll")

    student = get_object_or_404(StudentRegistration, roll_no=roll_no)

    is_mock = request.GET.get("mock") == "1"

    session_key = f"mock_attempt_{quiz_id}"
    mock_count = request.session.get(session_key, 0)

    questions = list(
        quiz.questions.prefetch_related("options")
    )

    regenerated_questions = []

    if is_mock and mock_count > 0:
        random.shuffle(questions)

        for q in questions:
            regenerated_questions.append({
                "id": q.id,
                "text": rebuild_mcq_stem(q.question_text),
                "options": q.options.all()
            })
    else:
        for q in questions:
            regenerated_questions.append({
                "id": q.id,
                "text": q.question_text,
                "options": q.options.all()
            })

    if request.method == "POST":

        if is_mock:
            QuizAttempt.objects.filter(
                quiz=quiz,
                student=student,
                is_mock=True
            ).delete()

        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            student=student,
            is_mock=is_mock
        )

        score = correct = wrong = 0

        for q in questions:
            selected_option_id = request.POST.get(str(q.id))
            if not selected_option_id:
                continue

            opt = get_object_or_404(QuizOption, id=selected_option_id)

            QuizAnswer.objects.create(
                attempt=attempt,
                question=q,
                selected_option=opt
            )

            if opt.is_correct:
                score += 1
                correct += 1
            else:
                wrong += 1

        attempt.score = score
        attempt.correct_count = correct
        attempt.wrong_count = wrong
        attempt.passed = score >= quiz.pass_mark
        attempt.save()

        if is_mock:
            request.session[session_key] = mock_count + 1

        return redirect("student_quiz_result", attempt_id=attempt.id)

    return render(request, "student/attempt_quiz.html", {
        "quiz": quiz,
        "questions": regenerated_questions,
        "is_mock": is_mock,
        "mock_count": mock_count
    })


def email_otp(request):
    return render(request,'email_otp.html')

def student_quiz_result(request, attempt_id):
    attempt = QuizAttempt.objects.get(id=attempt_id)
    quiz = attempt.quiz   

    questions = quiz.questions.prefetch_related('options')

    return render(request, 'student/quiz_result.html', {
        'attempt': attempt,
        'quiz': quiz,        
        'questions': questions
    })


def email_otp(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        email = request.POST.get('email_id')
        print(email)
        
        try:
            student=StudentRegistration.objects.get(email_id = email)
            request.session['email_id'] = student.email_id
            subject="quiz app password reset"
            otp=random.randint(1000,9999)
            body=f"otp for your password reset = {otp}"
            sent = send_emails(email,subject,body)
            return HttpResponse("otp sended")
        except StudentRegistration.DoesNotExist:
            return HttpResponse("no student in this email id")



# Create your views here.
def result_history(request):
    roll_no = request.session.get('student_roll')

    if not roll_no:
        return redirect('student_login')

    student = StudentRegistration.objects.get(roll_no=roll_no)

    attempts = QuizAttempt.objects.filter(
        student=student
    ).order_by('-attempted_at')

    return render(request, 'student/result_history.html', {
        'student': student,
        'attempts': attempts
    })


def select_option(request):
    if request.method == "POST":
        choice = request.POST.get('choice')

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

def password_reset(request):

    stage = request.POST.get("stage", "email")

    if request.method == "POST":

    
        if stage == "email":

            email = request.POST.get("email")

            try:
                student = StudentRegistration.objects.get(email_id=email)

                otp = random.randint(100000, 999999)

                request.session["reset_email"] = email
                request.session["reset_otp"] = str(otp)

                send_emails(
                    receiver=email,
                    subject="Password Reset OTP",
                    body=f"Your OTP for password reset is: {otp}",
                          )

                messages.success(request, "OTP sent to your email.")
                return render(request, "passwordreset.html", {"stage": "otp"})

            except StudentRegistration.DoesNotExist:
                messages.error(request, "Email not registered.")

        
        elif stage == "otp":

            entered_otp = request.POST.get("otp")
            session_otp = request.session.get("reset_otp")

            if entered_otp == session_otp:
                messages.success(request, "OTP verified. Set new password.")
                return render(request, "passwordreset.html", {"stage": "new_password"})
            else:
                messages.error(request, "Invalid OTP.")
                return render(request, "passwordreset.html", {"stage": "otp"})

        
        elif stage == "new_password":

            new_password = request.POST.get("new_password")
            email = request.session.get("reset_email")

            try:
                student = StudentRegistration.objects.get(email_id=email)
                student.Password = new_password
                student.save()

                request.session.pop("reset_otp", None)
                request.session.pop("reset_email", None)

                messages.success(request, "Password reset successful.")
                return HttpResponseRedirect(reverse("login_page"))

            except StudentRegistration.DoesNotExist:
                messages.error(request, "Something went wrong.")

    return render(request, "passwordreset.html", {"stage": "email"})
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        print("EMAIL ENTERED:", email)
        student = StudentRegistration.objects.filter(email_id__iexact=email).first()
        print("USER FOUND:", user)
        if student:
            otp = str(random.randint(100000, 999999))
            student.otp = otp
            student.save()
            print("OTP GENERATED:", otp)
            sent_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}',
                'your_email@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['reset_user'] = user.id
            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')
        else:
            messages.error(request, "Email not registered.")
    role =  request.session.get("role")
    return render(request, 'forgot_password.html',{'role':role})

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('reset_user')
        user = Registration.objects.get(id=user_id)

        if user.otp == entered_otp:
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP")
    role =  request.session.get("role")
    return render(request, 'verify_otp.html',{'role':role})

def reset_password(request):
    user_id = request.session.get('reset_user')
    user = Registration.objects.get(id=user_id)

    if request.method == "POST":
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

        if p1 != p2:
            messages.error(request, "Passwords do not match")
        else:
            user.password = make_password(p1)
            user.confirm_password = make_password(p1)
            user.otp = None
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login_page')
    role =  request.session.get("role")
    return render(request, 'reset_password.html',{'role':role})