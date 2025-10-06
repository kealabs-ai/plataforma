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
                    } else if (!fileExists('.env')) {
                        error "Arquivo .env.example e .env não encontrados!"
                    }
                    sh 'sed -i "s/DOCKER_ENV=false/DOCKER_ENV=true/g" .env || true'
                    sh 'sed -i "s/FLASK_ENV=development/FLASK_ENV=production/g" .env || true'
                    sh 'sed -i "s/FLASK_DEBUG=1/FLASK_DEBUG=0/g" .env || true'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker --version || (echo "Docker não está instalado!" && exit 1)'
                    sh 'docker network create kealabs-network || true'
                    sh 'docker build -t kealabs-api ./api'
                    sh 'docker build -t kealabs-frontend ./frontend'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'docker stop kealabs-api kealabs-frontend || true'
                    sh 'docker rm kealabs-api kealabs-frontend || true'
                    sh '''docker run -d --name kealabs-api --network kealabs-network \
                        --env-file .env -p 8000:8000 kealabs-api'''
                    sleep 30
                    sh 'curl -f http://localhost:8000/status || (echo "API health check failed" && exit 1)'
                    sh 'docker logs kealabs-api || true'
                    sh 'docker stop kealabs-api || true'
                    sh 'docker rm kealabs-api || true'
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
                    sh 'docker stop kealabs-api kealabs-frontend || true'
                    sh 'docker rm kealabs-api kealabs-frontend || true'
                    sh '''docker run -d --name kealabs-api --network kealabs-network \
                        --env-file .env -p 8000:8000 --restart unless-stopped kealabs-api'''
                    sh '''docker run -d --name kealabs-frontend --network kealabs-network \
                        --env-file .env -p 8501:8501 --restart unless-stopped kealabs-frontend'''
                    echo "Deploy concluído com sucesso"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado."
        }
        failure {
            echo "Falha no pipeline. Verifique os logs."
        }
    }
}