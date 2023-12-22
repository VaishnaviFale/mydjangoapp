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
                    def dockerImage = 'vaishnavifale/mydjangoapp:latest'

                    // Build Docker image
                    docker.build dockerImage, '-f Dockerfile .'

                    // Push Docker image to Docker Hub
                    docker.withRegistry('https://registry-1.docker.io', 'docker-hub-credentials') {
                        docker.image(dockerImage).push()
                    }
                }
            }

        stage('Run Tests') {
            steps {
                // Run your tests (you might need additional steps based on your test framework)
               echo "Testing..."
            }
        }

        stage('Deploy to Minikube') {
            steps {
                // Deploy your application to Minikube
                 echo "Deploying..."
            }
        }
    }
}
