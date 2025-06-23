pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment {
        REGISTRY = 'tamvlb/stroke_pred_api'
        REGISTRY_CREDENTIAL = 'dockerhub'
        BUILD_NUMBER = 'latest'
    }

    stages {
        stage('Docker Test') {
            steps {
                sh 'docker --version'
                sh 'docker-compose --version'
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.9'
                }
            }
            environment {
                MLFLOW_TRACKING_URI = "http://host.docker.internal:5001"
            }
            steps {
                echo 'Testing FastAPI app...'
                sh '''
                    pip install --no-cache-dir -r service/model_api_serving/api_source/requirements.txt
                    pytest
                '''
            }
            
        }

        stage('Build') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${REGISTRY}:${BUILD_NUMBER}", "service/model_api_serving")
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    echo 'Pushing Docker image to Docker Hub...'
                    docker.withRegistry('', REGISTRY_CREDENTIAL)  {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                    ls -la ./src       # Optional: confirms file is there
                    chmod +x ./src/deploy.sh
                    ./src/deploy.sh
                    timeout 60s docker logs -f stroke_pred_api || true
                '''
            }
        }
    }
}
