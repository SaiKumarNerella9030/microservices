pipeline {
    agent any

    environment {
        DOCKER_HUB = "your-dockerhub"        // change this
        KUBECONFIG = credentials('kubeconfig-cred')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-org/microservices-project.git'
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    def services = ["auth", "user"]
                    services.each { svc ->
                        sh """
                        docker build -t $DOCKER_HUB/${svc}:$BUILD_NUMBER ./services/${svc}
                        docker push $DOCKER_HUB/${svc}:$BUILD_NUMBER
                        """
                    }
                }
            }
        }

        stage('Deploy with kubectl') {
            steps {
                sh """
                kubectl apply -f k8s-manifests/auth-deployment.yaml
                kubectl apply -f k8s-manifests/user-deployment.yaml
                """
            }
        }

        stage('Verify') {
            steps {
                sh "kubectl get pods -o wide"
                sh "kubectl get svc -o wide"
            }
        }
    }
}

