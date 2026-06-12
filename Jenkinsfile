pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sentiment-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/stefano-clementini/sentiment-app'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Creiamo un ambiente virtuale isolato per eseguire pytest
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest test_app.py -v
                '''
            }
        }
        /*
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Esegue pytest e genera un report standard
                sh 'pytest test_app.py -v'
            }
        }
        */

        stage('Docker Deploy') {
            steps {
                // Ferma eventuali container vecchi, builda la nuova immagine e la avvia
                sh '''
                    docker-compose down
                    docker-compose up --build -d
                '''
            }
        } 
    }


    
    post {
        always {
            // Pulisce il workspace di Jenkins
            cleanWs()
        }
        failure {
            echo "La pipeline è fallita. Controlla i test o i comandi Docker."
        }
    }
}

