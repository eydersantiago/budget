from django.db import models

class Settings(models.Model):
    daily_min_spend = models.IntegerField(default=600)
    bus_monthly = models.IntegerField(default=100000)  # COP
    last_bus_topup = models.DateField(null=True, blank=True)  # p/ no duplicar

class CreditCard(models.Model):
    name = models.CharField(max_length=100, default="Principal")
    total_due = models.IntegerField(default=0)       # deuda total estimada
    installment_due = models.IntegerField(default=0) # cuota del mes
    cutoff_day = models.IntegerField(default=20)     # día de corte (1-28)
    payment_day = models.IntegerField(default=10)    # día de pago (1-28)

class Transaction(models.Model):
    INCOME="IN"; EXPENSE="OUT"
    KIND = [(INCOME,"Income"), (EXPENSE,"Expense")]
    kind = models.CharField(choices=KIND, max_length=3)
    amount = models.IntegerField()
    when = models.DateField()
    category = models.CharField(max_length=60, default="general")
    note = models.TextField(blank=True, default="")
