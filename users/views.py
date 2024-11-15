from django.shortcuts import render

from payments.services import get_payments


def index(request):
    return render(request, "index.html")

def signin(request):
    return render(request, "signin.html")

def signup(request):
    return render(request, "signup.html")

def real_state_financing(request):
    return render(request, "financing.html")

def extrato(request, id):
    payments = get_payments(id)
    if request.method == 'POST':
        text = request.POST.get('filtro')
        if len(text.strip()) == 0:
            return render(request, 'extrato.html', {'post': id, 'posts': payments})

        payments_filtrado = {'Entradas': [], 'Saidas': []}
        for en_sa in payments:
            for payment in payments[en_sa]:
                if payment['name'] == text:
                    payments_filtrado[en_sa].append(payment)

        return render(request, 'extrato.html', {'post': id, 'posts': payments_filtrado})

    return render(request, 'extrato.html', {'post': id, 'posts': payments})
