from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from Common.models import admin_registration,department,faculty_registration

from Common.forms import admin_registrationForm,departmentForm,faculty_RegistrationForm


def adlogin(request):
    reg=admin_registrationForm()
    return render(request,"adlogin.html",{'forms':reg})
def adregister(request):
    regs=admin_registrationForm()
    return render(request,"adregister.html",{'forms':regs})
def teachers(request):
     data=faculty_registration.objects.all()


    
     return render(request,"teachers.html",{'teacherdata':data})
def department(request):
     dep=departmentForm()
     return render(request,"department.html",{'forms':dep})
def registerdisplay(request):
    return render(request,"registerdisplay.html")
def ahome(request):
    return render(request,"ahome.html")
def faculty_edit(request, faculty_id):
    faculty = get_object_or_404(faculty_registration, faculty_id=faculty_id)

    if request.method == "POST":
        form = faculty_RegistrationForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('teachers_list')
    else:
        form = faculty_RegistrationForm(instance=faculty)

    return render(request, "faculty_edit.html", {"form": form, "faculty": faculty})



def faculty_delete(request, faculty_id):
    faculty = get_object_or_404(faculty_registration, faculty_id=faculty_id)
    faculty.delete()
    return redirect('teachers_list')


 
 

def admin_reg(request):
    if request.POST:

      form = admin_registrationForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect("admin_home")
    return HttpResponse("invalid")



# Create your views here.
def department_in(request):
    if request.method=="POST":
        form = departmentForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("apploded")
    return HttpResponse("invalid")

