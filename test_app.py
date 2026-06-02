import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# 1. TEST DI PRECISIONE DEL MODELLO (Casi attesi)
@pytest.mark.parametrize(
    "input_text, expected_sentiment",
    [
        ("Amo assolutamente questo prodotto! Funziona perfettamente.", "positivo"),
        ("Quest è la peggiore esperienza della mia vita.", "negativo"),
        ("Il pacco è arrivato oggi.", "neutro"),
        ("Grande servizio e personale molto amichevole!", "positivo"),
        ("Servizio clienti orribile, voglio un rimborso.", "negativo"),
    ],
)
def test_sentiment_accuracy(input_text, expected_sentiment):
    """Verifica che il modello predica il sentiment corretto per frasi evidenti."""
    response = client.post(f"/predict?review={input_text}")
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == expected_sentiment
    assert "score" in data


# 2. TEST DELLE METRICHE DI ERRORE
def test_empty_input_error():
    """Verifica la gestione dell'errore con testo vuoto."""
    response = client.post("/predict?review= ")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Giudizio mancante"


# 3. TEST ENDPOINT METRICHE
def test_metrics_endpoint():
    """Assicura che l'endpoint di Prometheus risponda correttamente."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_processing_seconds" in response.text
