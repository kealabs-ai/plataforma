pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
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
                script {
                    // Verificar se docker-compose existe, senão usar docker
                    def composeExists = sh(script: 'which docker-compose', returnStatus: true) == 0
                    if (composeExists) {
                        sh 'docker-compose build'
                    } else {
                        // Usar Docker diretamente
                        sh 'docker network create kealabs-network || true'
                        sh 'docker build -t kealabs-api ./api'
                        sh 'docker build -t kealabs-frontend ./frontend'
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    def composeExists = sh(script: 'which docker-compose', returnStatus: true) == 0
                    if (composeExists) {
                        sh 'docker-compose up -d'
                        sh 'sleep 45'
                        sh 'for i in {1..10}; do curl -f http://localhost:8000/status && break || sleep 5; done'
                        sh 'for i in {1..10}; do curl -f http://localhost:8501 && break || sleep 5; done'
                    } else {
                        // Usar Docker diretamente
                        sh '''docker run -d --name kealabs-api --network kealabs-network \
                              --env-file .env -p 8000:8000 kealabs-api'''
                        sh '''docker run -d --name kealabs-frontend --network kealabs-network \
                              --env-file .env -p 8501:8501 kealabs-frontend'''
                        sh 'sleep 45'
                        sh 'for i in {1..10}; do curl -f http://localhost:8000/status && break || sleep 5; done'
                        sh 'for i in {1..10}; do curl -f http://localhost:8501 && break || sleep 5; done'
                    }
                }
            }
            post {
                always {
                    script {
                        def composeExists = sh(script: 'which docker-compose', returnStatus: true) == 0
                        if (composeExists) {
                            sh 'docker-compose logs || true'
                            sh 'docker-compose down || true'
                        } else {
                            sh 'docker logs kealabs-api || true'
                            sh 'docker logs kealabs-frontend || true'
                            sh 'docker stop kealabs-api kealabs-frontend || true'
                            sh 'docker rm kealabs-api kealabs-frontend || true'
                        }
                    }
                }
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
                script {
                    def composeExists = sh(script: 'which docker-compose', returnStatus: true) == 0
                    if (composeExists) {
                        sh 'docker-compose up -d --build'
                    } else {
                        // Deploy com Docker
                        sh 'docker stop kealabs-api kealabs-frontend || true'
                        sh 'docker rm kealabs-api kealabs-frontend || true'
                        sh '''docker run -d --name kealabs-api --network kealabs-network \
                              --env-file .env -p 8000:8000 --restart unless-stopped kealabs-api'''
                        sh '''docker run -d --name kealabs-frontend --network kealabs-network \
                              --env-file .env -p 8501:8501 --restart unless-stopped kealabs-frontend'''
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            script {
                def composeExists = sh(script: 'which docker-compose', returnStatus: true) == 0
                if (composeExists) {
                    sh 'docker-compose logs || true'
                } else {
                    sh 'docker logs kealabs-api || true'
                    sh 'docker logs kealabs-frontend || true'
                }
            }
        }
    }
}