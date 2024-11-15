from django.db import transaction
from .models import Payment, Client

@transaction.atomic
def get_payments(client_id):
    entradas = Payment.objects.filter(receiver_id=client_id).select_related('sender__user')
    saidas = Payment.objects.filter(sender_id=client_id).select_related('receiver__user')

    payments = {
        'Entradas': list(entradas.values('id', 'sender__user__id', 'sender__user__username', 'value', 'date')),
        'Saidas': list(saidas.values('id', 'receiver__user__id', 'receiver__user__username', 'value', 'date'))
    }
    return payments

@transaction.atomic
def set_payment(sender_id, receiver_id, value):
    sender = Client.objects.get(id=sender_id)
    receiver = Client.objects.get(id=receiver_id)

    Payment.objects.create(sender=sender, receiver=receiver, value=value)

    receiver.cash += value
    sender.cash -= value

    receiver.save()
    sender.save()
