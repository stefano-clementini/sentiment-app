
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import pickle
import logging
import os

logging.basicConfig(
    filename='log_restapi.log',
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global loaded_pipeline
    try:
        loaded_pipeline = load_model(MODEL_FILENAME)
    except Exception:
        loaded_pipeline = None
        logger.exception("Impossibile caricare il modello")
    yield

app = FastAPI(title="Sentiment Analysis API", lifespan=lifespan)

# Metriche Prometheus
REQUEST_TIME = Histogram('api_processing_seconds', 'Tempo di risposta dell API', ['endpoint'])
MODEL_ERRORS = Counter('model_errors_total', 'Numero di errori o predizioni fallite')
CPU_USAGE = Gauge('process_cpu_usage_percent', 'Utilizzo CPU dell applicazione')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Utilizzo memoria dell applicazione')

MODEL_FILENAME = 'language_detection_pipeline.pkl'
loaded_pipeline = None

LABEL_MAP = {
    'positive': 'positivo',
    'negative': 'negativo',
    'neutral': 'neutro',
}


def load_model(model_path: str):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modello non trovato: {model_path}")
    with open(model_path, 'rb') as model_file:
        pipeline = pickle.load(model_file)
    logger.info("Modello caricato da %s", model_path)
    return pipeline


@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict")
def predict_sentiment(review: str):
    start_time = time.time()
    try:
        if loaded_pipeline is None:
            logger.error("Predizione richiesta ma il modello non è caricato")
            raise HTTPException(status_code=503, detail="Modello non disponibile")

        if not review or not review.strip():
            raise HTTPException(status_code=400, detail="Giudizio mancante")

        predicted_label = loaded_pipeline.predict([review])[0]
        sentiment = LABEL_MAP.get(str(predicted_label).lower(), str(predicted_label))

        confidence = None
        if hasattr(loaded_pipeline, 'predict_proba'):
            probabilities = loaded_pipeline.predict_proba([review])[0]
            confidence = float(max(probabilities))

        REQUEST_TIME.labels(endpoint='/predict').observe(time.time() - start_time)

        result = {
            'review': review,
            'sentiment': sentiment,
        }
        if confidence is not None:
            result['confidence'] = round(confidence, 4)

        return result

    except HTTPException:
        MODEL_ERRORS.inc()
        raise
    except Exception as exc:
        MODEL_ERRORS.inc()
        logger.exception("Errore nella predizione")
        raise HTTPException(status_code=500, detail=str(exc))