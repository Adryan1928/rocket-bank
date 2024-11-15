import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from users.models import Client
from .models import Payment, Favorite, Pix
from .services import get_payments, set_payment
from django.shortcuts import render
from .models import Payment


def show_payments(request, id):
    if request.method == 'GET':
        payments = get_payments(id)
        user = Client.objects.get(pk=id)
        favorites = Favorite.objects.filter(user=id)

        context = {
            'post': id,
            'user': user,
            'favorites': favorites,
            'payments': payments
        }

        print("Cash: ", context)

        return render(request, 'pagamentos.html', context=context)

def add_favorite(request, id):
    key = request.POST.get('key')
    type = request.POST.get('type')

    print(key)

    pix = get_object_or_404(Pix, key=key)
    user = get_object_or_404(Client, pk=id)

    favorite = Favorite(user=user, pix=pix)
    favorite.save()

    return redirect(reverse('payments:show_payments', args=[id]))

def delete_favorite(request, id):
    favorite = Favorite.objects.get(id=id)
    user_id = favorite.user.id
    favorite.delete()

    return redirect(reverse('payments:show_payments', args=[user_id]))

def pix(request, id):
    if request.method == 'GET':
        step = request.GET.get('step')
        if step == 'select' or not step:
            return render(request, 'pix.html', {'post': id})
        elif step == 'finalizar':
            dados = request.GET.get('dados')
            dados_dict = json.loads(dados)

            senha = request.POST.get('senha')
            user = Client.objects.get(id=id)
            if senha != user.password:
                return render(request, 'pix_confirm.html', {'post': id, 'dados': dados_dict})

            pix = Favorite.objects.get(key=dados_dict['chave'])

            set_payment(id, pix.user_id, dados_dict['valor'])

            return redirect(reverse('payments:show_payments', args=[id]))

    chave = request.POST.get('chave')
    type = request.POST.get('radio')
    valor = request.POST.get('valor')

    try:
        pix = Favorite.objects.get(key=chave)
        return render(request, 'pix_confirm.html', {'post': id, 'dados': {'chave': chave, 'type': type, 'valor': valor}})
    except Favorite.DoesNotExist:
        return render(request, 'pix.html', {'post': id})

def depositos(request, id):
    if request.method == 'POST':
        valor = request.POST.get('valor')
        senha = request.POST.get('senha')
        user = Client.objects.get(pk=id)
        if senha == user.password:
            user.balance += float(valor)
            user.save()
            return redirect(reverse('payments:show_payments', args=[id]))
    return render(request, 'depositos.html', {'post': id})
