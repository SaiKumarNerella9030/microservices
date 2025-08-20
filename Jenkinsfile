pipeline {
    agent any

    environment {
        REGISTRY = "saikumarnerella90"
        IMAGE_TAG = "${env.BUILD_NUMBER}"   // Version-wise tag
        KUBECONFIG_PATH = "${WORKSPACE}/kubeconfig"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'Gitcreds', url: 'https://github.com/SaiKumarNerella9030/microservices.git', branch: 'main'
            }
        }

        stage('Build & Push Docker Images') {
            steps {
                script {
                    def services = ["auth", "user"]
                    docker.withRegistry('https://index.docker.io/v1/', 'Dockercreds') {
                        services.each { service ->
                            sh """
                                docker build -t ${REGISTRY}/${service}:${IMAGE_TAG} ./services/${service}
                                docker push ${REGISTRY}/${service}:${IMAGE_TAG}
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                script {
                        def services = ["auth", "user"]
                            services.each { service ->
                        sh """
                        echo \"Deploying ${service}\"
                        sed -i 's|image: ${REGISTRY}/${service}:.*|image: ${REGISTRY}/${service}:${IMAGE_TAG}|' k8s-manifests/${service}-deployment.yaml
                        kubectl --kubeconfig=$KUBECONFIG apply -f k8s-manifests/${service}-deployment.yaml
                        kubectl --kubeconfig=$KUBECONFIG rollout status deployment/${service}-deployment
                        """
                        }
                    }
                }
            }
        }
    }
}
