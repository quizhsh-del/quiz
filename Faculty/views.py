from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from Common.models import FacultyRegistration,QuestionBank,QuizQuestion,Quiz,StudentRegistration,Course,Subject,Result,QuizOption, QuizAttempt
from Common.forms import FacultyRegistrationForm,QuestionBankForm,QuizForm, QuizAnswerForm,QuizAttemptForm,QuizOptionForm,QuizQuestionForm,StudentRegistrationForm,QuizForm, StudentEditForm,CourseForm,SubjectForm

import random
from django.http import JsonResponse
from django.contrib import messages

from django.http import JsonResponse 

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from Common.util import  send_emails

def login(request):
    reg = FacultyRegistrationForm()
    return render(request,'faculty/login.html', {'form':reg})


def register(request):
    regs=FacultyRegistrationForm()
    return render(request,'faculty/register.html', {'form':regs})


def faculty_reg(request):
    if request.method == "POST":
        form = FacultyRegistrationForm(request.POST)

        if form.is_valid():
            faculty = form.save()

            
            email = form.cleaned_data.get('email')
            faculty_id = form.cleaned_data.get('faculty_id')
            password = form.cleaned_data.get('password')

            subject = "Registration Info"
            body = f"""Registration on quiz
Faculty ID: {faculty_id}
Email: {email} 
"password : {password}
"""

            if email:
                send_emails(receiver=email, subject=subject, body=body)

            messages.success(request, "Registration successful. Please login.")
            return redirect('teachers_list')

        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = FacultyRegistrationForm()

    return render(request, 'faculty/register.html', {'form': form})


def floginaction(request):
    reg = FacultyRegistrationForm()
    if request.method == "POST":
        faculty_id = request.POST.get("faculty_id")
        password = request.POST.get("password")

        try:
            faculty = FacultyRegistration.objects.get(
                faculty_id=faculty_id,
                password=password
            )
            request.session["faculty_id"] = faculty.faculty_id
            return redirect("faculty_home")
        except FacultyRegistration.DoesNotExist:
            error = "Invalid Roll Number or Password"
    return render(request, "faculty/login.html",{'form':reg})


def students(request):

    faculty_id = request.session.get('faculty_id')

    if not faculty_id:
        return redirect('faculty_login')

    # Use correct PK field
    faculty = FacultyRegistration.objects.get(
        faculty_id=faculty_id
    )

    students = StudentRegistration.objects.filter(
        department=faculty.department
    )

    return render(request, 'studentlist.html', {
        'students': students
    })


def student_edit(request, roll_no):
    student = get_object_or_404(StudentRegistration, roll_no=roll_no)

    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')   
    else:
        form = StudentEditForm(instance=student)

    return render(request, "student_edit.html", {
        "form": form,
        "student": student
    })


def student_delete(request, roll_no):
    student = get_object_or_404(StudentRegistration, roll_no=roll_no)
    student.delete()
    return redirect('student_list')


def course_insert(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cource_list')   # or wherever you want
    else:
        form = CourseForm()

    return render(request, "faculty/course_insert.html", {"form": form})


def cource_list(request):

    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("faculty_login")

    faculty = get_object_or_404(FacultyRegistration, faculty_id=faculty_id)


    courses = Course.objects.select_related('department').filter(
        department=faculty.department
    )


    return render(request, 'faculty/cource_list.html', {

        'courses': courses

    })


def course_edit(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('cource_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'faculty/course_edit.html', {
        'form': form,
        'course': course
    })


def course_delete(request, id):
    course = get_object_or_404(Course, id=id)

    try:
        course.delete()
        messages.success(request, "Course deleted successfully.")
    except ProtectedError:
        messages.error(
            request,
            "Cannot delete this course because it is linked to subjects or questions."
        )

    return redirect('cource_list')


def upload_question(request):
    if request.method == "POST":
        form = QuestionBankForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('questionbank_list')
    else:
        form = QuestionBankForm()

    return render(request, 'faculty/upload_question.html', {'form': form})


def questionbank_list(request):
    questions = QuestionBank.objects.all()
    return render(request, 'faculty/questionbank_list.html', {'questions': questions})


def subject_upload(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('faculty_home') 
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = SubjectForm()

    return render(request, 'faculty/subject_upload.html', {'form': form})


def subject_list(request):

    subjects = Subject.objects.select_related('course', 'course__department').all()

    return render(request, 'faculty/subject_list.html', {
        'subjects': subjects
    })



def subject_edit(request, id):
    subject = get_object_or_404(Subject, id=id)

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'faculty/subject_edit.html', {
        'form': form,
        'subject': subject
    })


from django.contrib import messages
from django.db.models.deletion import ProtectedError


def subject_delete(request, id):
    subject = Subject.objects.get(id=id)

    try:
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
    except ProtectedError:
        messages.error(
            request,
            "Cannot delete subject. It is linked with quizzes or questions."
        )

    return redirect("subject_list")


def question_edit(request, pk):
    question = get_object_or_404(QuestionBank, id=pk)

    if request.method == "POST":
        form = QuestionBankForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            return redirect('questionbank_list')   
    else:
        form = QuestionBankForm(instance=question)

    return render(request, 'faculty/question_edit.html', {
        'form': form,
        'question': question
    })


def question_delete(request, pk):
    question = get_object_or_404(QuestionBank, id=pk)
    question.delete()
    return redirect('questionbank_list')


def faculty_quiz_insert(request):
    quizzes = Quiz.objects.all()

    if request.method == "POST":
        quiz_id = request.POST.get("quiz")
        question_text = request.POST.get("question")

        option_texts = request.POST.getlist("option_text")
        explanations = request.POST.getlist("explanation")
        correct_indexes = request.POST.getlist("is_correct")

        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Save Question
        question = QuizQuestion.objects.create(
            quiz=quiz,
            question_text=question_text
        )

        # Save Options
        for i, text in enumerate(option_texts):
            if text.strip():
                QuizOption.objects.create(
                    question=question,
                    option_text=text,
                    explananation=explanations[i],
                    is_correct=str(i) in correct_indexes
                )

        return redirect("faculty_quiz_insert")

    return render(request, "faculty/quiz_insert.html", {
        "quizzes": quizzes
    })


def create_quiz(request):

    faculty_id = request.session.get("faculty_id")

    if not faculty_id:
        return redirect("faculty_login")

    faculty = get_object_or_404(
        FacultyRegistration,
        faculty_id=faculty_id
    )

    if request.method == "POST":
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.faculty = faculty   # assign owner
            quiz.save()

            return redirect("faculty_quiz_insert")

    else:
        form = QuizForm()

    return render(request, "faculty/create_quiz.html", {
        "form": form
    })



def faculty_course_quizzes(request, course_id):

    faculty_id = request.session.get("faculty_id")
    if not faculty_id:
        return redirect("faculty_login")

    quizzes = Quiz.objects.filter(
        subject__course_id=course_id,
        faculty_id=faculty_id
    )

    return render(request, "faculty/course_quiz_list.html", {
        "quizzes": quizzes
    })


def faculty_quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # questions are related via ManyToMany / ForeignKey
    questions = quiz.questions.prefetch_related('options')

    return render(request, 'faculty/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions
    })

 
