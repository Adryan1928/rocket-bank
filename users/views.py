from django.shortcuts import render, redirect
from payments.services import get_payments
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from users.models import Client


def index(request):
    return render(request, "index.html")

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect(f"/payments/{user.client.id}", id=user.id)
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
    return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')

        if password != password_confirm:
            messages.add_message(request, constants.ERROR, 'As senhas não conferem')

        else:
            try:
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                client = Client(user=user, phone_number=phone_number, cpf=cpf, birth_date=birth_date, cash=0)
                client.save()
                return redirect('signin')
            except Exception as e:
                print(e)
                messages.add_message(request, constants.ERROR, 'Dados inválidos ou outro usuário já possui este email')

    return render(request, "signup.html")

def real_state_financing(request):
    return render(request, "financing.html")
