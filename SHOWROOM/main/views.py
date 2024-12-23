from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from cars.models import Car

# Create your views here.

def main_view(request:HttpRequest):
    
    first_car = Car.objects.order_by('id').first()

    cars = Car.objects.all().order_by("-created_at")[:3]

    return render(request, 'main/home.html', {'car': first_car, 'cars': cars})
