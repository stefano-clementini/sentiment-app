
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import requests
import pickle
import uvicorn

import logging

logging.basicConfig(
    # logger configuration
    filename='log_restapi.log',
    level=logging.INFO,
    format= '[%(asctime)s] - %(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
 )
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API")

# Metriche Prometheus
REQUEST_TIME = Histogram('api_processing_seconds', 'Tempo di risposta dell API', ['/metrics', '/predict'])
MODEL_ERRORS = Counter('model_errors_total', 'Numero di errori o predizioni fallite')
CPU_USAGE = Gauge('process_cpu_usage_percent', 'Utilizzo CPU dell applicazione')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Utilizzo memoria dell applicazione')

url = 'https://github.com/Profession-AI/progetti-devops/raw/refs/heads/main/Deploy e monitoraggio di un modello di sentiment analysis per recensioni/sentiment_analysis_model.pkl'
filename = 'language_detection_pipeline.pkl'

# Scaricare preliminarmente il file nella cartella corrente
response = requests.get(url)
logger.info(f"GET URL status: {response.status_code}")
loaded_pipeline = None
if response.status_code == 200:
   logger.info("Model Download completed")
   # write file in local filesystem
   file_locale = open(filename,"wb")
   file_locale.write(response.content)
   file_locale.close()
else:
   logger.error("Model Download failed")

try:
    # ML model from file
    loaded_pipeline = pickle.load(open(filename,"rb"))
    logger.info("Model ready to predict")
except FileNotFoundError:
    logger.error("Model not found")


@app.get("/metrics")
def metrics():
    # Aggiorna le metriche hardware prima di esporle
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
def predict_sentiment(review: str):
    start_time = time.time()
    try:
        if not review.strip():
            raise ValueError("Giudizio mancante")
            
        predicted_sentiment = loaded_pipeline.predict([review])[0]
        
        # Determina il sentiment
        polarity = predicted_sentiment.polarity
        if polarity > 0:
            sentiment = "positivo"
        elif polarity < 0:
            sentiment = "negativo"
        else:
            sentiment = "neutro"
            
        # Registra il tempo di risposta
        REQUEST_TIME.labels(endpoint='/predict').observe(time.time() - start_time)
        
        return {"review": review, "sentiment": sentiment, "confidence": predicted_sentiment.confidence}
        
    except Exception as e:
        MODEL_ERRORS.inc()
        return {"error": str(e)}