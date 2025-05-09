pipeline 
    agent any

    environment {
        DOCKER_IMAGE = 'ayushhyperflex/hyperflexcontrolplane'
        DOCKER_TAG = "latest"
        DOCKER_REGISTRY = 'https://hub.docker.com/' 

    stages {
       

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    // Run Trivy scan
                    sh '''
                        apt-get update
                        apt-get install -y trivy
                        trivy image ${DOCKER_IMAGE}:${DOCKER_TAG} --severity HIGH,CRITICAL --exit-code 1
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'  // Only push on main branch
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}") {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
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
                    
                    sh 'docker-compose up -d'
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