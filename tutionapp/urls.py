from django.urls import path
from .import views
urlpatterns=[
    path('',views.home,name='home'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('student_signup',views.student_signup,name='student_signup'),
    path('teacher_signup',views.teacher_signup,name='teacher_signup'),
    path('add_student',views.add_student,name='add_student'),
    path('add_teacher',views.add_teacher,name='add_teacher'),
    path('login1',views.login1,name='login1'),
    path('s_dashboard',views.s_dashboard,name='s_dashboard'),
    path('t_dashboard',views.t_dashboard,name='t_dashboard'),
    path('admin_view',views.admin_view,name='admin_view'),
    path('approve/<int:k>',views.approve,name='approve'),
    path('disapprove/<int:k>',views.disapprove,name='disapprove'),
    path('approvedisapprove',views.approvedisapprove,name='approvedisapprove'),
    path('reset',views.reset,name='reset'),
    path('logout',views.logout,name='logout')



]