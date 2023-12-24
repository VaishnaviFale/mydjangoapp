#!/usr/bin/env groovy
pipeline {
    agent any

    

    stages {
        stage('Checkout') {
            steps {
                // Checkout your source code from your version control system (e.g., Git)
                git 'https://github.com/VaishnaviFale/mydjangoapp.git'
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Define Docker image name and tag
                    def dockerImage = "vaishnavifale/mydjangoapp-${env.BUILD_NUMBER}"
                    echo "Building Docker image: ${dockerImage}"

                    // Build Docker image
                    docker.build dockerImage, '-f Dockerfile .'

                    // Push Docker image to Docker Hub
                    docker.withRegistry('https://index.docker.io/v1/', 'vaishnavifale-docker-hub-credentials') {
                        echo "Pushing Docker image: ${dockerImage}"
                        docker.image(dockerImage).push()
                    }
                }
            }
        }

        stage('Run Tests') {
            steps  {
                script {
                    sh 'echo "Testing started.."'
                    
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv('Your SonarQube Server Configuration') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                    sh 'echo "Testing ended."'
                }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh 'echo "Debug information"'
                    
                    //def kubeconfig = credentials('kubeconfig-id')  // Replace 'kubeconfig-id' with the ID of your Kubernetes credentials

                         withCredentials([file(credentialsId: 'kubeconfig-id', variable: 'KUBECONFIG')]) {
                         sh "kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml"
                         sh "kubectl --kubeconfig=${KUBECONFIG} apply -f service.yaml"
                         sh "kubectl --kubeconfig=${KUBECONFIG} apply -f ingress.yaml"

                             sh 'echo "End of Debug information"'

                    }    

                    sh 'echo "DONE"'

                    
                }
            }
        }
    }
}
