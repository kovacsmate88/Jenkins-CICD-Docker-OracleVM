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
                    echo "Image ${env.VERSION} pushed"
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
                    sh "ls -t my_app_*.tar.gz"
                }
                
            }
        }

        stage('Deploy to VM') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'SSH-into-VM', keyFileVariable: 'SSH_KEY')]) {
                        def vmUser = 'vboxuser'
                        def vmHost = '10.44.9.19'
                        def targetDir = '~/Dokumentumok'

                        // Add fingerprint to "known_hosts" to verify it
                        sh 'ssh-keyscan -H ' + vmHost + ' >> ~/.ssh/known_hosts'

                        // Check if the archive already exists on the VM
                        sh '''
                        ssh -i $SSH_KEY ''' + vmUser + '@' + vmHost + ''' << 'ENDSSH'
                            if [ ! -f "''' + targetDir + '''/my_app_latest.tar.gz" ]; then
                                exit 1
                            fi
                        ENDSSH
                        '''

                        // If the archive doesn't exist, copy it
                        if (currentBuild.resultIsBetterOrEqualTo('UNSTABLE')) {
                            sh 'scp -i $SSH_KEY my_app_latest.tar.gz ' + vmUser + '@' + vmHost + ':' + targetDir
                        }

                        // Use SCP to copy the artifact to the VM
                        sh 'scp -i $SSH_KEY my_app_latest.tar.gz ' + vmUser + '@' + vmHost + ':' + targetDir

                        // SSH into the VM and execute commands
                        sh '''
                        ssh -i $SSH_KEY ''' + vmUser + '@' + vmHost + ''' << 'ENDSSH'
                            cd ''' + targetDir + '''
                            tar xzf my_app_latest.tar.gz
                            if ! command -v pip3 &> /dev/null; then
                                sudo apt update
                                sudo apt install -y python3-pip
                            fi
                            if [ ! -d "myenv" ]; then
                                python3 -m venv myenv
                            fi
                            source myenv/bin/activate
                            pip install -r requirements.txt
                            pkill -f 'python app.py' || true
                            nohup python app.py &
                        ENDSSH
                        '''
                    }
                }
            }
        }

    }
}
