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
            steps {
                // Run your tests (you might need additional steps based on your test framework)
               echo "Testing..."
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    def kubeconfig = credentials('kubeconfig-id')  // Replace 'kubeconfig-id' with the ID of your Kubernetes credentials
                    sh "kubectl --kubeconfig=${kubeconfig} apply -f deployment.yaml"
                    sh "kubectl --kubeconfig=${kubeconfig} apply -f service.yaml"
                    sh "kubectl --kubeconfig=${kubeconfig} apply -f ingress.yaml"
                }
            }
        }
    }
}
