pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_IMAGE = 'vaishnavifale/mydjangoapp:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your source code from your version control system (e.g., Git)
                git 'https://github.com/yourusername/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build your Docker image
                script {
                    docker.build DOCKER_IMAGE
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Run your tests (you might need additional steps based on your test framework)
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                // Deploy your application to Minikube
                script {
                    // Use kubectl commands to apply your Kubernetes manifests
                    sh 'kubectl apply -f path/to/your/kubernetes/manifests'
                }
            }
        }
    }
}
