from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'students/home.html')


def about(request):
    return render(request, 'students/about.html')


def contact(request):
    return render(request, 'students/contact.html')

@login_required
def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Student added successfully!'
            )
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'students/add_students.html', {
        'form': form
    })

@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Student updated sucessfully!'
            )
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {
        'form' : form
    })

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_student.html', {
        'student':student
    })

@login_required
def student_details(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/student_details.html', {
        'student' : student
    })

@login_required
def student_list(request):

    query = request.GET.get('search')
    course = request.GET.get('course')
    age = request.GET.get('age')
    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)
    if course:
        students = students.filter(course__icontains=course)
    if age:
        students = students.filter(age=age)
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'students/student_list.html', {
        'page_obj': page_obj
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request, 
            username = username,
            password = password
        )
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            messages.error(
                request, 'Invalid username or password.'
            )
    return render(request, 'students/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 'Account created successfully!'
            )
            return redirect('student_list')
    else:
        form = UserCreationForm()

    return render(request, 'students/register.html', {
                'form' : form
            })

def logout_view(request):
    logout(request)
    messages.success(
        request,
        'You have been logged out successfully.'
    )
    return redirect('login')
