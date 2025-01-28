from django.shortcuts import render,redirect
from tutionapp.models import CustomUser,Student,Teacher
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import os
import random
from django.db.models import Q


# Create your views here.
def t_dashboard(request):
    return render(request,'t_dashboard.html')

def s_dashboard(request):
    return render(request,'s_dashboard.html')

def home(request):
    return render(request,'index.html')

def loginpage(request):
    return render(request,'login.html')

def student_signup(request):
    return render(request,'studentsignup.html')

def teacher_signup(request):
    return render(request,'teachersignup.html')

def add_teacher(request):
    if request.method=="POST":
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        username=request.POST['uname']
        age=request.POST['age']
        email=request.POST['email']
        contact=request.POST['pno']
        user_type=request.POST['text']
        sel1=request.POST['sel']
        Image=request.POST['file']

        if CustomUser.objects.filter(username=username).exists():
            messages.success(request,'Username already exists.Please choose another')
            return redirect('teacher_signup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request,'Email already exists.Please choose another')
            return render(request,'teachersignup.html')
        
        user=CustomUser.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            user_type=user_type
        )
        user.save()

        teacher=Teacher(
            user=user,
            course=sel1,
            Age=age,
            Phone_number=contact,
            Image=Image
        )
        teacher.save()
        messages.success(request,'Registration Successfull!Please wait for admin approval.')
        return redirect('teacher_signup')
    

def add_student(request):
    if request.method=="POST":
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        username=request.POST['uname']
        age=request.POST['age']
        email=request.POST['email']
        contact=request.POST['pno']
        user_type=request.POST['text']
        sel1=request.POST['sel']
        Image=request.POST['file']

        if CustomUser.objects.filter(username=username).exists():
            messages.success(request,'Username already exists.Please choose another')
            return redirect('student_signup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request,'Email already exists.Please choose another')
            return render(request,'studentsignup.html')
        
        user=CustomUser.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            user_type=user_type
        )
        user.save()

        student=Student(
            user=user,
            course=sel1,
            Age=age,
            Phone_number=contact,
            Image=Image
        )
        student.save()
        messages.success(request,'Registration Successfull!Please wait for admin approval.')
        return redirect('student_signup')
    
def login1(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            if user.user_type=='1':
                login(request,user)
                return redirect('admin_view')
            elif user.user_type=='2':
                login(request,user)
                return redirect('t_dashboard')
            elif user.user_type=='3':
                return redirect('s_dashboard')
            
        else:
            messages.info(request,"Invalid username or password")
            return redirect('loginpage')
        
def admin_view(request):
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request,'admin.html',{'unapproved_count':count})

def approvedisapprove(request):
    users=CustomUser.objects.filter(~Q(user_type="1"))
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request,'approvedisapprove.html',{'user_data':users,'unapproved_count':count})


def approve(request,k):
    usr=CustomUser.objects.get(id=k)
    usr.status=1
    usr.save()

    if usr.user_type=='2':
       
       tea=Teacher.objects.get(user=k) 
       password=str(random.randint(100000, 999999))
       print(password)
       usr.set_password(password)
       usr.save()

       send_mail(
          'Admin approved',
           f'Username: {tea.user.username}\nPassword:{password}\nEmail:{tea.user.email}',
           settings.EMAIL_HOST_USER,
           [tea.user.email]
        )
       messages.info(request,'Teacher approved.')
    
    elif usr.user_type=='3':
        stu=Student.objects.get(user=k)
        password=str(random.randint(100000, 999999))
        print(password)
        usr.set_password(password)
        usr.save()

        send_mail(
          'Admin approved',
           f'Username: {stu.user.username}\nPassword:{password}\nEmail:{stu.user.email}',
           settings.EMAIL_HOST_USER,
           [usr.email]
        )
        messages.info(request,'Student approved.')

    return redirect  ('approvedisapprove')

def disapprove(request,k):
    usr=CustomUser.objects.get(id=k)
    if usr.user_type=='2':
        Teacher.objects.filter(user=k).delete()
    elif usr.user_type=='3':
        Student.objects.filter(user=k).delete()

    usr.delete()
    send_mail(
          ' Disapproved ',
           f'Your registration has been disapproved by admin',
           settings.EMAIL_HOST_USER,
           [usr.email]
        )
    messages.info(request,'User dissaproved.')
    return redirect('approvedisapprove')



def reset(request):
    if request.method=='POST':
        pas=request.POST['new_password']
        cpas=request.POST['confirm_password']
        if pas==cpas:
            if len(pas)<6 or not any(char.isupper() for char in pas) \
                or not any(char.isdigit() for char in pas)\
                or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in pas):
                messages.error(request,'Password must be atleast 6 characters long and contain at least one uppercase,one digit and one special character')
                return redirect('reset')
            
            else:
                usr=request.user.id
                print(usr)
                tsr=CustomUser.objects.get(id=usr)
                tsr.set_password(pas)
             
                tsr.save()
                messages.info(request,"Password Changed")
                return redirect('reset')
    return render(request,'resetpassword.html')

def logout(request):
    auth.logout(request)
    return render(request,'login.html')

            
            
            
