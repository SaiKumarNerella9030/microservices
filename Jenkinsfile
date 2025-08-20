pipeline {
    agent any

    environment {
        DOCKER_HUB_ID = "saikumarnerella90"
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // Repo already checked out by Jenkins SCM
                    GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    IMAGE_TAG = "${GIT_COMMIT_SHORT}"
                    echo "Using image tag: ${IMAGE_TAG}"
                }
            }
        }

        stage('Build & Push Docker Images') {
            steps {
                script {
                    docker.withRegistry("https://index.docker.io/v1/", "dockerhub-creds") {
                        sh """
                        # Auth service
                        docker build -t ${DOCKER_HUB_ID}/auth:${IMAGE_TAG} ./auth
                        docker push ${DOCKER_HUB_ID}/auth:${IMAGE_TAG}
                        docker tag ${DOCKER_HUB_ID}/auth:${IMAGE_TAG} ${DOCKER_HUB_ID}/auth:latest
                        docker push ${DOCKER_HUB_ID}/auth:latest

                        # User service
                        docker build -t ${DOCKER_HUB_ID}/user:${IMAGE_TAG} ./user
                        docker push ${DOCKER_HUB_ID}/user:${IMAGE_TAG}
                        docker tag ${DOCKER_HUB_ID}/user:${IMAGE_TAG} ${DOCKER_HUB_ID}/user:latest
                        docker push ${DOCKER_HUB_ID}/user:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl set image deployment/auth-deployment auth=saikumarnerella90/auth:${IMAGE_TAG} --record
                        kubectl set image deployment/user-deployment user=saikumarnerella90/user:${IMAGE_TAG} --record
                        kubectl rollout status deployment/auth-deployment
                        kubectl rollout status deployment/user-deployment
                    '''
                }
            }
        }
    }
}
