from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.db.models import Count
from Common.models import Department,FacultyRegistration,QuestionBank,Adminstrator

from Common.forms import DepartmentForm,FacultyRegistrationForm,FacultyEditform

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from django.contrib.auth import authenticate, login

from django.contrib.auth.hashers import check_password
from django.contrib import messages



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin = Adminstrator.objects.get(user_name=username)

            if check_password(password, admin.password):
                request.session['admin_user'] = admin.user_name   
                return redirect("admin_home")
            else:
                messages.error(request, "Invalid password")

        except Adminstrator.DoesNotExist:
            messages.error(request, "Invalid username")

    return render(request, "user/adlogin.html")


from django.contrib.auth.decorators import login_required

def admin_home(request):
    if 'admin_user' not in request.session:
        return redirect('admin_login')

    return render(request, "user/ahome.html")


from django.contrib.auth import logout

def admin_logout(request):
    logout(request)
    return redirect("commonhome")


def teachers(request):
    data = FacultyRegistration.objects.all()
    return render(request, "user/faculty_list.html", {"data": data})


def department(request):
     dep=DepartmentForm()
     return render(request,"department.html",{'forms':dep})

def registerdisplay(request):
    return render(request,"registerdisplay.html")

def ahome(request):
    return render(request,"ahome.html")

def faculty_edit(request, faculty_id):
    faculty = get_object_or_404(FacultyRegistration, faculty_id=faculty_id)

    if request.method == "POST":
        form = FacultyEditform(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('teachers_list')
    else:
        form = FacultyEditform(instance=faculty)

    return render(request, "faculty_edit.html", {"form": form, "faculty": faculty})


def faculty_delete(request, faculty_id):
    faculty = get_object_or_404(FacultyRegistration, faculty_id=faculty_id)
    faculty.delete()
    return redirect('teachers_list')


def admin_reg(request):
    if request.POST:

      form = AdminRegistrationForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect("admin_home")
    return HttpResponse("invalid")


# Create your views here.



def department_add(request):
    if request.method == "POST":
        name = request.POST.get("department_name")

        if Department.objects.filter(department_name=name).exists():
            messages.error(request, "Department already exists.")
        else:
            Department.objects.create(department_name=name)
            messages.success(request, "Department added successfully.")
            return redirect('department_list')

    return render(request, "user/department_add.html")


def department_list(request):
    departments = Department.objects.all()   

    return render(
        request,
        "user/department_list.html",
        {
            "departments": departments  
        }
    )

def department_edit(request, id):
    department = get_object_or_404(Department, id=id)

    if request.method == "POST":
        department.department_name = request.POST.get("department_name")
        department.save()
        messages.success(request, "Department updated successfully.")
        return redirect('department_list')

    return render(request, "user/department_edit.html", {
        "department": department
    })


def department_delete(request, id):
    department = get_object_or_404(Department, id=id)

    try:
        department.delete()
        messages.success(request, "Department deleted successfully.")
    except ProtectedError:
        messages.error(
            request,
            "Cannot delete this department because it is linked to courses or subjects."
        )

    return redirect("department_list")


def question_repetition_report(request):
    report = (
        QuestionBank.objects
        .values('subject__subject_name')
        .annotate(repeated_count=Count('year', distinct=True))
        .order_by('-repeated_count')
    )

    return render(request, 'admin/question_repetition.html', {
        'report': report
    })
