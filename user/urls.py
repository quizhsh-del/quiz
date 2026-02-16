from django.urls import path

from .import views


urlpatterns = [
    #rendered function
# path('user/',views.adlogin,name='user_login'),
# path('adminreg',views.adregister,name='admin_register'),
path('teachers',views.teachers,name='teachers_list'),
# path('department',views.department,name='department_list'),
path('reglist',views.registerdisplay,name='register_list'),
path('ahomepage',views.ahome,name='admin_home'),
path('faculty/edit/<str:faculty_id>/', views.faculty_edit, name='faculty_edit'),
path('faculty/delete/<str:faculty_id>/', views.faculty_delete, name='faculty_delete'),

 
 #action perfomed
path('adminaction',views.admin_reg,name='admin_reg'),
# path('departmentaction',views.department_in,name='department_in'),

# Department
path('department/add/', views.department_add, name='department_add'),
path('department/list/', views.department_list, name='department_list'),
path('department/edit/<str:id>/', views.department_edit, name='department_edit'),
path('department/delete/<str:id>/', views.department_delete, name='department_delete'),


path("admin/login/", views.admin_login, name="admin_login"),
path("admin/home/", views.admin_home, name="admin_home"),
 path("admin/logout/", views.admin_logout, name="admin_logout"),
]