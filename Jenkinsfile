pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sentiment-api-app"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clona il repository Git contenente il codice dell'applicazione
                git branch: 'main', url: 'https://github.com/stefano-clementini/sentiment-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installa le dipendenze necessarie per l'applicazione
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Esegue pytest e genera un report standard
                sh 'pytest test_app.py -v'
            }
        }

        stage('Docker Build') {
            // Viene eseguito solo se i test passano
            // Costruisce l'immagine Docker dell'applicazione
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Docker Run / Deploy') {
            steps {
                // Ferma eventuali container vecchi e avvia il nuovo
                sh 'docker stop sentiment-container || true'
                sh 'docker rm sentiment-container || true'
                sh "docker run -d -p 8000:8000 --name sentiment-container ${DOCKER_IMAGE}:latest"
            }
        }
    }
}
