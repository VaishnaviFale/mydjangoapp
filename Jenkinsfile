pipeline {
    agent any

    

    stages {
        stage('Checkout') {
            steps {
                // Checkout your source code from your version control system (e.g., Git)
                git 'https://github.com/VaishnaviFale/mydjangoapp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "building..."
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
