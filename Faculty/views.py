from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from Common.models import faculty_registration,question_bank,questions,question_bank,quiz,questions,student_registration
from Common.forms import faculty_RegistrationForm,quizquestionForm,quizForm,question_bankForm,questionsForm,student_registrationForm


def login(request):
    reg = faculty_RegistrationForm()
    return render(request,'login.html', {'form':reg})

def register(request):
    regs=faculty_RegistrationForm()
    return render(request,'register.html', {'form':regs})

def questioninsert(request):
    qs=quizquestionForm()
    return render(request,"questioninsert.html",{'form':qs})

def quizinsert(request):
    qz=quizForm()
    return render(request,"quizinsert.html",{'form':qz})

def questiondisplay(request):
     data=questions.objects.all()
     return render(request,"questiondisplay.html",{'questiondata':data})


def students(request):
    data=student_registration.objects.all()
    return render(request,"studentlist.html",{'studentdata':data})

def quizdisplay(request):
    data=quiz.objects.all()
    return render(request,"quizdisplay.html",{'quizdata':data})
 
def home(request):
    return render(request,"home.html")

def faculty_reg(request):
    if request.method=="POST":
        form = faculty_RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("registerd")
    return HttpResponse("invalid")

def quiz_in(request):
    if request.method=="POST":
        form = quizForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("apploded")
    return HttpResponse("invalid")

def question_in(request):#view
  
    if request.method == "POST":
      form = questionsForm(request.POST)
      if form.is_valid():
          form.save()

    return HttpResponse("apploded")
 
def student_edit(request, roll_no):
    student = get_object_or_404(student_registration, roll_no=roll_no)

    if request.method == "POST":
        form = student_registrationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = student_registrationForm(instance=student)

    return render(request, "student_edit.html", {"form": form, "student": student})


def student_delete(request, roll_no):
    student = get_object_or_404(student_registration, roll_no=roll_no)
    student.delete()
    return redirect('student_list')


def quiz_edit(request, quiz_id):
    q = get_object_or_404(quiz, quiz_id=quiz_id)
    
    if request.method == "POST":
        form = quizForm(request.POST, instance=q)
        if form.is_valid():
            form.save()
            return redirect('quiz_display')

    else:
        form = quizForm(instance=q)

    return render(request, 'quizedit.html', {'form': form})


def quiz_delete(request, quiz_id):
    q = get_object_or_404(quiz, quiz_id=quiz_id)
    q.delete()
    return redirect('quiz_display')


def floginaction(request):
    if request.method == "POST":
       faculty_id= request.POST.get('faculty_id')
       password=request.POST.get('password')

   
      
    try:
        faculty = faculty_registration.objects.get(faculty_id=faculty_id,password=password)
        request.session['faculty_id']=faculty.faculty_id
        request.session['password']=faculty.password
       # return HttpResponse("log in success")
        return redirect('faculty_home')
    except faculty_registration.DoesNotExist:
            return HttpResponse("invalid login ")     

# def upload_question_action(request):#view action

#     form = questionsForm(request.POST)
#     if form.is_valid():
#         question = form.save(commit=False)
#         print("after validation")
#         question.subject_k=form.cleaned_data['subject_k']
#         print(question.subject_k)
#         print("after foreign key")
#         question.save()
#         print("after saved")
#         return redirect('question_inn')
#     return render(request,"uquestions.html",{"form":form})

def upload_question_action(request):#view action
    # if request.POST:
    #     form = questionsForm(request.POST) #getting all information which include foreign key
    #     try:
    #         if form.is_valid():
    #             form.save()
    #             return render(request,'uquestions.html',{
    #             'form':form, #Re displaying page after registering a cource
    #             'message':'added new question'  #A confirmation message is passed 
    #             })
    #     except Exception as e:
    #         return render(request,'uquestion.html',{
    #             'form':form, #Re displaying page after registering a cource
    #             'message':'failed to as a new question'  #A confirmation message is passed 
    #             })
    # print(request.POST)
    # return HttpResponse("post failed") #include if your post request is failing
    if request.method == "POST":
        form = questionsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    return HttpResponse("QUESTION APPLODED")


def uploadquestion(request):
    qf = questionsForm()
    return render(request,'uquestions.html', {'form':qf})