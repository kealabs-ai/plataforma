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

        stage('Deploy - Desenvolvimento') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    sh 'cp .env.dev .env'
                    sh 'docker stop kealabs-api-dev kealabs-frontend-dev || true'
                    sh 'docker rm kealabs-api-dev kealabs-frontend-dev || true'
                    sh '''docker run -d --name kealabs-api-dev --network kealabs-network \
                        --env-file .env -p 8001:8000 --restart unless-stopped kealabs-api'''
                    sh '''docker run -d --name kealabs-frontend-dev --network kealabs-network \
                        --env-file .env -p 8502:8501 --restart unless-stopped kealabs-frontend'''
                    echo "Deploy de desenvolvimento concluído!"
                }
            }
        }

        stage('Deploy - Homologação') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh 'cp .env.homolog .env'
                    sh 'docker stop kealabs-api-homolog kealabs-frontend-homolog || true'
                    sh 'docker rm kealabs-api-homolog kealabs-frontend-homolog || true'
                    sh '''docker run -d --name kealabs-api-homolog --network kealabs-network \
                        --env-file .env -p 8000:8000 --restart unless-stopped kealabs-api'''
                    sh '''docker run -d --name kealabs-frontend-homolog --network kealabs-network \
                        --env-file .env -p 8501:8501 --restart unless-stopped kealabs-frontend'''
                    echo "Deploy de homologação concluído!"
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