pipeline {
    agent any 

    environment {
        // Define any environment variables here

        // Create a Jenkins credential with DockerHub username and password
        DOCKER_CREDENTIAL_ID = 'Docker-Hub'
        IMAGE_NAME = 'mate8817/leroy-jenkins'
        VERSION = '${BUILD_NUMBER}'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Get the code from the version control system.
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${IMAGE_NAME}:${VERSION} -f ./dockerfiles/Dockerfile-app ."
                    echo "Image built"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log into Docker Hub
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIAL_ID}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                    }
                    echo "Logged in"
                    
                    // Push the image
                    sh "docker push ${IMAGE_NAME}:${VERSION}"
                    echo "Image ${VERSION} pushed"
                }
            }
        }

        stage('Cleanup image') {
            steps {
                script{
                    // Remove the Docker image from the Jenkins agent for storage management
                    sh "docker rmi ${IMAGE_NAME}:${VERSION}"
                    echo "Image has removed"
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                script{
                    // Build and archive the artifact
                    sh "tar czf my_app_${BUILD_NUMBER}.tar.gz ./app/app.py ./app/requirements.txt"
                    archiveArtifacts artifacts: "my_app_${env.BUILD_NUMBER}.tar.gz", allowEmptyArchive: true
                }
            }
        }

        stage('Cleanup Older Artifacts') {
            steps {
                script{
                    // Remove all artifacts except the latest one for storage management
                    sh "ls -t my_app_*.tar.gz | tail -n +2 | xargs rm -f"
                }
                
            }
        }
    }
}
