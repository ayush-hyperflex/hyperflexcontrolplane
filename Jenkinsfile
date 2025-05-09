pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ayushhyperflex/hyperflexcontrolplane"
        DOCKER_TAG = "latest"
        DOCKER_REGISTRY = "hub.docker.com"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}", ".")
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Failed to build Docker image: ${e.message}")
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    // Using Docker to run Trivy instead of installing it
                    sh '''
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${DOCKER_IMAGE}:${DOCKER_TAG} \
                            --severity HIGH,CRITICAL --exit-code 1
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    try {
                        docker.withRegistry("https://${DOCKER_REGISTRY}") {
                            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
                        }
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Failed to push Docker image: ${e.message}")
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    try {
                        sh 'docker-compose up -d'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Failed to deploy: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
