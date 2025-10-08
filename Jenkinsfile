pipeline {
    agent any
    
    environment {
        PROJECT_NAME = 'kealabs-intelligence'
        DOCKER_NETWORK = 'kealabs-network'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Environment Setup') {
            steps {
                sh 'cp .env.example .env || echo "Arquivo .env.example não encontrado"'
                sh 'sed -i "s/DOCKER_ENV=false/DOCKER_ENV=true/g" .env || true'
                sh 'sed -i "s/FLASK_ENV=development/FLASK_ENV=production/g" .env || true'
                sh 'sed -i "s/FLASK_DEBUG=1/FLASK_DEBUG=0/g" .env || true'
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker --version'
                sh 'docker network create kealabs-network || true'
                sh 'docker build -t kealabs-api ./api'
                sh 'docker build -t kealabs-frontend ./frontend'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker stop kealabs-api kealabs-frontend || true'
                sh 'docker rm kealabs-api kealabs-frontend || true'
                sh '''docker run -d --name kealabs-api --network kealabs-network \
                      --env-file .env -p 8000:8000 kealabs-api'''
                sh 'sleep 30'
                sh 'curl -f http://localhost:8000/status || echo "API health check failed"'
                sh 'docker logs kealabs-api || true'
                sh 'docker stop kealabs-api || true'
                sh 'docker rm kealabs-api || true'
            }
        }
        
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh 'chmod +x deploy.sh'
                sh './deploy.sh'
            }
        }
    }
}
