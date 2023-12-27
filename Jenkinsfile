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
            steps {
                script {
                    ///sh 'pip install pytest'
                    //sh 'pytest test_example.py'
                     // Install python3-venv package with sudo
    sh 'sudo apt install -y python3.11-venv'

    // Create a virtual environment, activate it, and run subsequent commands
    sh '''
        /usr/bin/python3.11 -m venv venv
        . venv/bin/activate
        pip install pytest
        pytest test_example.py
        deactivate
    '''
                    
                }
            }
        }


        

        stage('Create Virtual Environment') {
            steps {
                script {
                    sh 'python -m venv venv'
                }
            }
        }

        stage('Activate Virtual Environment') {
            steps {
                script {
                    sh 'source venv/bin/activate'
                }
            }
        }

        stage('Install Requirements') {
            steps {
                script {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
            }
        }

        stage('Build and Test') {
            steps {
                script {
                    sh 'coverage run --source=. manage.py test'
                    sh 'coverage xml -o coverage.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv('SonarQube Server') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=myproject -Dsonar.projectName='My Project' -Dsonar.projectVersion=1.0 -Dsonar.sources=. -Dsonar.tests=. -Dsonar.language=python -Dsonar.sourceEncoding=UTF-8 -Dsonar.python.coverage.reportPaths=coverage.xml"
                    }
                }
            }
        }

        stage('Deactivate Virtual Environment') {
            steps {
                script {
                    sh 'deactivate'
                }
            }
        }




        

        stage('SonarQube Analysis-2') {
            steps  {
                script {
                    sh 'echo "Testing started.."'
                    
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                    sh 'echo "Testing ended."'
                }
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
