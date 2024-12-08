from decimal import Decimal
from django.db import transaction
from .models import Payment, Client

@transaction.atomic
def get_payments(client_id, payments=None):
    if payments is None:
        payments = Payment.objects.all()

    incomes = payments.filter(receiver_id=client_id).select_related('sender__user')
    expenses = payments.filter(sender_id=client_id).select_related('receiver__user')

    result = {
        'Incomes': list(incomes.values('id', 'sender__user__id', 'sender__user__username', 'value', 'date')),
        'Expenses': list(expenses.values('id', 'receiver__user__id', 'receiver__user__username', 'value', 'date'))
    }
    return result

@transaction.atomic
def set_payment(sender_id, receiver_id, value):
    print("Valor: ", value)
    value = Decimal(value)

    sender = Client.objects.get(id=sender_id)
    receiver = Client.objects.get(id=receiver_id)

    print(f"{sender} sends to {receiver}")

    Payment.objects.create(sender=sender, receiver=receiver, value=value)

    receiver.cash += value
    sender.cash -= value

    receiver.save()
    sender.save()
