Repository per il progetto AI Develpment - mod 11 - DevOps

La soluzione ha incluso i seguenti step:

1.  Implementare un modello di Sentiment Analysis utilizzando un framework di Machine Learning (è stato utilizzato il modello suggerito). 

2.  Creare un pipeline di Continuous Integration/Continuous Deployment (CI/CD) con Jenkins per automatizzare il deploy del modello. 

3.  Configurare un'infrastruttura di monitoraggio utilizzando Prometheus e Grafana per registrare metriche come tempi di risposta, errore del modello e utilizzo delle risorse. 

4.  Documentare e gestire il progetto su un repository GitHub (https://https://github.com/stefano-clementini/sentiment-app).

Nel dettaglio il progetto include:

1.  app.py: file python che ha la funzione di espoorre RESTAPI con endpoint /predict e /metrics rispettivamente per predire il sentiment di una frase e recuperare le metriche dell'applicativo

2.  test_app.py: file python per eseguire i test funzionali sull'applicativo, necessari per prevenire errori prima della pubblicazione sul repository GitHub

3.  requirements.txt: file contenente le dipendenze (librerie necessarie per l'applicativo python)

4.  Jenkinsfile: file per implementare la CI\CD. 
    Le Fasi della Pipeline (Stages)
    - Checkout: Scarica il codice sorgente dal ramo main di GitHub.
    - Install Dependencies: Installa i pacchetti Python richiesti tramite pip.
    - Run Unit Tests: Esegue i test unitari con pytest. Se un test fallisce, la pipeline si blocca.
    - Docker Build: Crea l'immagine Docker dell'applicazione usando il Dockerfile presente nel progetto.
    - Docker Run / Deploy: Rilascia l'applicazione. Ferma e rimuove eventuali container vecchi con lo stesso nome, poi avvia il nuovo container esponendo la porta 8000

5.  Dockerfile: File che Docker usa per creare un'immagine. 
    Installa le dipendenze (requirement.txt) e contiene le informazioni per lanciare l'applicativo (app.py)

6.  prometheus.yml: file per la configurazione di Promethes per la collezione delle metriche
