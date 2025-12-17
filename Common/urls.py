from django.urls import path

from .import views

urlpatterns = [
 path('Performance',views.Performance,name='Performance'),
 path('feedback',views.feedback,name='feedback'),
 path('feedback_action',views.feedback_action,name='faction'),
 path('header_c',views.header_c,name='header_c'),
 path('commonhome',views.commonhome,name='commonhome'),
]
