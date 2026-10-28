from fastapi.testclient import TestClient

from analyzer.app import app as app_module
from analyzer.constants import ANALYSE_COMPANY

client = TestClient(app_module.app)


def test_analyse_company_returns_generator_result(monkeypatch):
    async def fake_analysis(text):
        return [{"company_name": text}]

    monkeypatch.setattr(app_module.generator, "get_company_analysis", fake_analysis)

    response = client.post(ANALYSE_COMPANY, json={"query": "Kaspi"})

    assert response.status_code == 200
    assert response.json() == {"text": [{"company_name": "Kaspi"}]}


def test_analyse_company_without_query_returns_422():
    response = client.post(ANALYSE_COMPANY, json={})
    assert response.status_code == 422
