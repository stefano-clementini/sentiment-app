import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize(
    "input_text",
    [
        "Amo assolutamente questo prodotto! Funziona perfettamente.",
        "Quest è la peggiore esperienza della mia vita.",
        "Il pacco è arrivato oggi.",
        "Grande servizio e personale molto amichevole!",
        "Servizio clienti orribile, voglio un rimborso.",
    ],
)

# 1. TEST DI RISPOSTA DEL MODELLO
def test_sentiment_response(client, input_text):
    """Verifica che l'endpoint restituisca sentiment e confidence per richieste valide."""
    response = client.post("/predict", params={"review": input_text})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] in {"positivo", "negativo", "neutro"}
    assert "confidence" in data


# 2. TEST DELLE METRICHE DI ERRORE
def test_empty_input_error(client):
    """Verifica la gestione dell'errore con testo vuoto."""
    response = client.post("/predict", params={"review": " "})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Giudizio mancante"


# 3. TEST ENDPOINT METRICHE
def test_metrics_endpoint(client):
    """Assicura che l'endpoint di Prometheus risponda correttamente."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_processing_seconds" in response.text
