pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
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
                    // Instalar dependências necessárias
                    sh 'apk add --no-cache curl'
                    
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
                    // Usar Docker diretamente
                    sh 'docker network create kealabs-network || true'
                    sh 'docker build -t kealabs-api ./api'
                    sh 'docker build -t kealabs-frontend ./frontend'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Usar Docker diretamente
                    sh '''docker run -d --name kealabs-api --network kealabs-network \
                          --env-file .env -p 8000:8000 kealabs-api'''
                    sh '''docker run -d --name kealabs-frontend --network kealabs-network \
                          --env-file .env -p 8501:8501 kealabs-frontend'''
                    sh 'sleep 45'
                    sh 'for i in 1 2 3 4 5 6 7 8 9 10; do curl -f http://localhost:8000/status && break || sleep 5; done'
                    sh 'for i in 1 2 3 4 5 6 7 8 9 10; do curl -f http://localhost:8501 && break || sleep 5; done'
                }
            }
            post {
                always {
                    script {
                        sh 'docker logs kealabs-api || true'
                        sh 'docker logs kealabs-frontend || true'
                        sh 'docker stop kealabs-api kealabs-frontend || true'
                        sh 'docker rm kealabs-api kealabs-frontend || true'
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
    
    post {
        always {
            cleanWs()
        }
        failure {
            script {
                sh 'docker logs kealabs-api || true'
                sh 'docker logs kealabs-frontend || true'
            }
        }
    }
}