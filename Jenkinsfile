pipeline {
    // 1. Mudar o agente global para 'none'. Isso força a definição de um agente em cada stage.
    agent none 

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        PROJECT_NAME = 'kealabs-intelligence'
        DOCKER_NETWORK = 'kealabs-network'
    }

    stages {
        // Stages de preparação podem rodar em qualquer agente (o padrão do Jenkins)
        stage('Checkout') {
            agent any
            steps {
                checkout scm
            }
        }

        stage('Environment Setup') {
            agent any
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

        // 2. Stage de Build agora usa um agente Docker
        stage('Build') {
            agent {
                docker {
                    // Usamos uma imagem que já contém o cliente Docker
                    image 'docker:dind'
                    // IMPORTANT: Montamos o socket do Docker do host para que o container possa
                    // se comunicar e executar comandos (build, run, network) no host principal.
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    // O comando 'docker --version' não é mais necessário aqui.
                    // Se o agente Docker falhar, o Jenkins já vai reportar o erro.
                    
                    sh 'docker network create kealabs-network || true'
                    sh 'docker build -t kealabs-api ./api'
                    sh 'docker build -t kealabs-frontend ./frontend'
                }
            }
        }

        // 3. Stages de Deploy também usam o agente Docker
        stage('Deploy - Desenvolvimento') {
            agent {
                docker {
                    image 'docker:dind'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
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
            agent {
                docker {
                    image 'docker:dind'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
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
