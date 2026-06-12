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
    - Install Dependencies: 
    - Run Unit Tests: Esegue i test unitari con pytest. Se un test fallisce, la pipeline si blocca. Installa i pacchetti Python richiesti tramite pip in un ambiente virtuale per poterlo rimuovere al termine.
    - Docker Build: Crea l'immagine Docker dell'applicazione usando il docker-compose che consente di avviare più container insieme. Una volta avviati i container sarà possibile accedere sulla RestAPI, su Prometheus (per osservare le metriche), su Grafana (per visualizzae i grafici dei dati collezionati da Prometheus)

5.  prometheus.yml: filee di configurazione per Prometheus, che richiama l'app

6.  grafana-datasource.yml: filee di configurazione per Grafana, che richiama Prometheus

7.  docker-compose: file per racchidere tutti i container necessari per il progetto.
    7.1  Dockerfile: file di configurazione per il container dell'app
    7.2  Dokerfile.jenkins: file per creare il container che deve contenere Jenkins 
    7.3  Dokerfile.promethes: file per creare il container che deve contenere Prometheus 
    7.4  Dokerfile.grafana: file per creare il container che deve contenere Grafana

-----------------------------------

Per avviare tutto, bisogna possedere un Docker in locale o un Docker-Hub.

Per creare il container:
docker build -t custom-jenkins:latest .

Per eseguirlo:
docker run -d \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins-local \
  custom-jenkins:latest

Una volta che sarà tutto deployato ed avviato sarà possibile raggiungere:
- App:         http://localhost:8000
- Prometheus:  http://localhost:9090
- Grafana:     http://localhost:3000 (admin/admin)
