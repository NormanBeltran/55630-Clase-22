from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import Curso, Profesor, Estudiante
from .forms import CursoForm, ProfesorForm

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
# Create your views here.
def home(request):
    return render(request, "aplicacion/home.html")

def cursos(request):
    contexto = {'cursos': Curso.objects.all(), 'titulo': 'Reporte de Cursos', 'comisiones': ['55630', '55640'] }
    return render(request, "aplicacion/cursos.html", contexto)

def profesores(request):
    return render(request, "aplicacion/profesores.html")

def estudiantes(request):
    return render(request, "aplicacion/estudiantes.html")

def entregables(request):
    return render(request, "aplicacion/entregables.html")

def cursoForm(request):
    if request.method == "POST":
        curso = Curso(nombre=request.POST['nombre'], 
                      comision=request.POST['comision'])
        curso.save()
        return HttpResponse("Se grabo con exito el curso!")
    
    return render(request, "aplicacion/cursoForm.html")

def cursoForm2(request):
    if request.method == "POST":
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            curso_nombre = miForm.cleaned_data.get('nombre')
            curso_comision = miForm.cleaned_data.get('comision')
            curso = Curso(nombre=curso_nombre,
                          comision=curso_comision)
            curso.save()
            return render(request, "aplicacion/base.html")
    else:
        miForm = CursoForm()
    
    return render(request, "aplicacion/cursoForm2.html", {"form": miForm })

def buscarComision(request):
    return render(request, "aplicacion/buscarComision.html")

def buscar2(request):
    if request.GET['buscar']:
        patron = request.GET['buscar']
        cursos = Curso.objects.filter(nombre__icontains=patron)
        contexto = {"cursos": cursos, 'titulo': f'Cursos que tiene como patron "{patron}"'}
        return render(request, "aplicacion/cursos.html", contexto)
    return HttpResponse("No se ingreso nada a buscar")

#___________________________ 15/08/2023

def profesores(request):
    ctx = {'profesores': Profesor.objects.all()}
    return render(request, "aplicacion/profesores.html", ctx)

def updateProfesor(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            profesor.nombre = miForm.cleaned_data.get('nombre')
            profesor.apellido = miForm.cleaned_data.get('apellido')
            profesor.email = miForm.cleaned_data.get('email')
            profesor.profesion = miForm.cleaned_data.get('profesion') 
            profesor.save()
            return redirect(reverse_lazy('profesores'))   
    else:
        miForm = ProfesorForm(initial={
            'nombre': profesor.nombre,
            'apellido': profesor.apellido,
            'email': profesor.email,
            'profesion': profesor.profesion,
        })
    return render(request, "aplicacion/profesorForm.html", {'form': miForm})

def deleteProfesor(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
    return redirect(reverse_lazy('profesores'))

def createProfesor(request):    
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            p_nombre = miForm.cleaned_data.get('nombre')
            p_apellido = miForm.cleaned_data.get('apellido')
            p_email = miForm.cleaned_data.get('email')
            p_profesion = miForm.cleaned_data.get('profesion')
            profesor = Profesor(nombre=p_nombre, 
                             apellido=p_apellido,
                             email=p_email,
                             profesion=p_profesion,
                             )
            profesor.save()
            return redirect(reverse_lazy('profesores'))
    else:
        miForm = ProfesorForm()

    return render(request, "aplicacion/profesorForm.html", {"form":miForm})

#____________________ Class Based View

class EstudianteList(ListView):
    model = Estudiante

class EstudianteCreate(CreateView):
    model = Estudiante
    fields = ['nombre', 'apellido', 'email']
    success_url = reverse_lazy('estudiantes')

class EstudianteUpdate(UpdateView):
    model = Estudiante
    fields = ['nombre', 'apellido', 'email']
    success_url = reverse_lazy('estudiantes')

class EstudianteDelete(DeleteView):
    model = Estudiante
    success_url = reverse_lazy('estudiantes')