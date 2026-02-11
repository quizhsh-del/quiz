
from django.urls import path

from .import views



urlpatterns = [
    #rendered
# path('student',views.stlogin,name='student_login'),
# path('stregister',views.stregister,name='student_register'),
path('passwordchange/student',views.passwordchange,name='password_change'), 
# path('quizattempt',views.quizattempt,name='quiz_attempt'),
# path('pyq',views.pyq,name='pyq'),
# path('shomepage',views.home,name='student_home'),
path('emailotp',views.email_otp,name='email_otp'),
path('emailpage',views.student_email_page,name='student_email_page'),
path('result-history', views.result_history, name='result_history'),
path('select-option', views.select_option, name='select_option'),



#actioinperfomed
# path('studentaction',views.student_reg,name='student_reg'),
# path('student_log_page',views.sloginaction,name='slogin'),

path('sregister', views.student_reg, name='student_register'),
path('slogin', views.sloginaction, name='student_login'),
path('slogout/', views.student_logout, name='student_logout'),
path('student/home', views.student_home, name='student_home'),

path('student/pyq/', views.student_pyq_questions, name='student_pyq'),
path('quizzes/', views.student_quiz_list, name='quiz_attempt'),
# path('attempt/<int:quiz_id>/', views.quizattempt, name='attempt_quiz'),
# path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),

# path('quiz/<int:quiz_id>/start/', views.start_quiz, name='quiz_start'),

# path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),

path("quiz/<int:quiz_id>/", views.student_quiz_attempt, name="student_quiz_attempt"),
# path("student/quiz/result/<int:attempt_id>/", views.student_quiz_attempt, name="student_quiz_result"),

path('student/quiz/result/<int:attempt_id>/',views.student_quiz_result,name='student_quiz_result'),

]