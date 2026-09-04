from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


def home(request):
    return render(request, 'students/home.html')


def about(request):
    return render(request, 'students/about.html')


def contact(request):
    return render(request, 'students/contact.html')


def student_list(request):
    students = Student.objects.all()

    return render(request, 'students/student_list.html', {
        'students': students
    })


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
