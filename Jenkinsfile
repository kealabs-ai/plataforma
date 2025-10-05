pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        PROJECT_NAME = 'kealabs-intelligence'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    if (fileExists('.env.example')) {
                        sh 'cp .env.example .env'
                    }
                    // Configurações para ambiente Docker
                    sh 'sed -i "s/DOCKER_ENV=false/DOCKER_ENV=true/g" .env'
                    sh 'sed -i "s/DB_HOST=72.60.140.128/DB_HOST=72.60.140.128/g" .env'
                    sh 'sed -i "s/FLASK_ENV=development/FLASK_ENV=production/g" .env'
                    sh 'sed -i "s/FLASK_DEBUG=1/FLASK_DEBUG=0/g" .env'
                }
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh 'docker-compose up -d'
                    sh 'sleep 45'
                    
                    // Health check da API
                    sh 'for i in {1..10}; do curl -f http://localhost:8000/status && break || sleep 5; done'
                    
                    // Health check do Frontend
                    sh 'for i in {1..10}; do curl -f http://localhost:8501 && break || sleep 5; done'
                    
                    // Verificar logs para erros
                    sh 'docker-compose logs api | grep -i error && exit 1 || true'
                }
            }
            post {
                always {
                    sh 'docker-compose logs'
                    sh 'docker-compose down'
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            sh 'docker-compose logs'
        }
    }
}