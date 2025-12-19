
from django.urls import path

from .import views

urlpatterns = [
    #rendered
path('student',views.stlogin,name='student_login'),
path('stregister',views.stregister,name='student_register'),
path('passwordchange/student',views.passwordchange,name='password_change'), 
path('quizattempt',views.quizattempt,name='quiz_attempt'),
path('pyq',views.pyq,name='pyq'),
path('shomepage',views.home,name='student_home'),
path('emailotp',views.email_otp,name='email_otp'),
path('emailpage',views.student_email_page,name='student_email_page'),
path('result-history', views.result_history, name='result_history'),
path('select-option', views.select_option, name='select_option'),



#actioinperfomed
path('studentaction',views.student_reg,name='student_reg'),
 path('student_log_page',views.sloginaction,name='slogin')
]