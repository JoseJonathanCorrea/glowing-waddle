pipeline {
    agent any
    
    stages {
        stage('Build Docker Images') {
            steps {
                sh 'docker compose up -d flask_db'
                sh 'docker compose build'
            }
        }
        stage('Run Docker Containers') {
            steps {
                sh 'docker compose up --build -d flask_app'
            }
        }
    }
}