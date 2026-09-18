from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator


def home(request):
    return render(request, 'students/home.html')


def about(request):
    return render(request, 'students/about.html')


def contact(request):
    return render(request, 'students/contact.html')


def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'students/add_students.html', {
        'form': form
    })

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {
        'form' : form
    })

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_student.html', {
        'student':student
    })

def student_details(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/student_details.html', {
        'student' : student
    })

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
