
from django.urls import path

from .import views
#rendering urls
urlpatterns = [
 path('facultylogin',views.login,name='login'),
 path('facultyreg',views.register,name='register'),
 path('qninsert',views.questioninsert,name='question_insert'),
 path('quizinsert',views.quizinsert,name='quiz_insert'),
 path('qnlist',views.questiondisplay,name='question_displays'),
 path('quizlist',views.quizdisplay,name='quiz_display'),
 path('facultypage',views.home,name='faculty_home'),
 path('stlist',views.students,name='student_list'),
 #path('uquestion',views.uq,name='upload_question'),#first_url
 path('uquestion',views.uploadquestion,name='upload_question'),#first_url
path('student/edit/<str:roll_no>/', views.student_edit, name='student_edit'),
path('student/delete/<str:roll_no>/', views.student_delete, name='student_delete'),
path('quiz/edit/<str:quiz_id>/', views.quiz_edit, name='quiz_edit'),
path('quiz/delete/<str:quiz_id>/', views.quiz_delete, name='quiz_delete'),


 #action performed
 path('facultyaction',views.faculty_reg,name='faculty_reg'),
 path('quizaction',views.quiz_in,name='quiz_in'),
 path('questionaction',views.question_in,name='question_inn'),
 path('faculty_login_page',views.floginaction,name='flogin'),
 path('uquestion/action',views.upload_question_action,name='upload_question_action'),#first_url
]

