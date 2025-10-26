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
        HOSTINGER_URL = 'kealabs.cloud'
        SERVER_IP = '72.60.140.128'
        APP_PORT = '8502'

        // Container adicional desabilitado
        // ADDITIONAL_CONTAINER_NAME = 'kealabs-extra'
        // ADDITIONAL_CONTAINER_IMAGE = 'kealabs-extra-image'
        // ADDITIONAL_CONTAINER_PORT = '9000'
        // ADDITIONAL_HOST_PORT = '9003'
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        // ansiColor('xterm') // removido: plugin/option não disponível no servidor
    }

    stages {
        stage('Verificar Ambiente') {
            steps {
                script {
                    sh "mkdir -p \"${env.DOCKER_CONFIG}\" && chmod 700 \"${env.DOCKER_CONFIG}\""
                    sh "echo DOCKER_CONFIG=${env.DOCKER_CONFIG}"
                    sh 'docker --version'
                    sh 'git --version || echo "Git não está disponível no container."'
                }
            }
        }

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Environment Setup') {
            steps {
                script {
                    if (fileExists('.env.example')) {
                        sh 'cp .env.example .env'
                    } else if (!fileExists('.env') && fileExists('.env.dev')) {
                        // fallback: if only env.dev exists, copy it when building dev
                        sh 'cp .env.dev .env || true'
                    } else {
                        echo ".env não encontrado, prossiga com variáveis do Jenkins se existirem."
                    }
                }
            }
        }

        stage('Build Images') {
            steps {
                script {
                    // garante DOCKER_CONFIG antes de executar docker CLI
                    sh "mkdir -p \"${env.DOCKER_CONFIG}\" && chmod 700 \"${env.DOCKER_CONFIG}\""
                    sh "docker network create ${env.DOCKER_NETWORK} || true"

                    // Build API
                    dir('api') {
                        sh 'if [ -f Dockerfile ]; then docker build --pull -t kealabs-api .; else echo "Dockerfile não encontrado em ./api"; exit 1; fi'
                    }

                    // Build Frontend
                    dir('frontend') {
                        sh 'if [ -f Dockerfile ]; then docker build --pull -t kealabs-frontend .; else echo "Dockerfile não encontrado em ./frontend"; exit 1; fi'
                    }

                    // Build adicional desabilitado
                    echo "Build de container adicional desabilitado"

                    // sanity check
                    sh 'docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | grep -E "kealabs-api|kealabs-frontend" || true'
                }
            }
        }

        stage('Smoke Test (optional)') {
            steps {
                script {
                    // Rodar containers temporários para teste rápido (não substitui deploy)
                    sh 'docker rm -f kealabs-api-test || true'
                    sh 'docker run -d --name kealabs-api-test --network none -p 127.0.0.1:18100:8000 kealabs-api || true'
                    sleep 6
                    sh 'curl -sS --fail http://127.0.0.1:18100/ || echo "API root não respondeu"'
                    sh 'docker rm -f kealabs-api-test || true'
                }
            }
            when { expression { return false } } // desabilitado por padrão; habilitar se desejar
        }

        stage('Deploy - Desenvolvimento') {
            when {
                expression {
                    return (env.BRANCH_NAME == 'develop') ||
                           (env.GIT_BRANCH != null && env.GIT_BRANCH.contains('develop')) ||
                           (env.BRANCH_NAME == null && params.DEPLOY_ENV == 'develop')
                }
            }
            steps {
                script {
                    sh 'cp .env.dev .env || true'
                    sh 'docker stop kealabs-api-dev kealabs-frontend-dev || true'
                    sh 'docker rm -f kealabs-api-dev kealabs-frontend-dev || true'

                    sh """docker run -d --name kealabs-api-dev --network ${env.DOCKER_NETWORK} \
                        --env-file .env -p 8001:8000 --restart unless-stopped kealabs-api"""

                    sh """docker run -d --name kealabs-frontend-dev --network ${env.DOCKER_NETWORK} \
                        --env-file .env -p 8502:8501 --restart unless-stopped kealabs-frontend"""

                    echo "Deploy de desenvolvimento concluído"
                }
            }
        }

        stage('Deploy - Homologação') {
            when {
                expression {
                    return (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' || env.BRANCH_NAME == 'hml') ||
                           (env.GIT_BRANCH != null && (env.GIT_BRANCH.contains('main') || env.GIT_BRANCH.contains('master') || env.GIT_BRANCH.contains('hml'))) ||
                           (env.BRANCH_NAME == null && params.DEPLOY_ENV == 'homolog')
                }
            }
            steps {
                script {
                    sh 'cp .env.homolog .env || true'
                    sh 'docker stop kealabs-api-homolog kealabs-frontend-homolog || true'
                    sh 'docker rm -f kealabs-api-homolog kealabs-frontend-homolog || true'

                    sh """docker run -d --name kealabs-api-homolog --network ${env.DOCKER_NETWORK} \
                        --env-file .env -p 8000:8000 --restart unless-stopped kealabs-api"""

                    sh """docker run -d --name kealabs-frontend-homolog --network ${env.DOCKER_NETWORK} \
                        --env-file .env -p 8501:8501 --restart unless-stopped kealabs-frontend"""

                    echo "Deploy de homologação concluído"ologação concluído!"
                    echo "Acesse a API em: http://${env.HOSTINGER_URL}:8000"
                    echo "Acesse o Frontend em: http://${env.HOSTINGER_URL}:8501"
                    echo "Acesse serviço extra em: http://${env.HOSTINGER_URL}:${ADDITIONAL_HOST_PORT}"
                    echo "Aplicação disponível em: http://${env.SERVER_IP}:${env.APP_PORT}"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado. DOCKER_CONFIG localizado em: ${env.DOCKER_CONFIG}"
            sh 'docker ps -a --filter "name=kealabs" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || true'
            // mostrar status do container adicional
            sh "docker ps -a --filter \"name=${ADDITIONAL_CONTAINER_NAME}\" --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}' || true"
        }
        failure {
            echo "Falha no pipeline. Verifique os logs."
        }
    }
}
