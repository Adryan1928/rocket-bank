from django.shortcuts import render


def index(request):
    return render(request, "index.html")

def real_state_financing():
    return render('financing.html')
