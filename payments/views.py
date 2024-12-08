import re
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .services import get_payments, set_payment
from users.models import Client
from .models import Payment, Favorite, Pix


@login_required
def show_payments(request, id):
    if request.method == 'GET':
        if request.user.client.id != id:
            return redirect(reverse('payments:show_payments', args=[request.user.client.id]))
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

@login_required
def add_favorite(request, id):
    if request.user.client.id != id:
            return redirect(reverse('payments:show_payments', args=[request.user.client.id]))
    key = request.POST.get('key')
    type = request.POST.get('type')

    print(key)

    pix = get_object_or_404(Pix, key=key)
    user = get_object_or_404(Client, pk=id)

    favorite = Favorite(user=user, pix=pix)
    favorite.save()

    return redirect(reverse('payments:show_payments', args=[id]))

@login_required
def delete_favorite(request, id):
    favorite = Favorite.objects.get(id=id)
    if request.user.id != favorite.user.user.id:
            return redirect(reverse('payments:show_payments', args=[request.user.client.id]))
    user_id = favorite.user.id
    favorite.delete()

    return redirect(reverse('payments:show_payments', args=[user_id]))

@login_required
def pix(request, id, step=None):
    print(step)
    if step == 'select' or not step:
        return render(request, 'pix.html', {'post': id})
    elif step == 'finalizar':
        dados = request.session.get('dados')
        print(dados)
        if not dados:
            return redirect(reverse('payments:pix', args=[id]))

        senha = request.POST.get('senha')
        user = Client.objects.get(id=id)
        print(user.user.password)
        if senha != user.user.password:
            print("Errada")
            return render(request, 'pix_confirm.html', {'post': id, 'dados': dados})

        pix = Pix.objects.get(key=dados['chave'])

        set_payment(request.user.client.id, pix.user_id, dados['valor'])

        # Clear session data after use
        del request.session['dados']

        return redirect(reverse('payments:show_payments', args=[id]))

    chave = request.POST.get('chave')
    type = request.POST.get('radio')
    valor = request.POST.get('valor')

    try:
        pix = Pix.objects.get(key=chave)
        dados = {'chave': chave, 'type': type, 'valor': valor}
        request.session['dados'] = dados
        return render(request, 'pix_confirm.html', {'post': id})
    except Pix.DoesNotExist:
        return render(request, 'pix.html', {'post': id, 'error': 'Chave Pix não encontrada'})

@login_required
def depositos(request, id):
    print(request.user)
    if request.user.client.id != id:
            return redirect(reverse('payments:show_payments', args=[request.user.client.id]))
    if request.method == 'POST':
        valor = request.POST.get('valor')
        senha = request.POST.get('senha')
        user = Client.objects.get(pk=id)
        if senha == user.user.password:
            user.cash += float(valor)
            user.save()
            return redirect(reverse('payments:show_payments', args=[id]))
    return render(request, 'depositos.html', {'post': id})

@login_required
def extrato(request):
    payments = Payment.objects.all()
    if request.method == 'POST':
        search_query = request.POST.get('search', '').strip()

        # Filter by user
        filtered_payments = payments.filter(
            Q(sender__user__email__icontains=search_query) |
            Q(sender__user__username__icontains=search_query) |
            Q(sender__user__first_name__icontains=search_query) |
            Q(sender__user__last_name__icontains=search_query)
        )

        # Find integer and float values and convert floats to intl pattern
        query_values = re.findall(r'(?<!\S)\d+(?:,\d+)?(?!\S)', search_query)
        float_values = [float(value.replace(',', '.')) for value in query_values]

        # Filter by float values
        filtered_payments = filtered_payments.filter(value__in=float_values)

        # Filter by dates
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
            r'\b\d{2}/\d{2}/\d{4}\b'   # DD/MM/YYYY
        ]
        for pattern in date_patterns:
            date_matches = re.findall(pattern, search_query)
            for date_str in date_matches:
                try:
                    if '-' in date_str:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    else:
                        date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
                    filtered_payments = filtered_payments.filter(date=date_obj)
                except ValueError:
                    pass

        payments = get_payments(request.user.id, filtered_payments)

    context = {
        'payments': payments
    }

    return render(request, 'extrato.html', context)

@login_required
def register_pix(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        type = request.POST.get('type')
        user = request.user.client

        Pix.objects.create(user=user, key=key, type=type)

        return redirect(reverse('payments:show_payments', args=[user.id]))

    return render(request, 'register_pix.html')