def home(request):
    return render(request,"home.html")


# def question_in(request):#view
  
#     if request.method == "POST":
#       form = QuizQuestionForm(request.POST)
#       if form.is_valid():
#           form.save()

#     return HttpResponse("apppploded")

def quiz_edit(request, quiz_id):
    faculty_id = request.session.get("faculty_id")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        faculty__faculty_id=faculty_id   
    )

    if request.method == "POST":
        quiz.quiz_name = request.POST.get("quiz_name")
        quiz.semester = request.POST.get("semester")
        quiz.pass_mark = request.POST.get("pass_mark")
        quiz.save()

        return redirect("quiz_list")

    return render(request, "faculty/edit_quiz.html", {"quiz": quiz})


def quiz_delete(request, quiz_id):
    faculty_id = request.session.get("faculty_id")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        faculty__faculty_id=faculty_id
    )

    quiz.delete()
    return redirect("quiz_list")


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


# def upload_question_action(request):#view action
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
    # if request.method == "POST":
    #     form = questionsForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         form.save()
    # return HttpResponse("QUESTION APPLODED")


# def uploadquestion(request):
#     qf = questionsForm()
#     return render(request,'uquestions.html', {'form':qf})

# def pyqquestiondelete(request, subject_id):
#     q = get_object_or_404(questions, subject_id=subject_id)
#     q.delete()
#     return redirect('question_displays')


def faculty_result_view(request):
  
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('faculty_login')
    
    faculty = FacultyRegistration.objects.get(faculty_id=faculty_id)

    department = faculty.department

    results = QuizAttempt.objects.filter(
        student__department=department
    ).select_related('student', 'quiz').order_by('-id')

    context = {
        'results': results,
        'department': department.department_name if hasattr(department, 'department_name') else department,
    }

    return render(request, 'faculty/faculty_result_view.html', context)



# def quiz_regenerate_nlp(request):
#     if request.method == "POST":
#         question = request.POST.get("question", "").strip()

#         if not question:
#             return JsonResponse({"error": "Question is required"}, status=400)

#         regenerated = rebuild_mcq_stem(question)

#         return JsonResponse({
#             "original": question,
#             "regenerated": regenerated
#         })



def delete_result(request, result_id):
    res = get_object_or_404(result, id=result_id)
    res.delete()
    return redirect('faculty_result_see')    






# nlp code
# def regenerate_question(request):
#      if request.method == "POST":
#         original_question = request.POST.get("question")

#         if not original_question:
#             return JsonResponse({"error": "No question provided"})

#         new_question = rebuild_mcq_stem(original_question)

#         return JsonResponse({
#             "new_question": new_question
#         })
     

# def quiz_regenerate_nlp(request):
#     if request.method == "POST":
#         question = request.POST.get("question")
#         if question:
#             new_q = rebuild_mcq_stem(question)
#             return JsonResponse({"new_question": new_q})
#         return JsonResponse({"error": "No question"}, status=400)
    
# def student_delete(request, id):

#     if request.method == "POST":

#         student = Student.objects.get(id=id)

#         student.delete()

#     return redirect('student_list')
