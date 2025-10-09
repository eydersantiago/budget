import json
from datetime import date
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services.finance import decision_can_spend
from .services.nlp import classify

def _parse_json(request):
    if request.content_type not in (None, "", "application/json"):
        # Permitimos también sin header para facilitar pruebas
        pass
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        return json.loads(body)
    except json.JSONDecodeError:
        return None

@csrf_exempt
@require_POST
def can_spend(request):
    data = _parse_json(request)
    if data is None:
        return HttpResponseBadRequest("JSON inválido")

    try:
        today = date.fromisoformat(str(data["today"]))
        next_income = date.fromisoformat(str(data["next_income"]))
        cash_now = int(data["cash_now"])
        expense = int(data["expense"])
        include_bus = bool(data.get("include_bus", True))
        include_cc = bool(data.get("include_cc", True))
    except (KeyError, ValueError, TypeError) as e:
        return HttpResponseBadRequest(f"Campos inválidos o faltantes: {e}")

    res = decision_can_spend(
        cash_now=cash_now,
        expense=expense,
        next_income_date=next_income,
        today=today,
        include_bus=include_bus,
        include_cc=include_cc,
    )
    return JsonResponse(res, status=200)

@csrf_exempt
@require_POST
def classify_text(request):
    data = _parse_json(request)
    if data is None:
        return HttpResponseBadRequest("JSON inválido")

    text = str(data.get("text", "")).strip()
    if not text:
        return HttpResponseBadRequest("El campo 'text' es requerido")

    result = classify(text)
    return JsonResponse(result, status=200)
