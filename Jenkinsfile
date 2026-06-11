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

        stage('Docker Build') {
            // Viene eseguito solo se i test passano
            steps {
                //sh "docker build -t ${DOCKER_IMAGE}:latest ."
                sh 'docker-compose up -d'
            }
        }
    }


    
    post {
        always {
            // Pulizia dell'area di lavoro alla fine della pipeline
            cleanWs()
        }
    }
}
