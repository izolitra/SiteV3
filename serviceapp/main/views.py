from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def applications(request):
    return render(request, 'main/applications.html')