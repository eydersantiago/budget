import json
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class CanSpendViewTests(TestCase):
    def setUp(self):
        self.c = Client()

    def test_can_spend_ok_request(self):
        payload = {
            "today": "2025-10-08",
            "next_income": "2025-10-20",
            "cash_now": 200000,
            "expense": 1200,
            "include_bus": True,
            "include_cc": False
        }
        resp = self.c.post(
            "/api/can_spend/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("ok", data)
        self.assertIn("per_day", data)
        self.assertIn("net_after_oblig", data)
        self.assertIn("oblig", data)

    def test_can_spend_bad_request(self):
        # falta 'today'
        payload = {
            "next_income": "2025-10-20",
            "cash_now": 10000,
            "expense": 1200
        }
        resp = self.c.post(
            "/api/can_spend/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

class ClassifyTextTests(TestCase):
    def setUp(self):
        self.c = Client()

    @patch("core.services.nlp.classify", return_value={"label":"POSITIVE","score":0.99})
    def test_classify_text_ok(self, mock_classify):
        payload = {"text":"compré dulces por 1200"}
        resp = self.c.post(
            "/api/classify_text/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        response_data = resp.json()
        self.assertEqual(response_data["label"], "POSITIVE")
        self.assertAlmostEqual(response_data["score"], 0.99, places=1)


    def test_classify_text_missing(self):
        resp = self.c.post(
            "/api/classify_text/",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
