import re
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator

from .services import get_payments, set_payment
from users.models import Client
from .models import Payment, Favorite, Pix

from decimal import Decimal


@login_required
def show_payments(request):
    if request.method == 'GET':
        payments_all = Payment.objects.all().order_by('-date')
        user = Client.objects.get(user=request.user)
        favorites = Favorite.objects.filter(user=user)

        paginator = Paginator(payments_all, 3)
        page = request.GET.get('page', 1)
        payments = paginator.page(page)


        payments_list = Payment.objects.filter(id__in=[payment.id for payment in payments.object_list])

        payments.object_list = get_payments(request.user.client.id, payments_list)

        context = {
            'favorites': favorites,
            'payments': payments
        }

        return render(request, 'pagamentos.html', context=context)

@login_required
def add_favorite(request):
    key = request.POST.get('key')
    type = request.POST.get('type')

    pix = get_object_or_404(Pix, key=key)
    user = get_object_or_404(Client, user=request.user)
    print(user)

    favorite = Favorite(user=user, pix=pix)
    favorite.save()

    return redirect(reverse('payments:show_payments'))

@login_required
def delete_favorite(request, id):
    favorite = Favorite.objects.get(id=id)
    if request.user.id != favorite.user.user.id:
            return redirect(reverse('payments:show_payments'))
    favorite.delete()

    return redirect(reverse('payments:show_payments'))

@login_required
def pix(request, step=None):
    if step == 'select' or not step:
        return render(request, 'pix.html')
    elif step == 'finalizar':
        dados = request.session.get('dados')
        print(dados)
        if not dados:
            return redirect(reverse('payments:pix'))

        senha = request.POST.get('senha')
        user = Client.objects.get(user=request.user)
        if not user.user.check_password(senha):
            print("Errada")
            return render(request, 'pix_confirm.html', {'dados': dados})

        pix = Pix.objects.get(key=dados['chave'])

        set_payment(user.id, pix.user_id, dados['valor'], pix)

        # Clear session data after use
        del request.session['dados']

        return redirect(reverse('payments:show_payments'))

    chave = request.POST.get('chave')
    type = request.POST.get('radio')
    valor = request.POST.get('valor')

    try:
        pix = Pix.objects.get(key=chave)
        dados = {'chave': chave, 'type': type, 'valor': valor}
        request.session['dados'] = dados
        return render(request, 'pix_confirm.html')
    except Pix.DoesNotExist:
        return render(request, 'pix.html', {'error': 'Chave Pix não encontrada'})

@login_required
def depositos(request):
    if request.method == 'POST':
        user =  Client.objects.get(user = request.user)
        valor = request.POST.get('valor')
        senha = request.POST.get('senha')
        if user.user.check_password(senha):
            try:
                user.cash += Decimal(valor)
                user.save()
                return redirect(reverse('payments:show_payments'))
            except:
                pass
    return render(request, 'depositos.html')

@login_required
def extrato(request):
    if request.method == 'POST':
        payments = Payment.objects.filter(
            Q(receiver__user__id=request.user.id) | Q(sender__user__id=request.user.id)
        )

        search_query = request.POST.get('search', '').strip()
        order_by_date = request.POST.get('Data', None)
        order_by_name = request.POST.get('nomes', None)

        # Apply ordering by date
        if order_by_date:
            payments = payments.order_by(order_by_date)

        # Apply ordering by name
        if order_by_name:
            if order_by_name == 'ascending':
                payments = payments.order_by(order_by_date, 'sender__user__first_name') if order_by_date else payments.order_by('sender__user__first_name')
            elif order_by_name == 'descending':
                payments = payments.order_by(order_by_date, '-sender__user__first_name') if order_by_date else payments.order_by('-sender__user__first_name')

        if search_query != '':
            # Filter by user
            if (search_query.isnumeric()):
                # Find integer and float values and convert floats to intl pattern
                query_values = re.findall(r'(?<!\S)\d+(?:,\d+)?(?!\S)', search_query)
                float_values = [float(value.replace(',', '.')) for value in query_values]

                # Filter by float values
                payments = payments.filter(value__in=float_values)
            else:
                payments = payments.filter(
                    Q(sender__user__id=request.user.id) & Q(receiver__user__email__icontains=search_query) |
                    Q(sender__user__id=request.user.id) & Q(receiver__user__username__icontains=search_query) |
                    Q(sender__user__id=request.user.id) & Q(receiver__user__first_name__icontains=search_query) |
                    Q(sender__user__id=request.user.id) & Q(receiver__user__last_name__icontains=search_query) |
                    Q(receiver__user__id=request.user.id) & Q(sender__user__email__icontains=search_query) |
                    Q(receiver__user__id=request.user.id) & Q(sender__user__username__icontains=search_query) |
                    Q(receiver__user__id=request.user.id) & Q(sender__user__first_name__icontains=search_query) |
                    Q(receiver__user__id=request.user.id) & Q(sender__user__last_name__icontains=search_query)
                )

            

            # print(payments)

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
                        payments = payments.filter(date=date_obj)
                    except ValueError:
                        pass

        payments = get_payments(request.user.client.id, payments)
    else:
        payments = get_payments(request.user.client.id)

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

        return redirect(reverse('payments:show_payments'))

    return render(request, 'register_pix.html')
