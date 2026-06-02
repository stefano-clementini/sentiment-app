import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# 1. TEST DI PRECISIONE DEL MODELLO (Casi attesi)
# Utilizziamo frasi con sentimenti chiari per verificare che il modello predica correttamente.
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
    """
    Verifica che il modello predica il sentiment corretto per frasi evidenti.
    """
    response = client.post(f"/predict?review={input_text}")
    # Controlla che la risposta sia 200 OK e che il sentiment predetto corrisponda a quello atteso.
    assert response.status_code == 200
    data = response.json()
    # Verifica che il sentiment predetto sia quello atteso e che sia presente un punteggio.
    assert data["sentiment"] == expected_sentiment
    # Controlla che il punteggio sia presente e sia un numero (non negativo).
    assert "confidence" in data


# 2. TEST DELLE METRICHE DI ERRORE
def test_empty_input_error():
    """
    Verifica la gestione dell'errore con testo vuoto.
    """
    response = client.post("/predict?review= ")
    # Controlla che la risposta sia 200 OK
    assert response.status_code == 200
    data = response.json()
    # Verifica che la risposta contenga un messaggio di errore specifico per input vuoto.
    assert "error" in data
    assert data["error"] == "Giudizio mancante"


# 3. TEST ENDPOINT METRICHE
def test_metrics_endpoint():
    """
    Assicura che l'endpoint di Prometheus risponda correttamente.
    """
    response = client.get("/metrics")
    # Controlla che la risposta sia 200 OK
    assert response.status_code == 200
    # Verifica che la risposta contenga la metrica personalizzata "api_processing_seconds" che abbiamo definito.
    assert "api_processing_seconds" in response.text
