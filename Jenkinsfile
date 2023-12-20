pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("mydjangoapp:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest'
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh 'kubectl apply -f k8s/'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQubeServer') {
                        sh 'sonar-scanner'
                    }
                }
            }
        }
    }
}

