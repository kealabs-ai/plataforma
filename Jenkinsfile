pipeline {
    agent {
        docker {
            image 'docker:20.10.24-cli'
            args '-v /var/run/docker.sock:/var/run/docker.sock --privileged'
        }
    }

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        PROJECT_NAME = 'kealabs-intelligence'
        DOCKER_NETWORK = 'kealabs-network'
        DOCKER_CONFIG = "${env.WORKSPACE}/.docker"
        HOSTINGER_URL = 'agro.kealabs.com.br' // Altere para seu domínio ou IP real
        SERVER_IP = '72.60.140.128'     // Altere para seu IP ou domínio real
        APP_PORT = '8502'                          // Altere para a porta do frontend
    }

    stages {
        stage('Verificar Ambiente') {
            steps {
                sh 'docker --version'
                sh 'git --version || echo "Git não está disponível no container."'
            }
        }

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
                    echo "Acesse a API em: https://${HOSTINGER_URL}:8001"
                    echo "Acesse o Frontend em: https://${HOSTINGER_URL}:8502"
                    echo "Aplicação disponível em: http://${env.SERVER_IP}:${env.APP_PORT}"
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
                    echo "Acesse a API em: https://${HOSTINGER_URL}:8000"
                    echo "Acesse o Frontend em: https://${HOSTINGER_URL}:8501"
                    echo "Aplicação disponível em: http://${env.SERVER_IP}:${env.APP_PORT}"
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
