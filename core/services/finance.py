from datetime import date
from calendar import monthrange
from core.models import Settings, CreditCard

def decision_can_spend(cash_now:int, expense:int, next_income_date:date, today:date,
                       include_bus:bool=True, include_cc:bool=True):
    s = Settings.objects.first() or Settings.objects.create()
    days = max(1, (next_income_date - today).days)

    oblig = 0
    if include_bus:
        oblig += s.bus_monthly

    if include_cc:
        cc = CreditCard.objects.first()
        if cc:
            pay_date = today.replace(day=min(cc.payment_day, monthrange(today.year, today.month)[1]))
            if pay_date < today:
                m = today.month + 1 if today.month < 12 else 1
                y = today.year if today.month < 12 else today.year + 1
                pay_date = date(y, m, min(cc.payment_day, monthrange(y, m)[1]))
            if pay_date <= next_income_date:
                oblig += cc.installment_due

    net = cash_now - oblig
    per_day = max(0, net // days)
    ok = (per_day >= s.daily_min_spend) and (expense <= per_day)
    return {"ok": ok, "per_day": per_day, "net_after_oblig": net, "oblig": oblig}
