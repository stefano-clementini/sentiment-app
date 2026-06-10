pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sentiment-api-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m textblob.download_corpora'
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
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Docker Run / Deploy') {
            steps {
                // Ferma container vecchi e avvia il nuovo
                sh 'docker stop sentiment-container || true'
                sh 'docker rm sentiment-container || true'
                sh "docker run -d -p 8000:8000 --name sentiment-container ${DOCKER_IMAGE}:latest"
            }
        }
    }
}
