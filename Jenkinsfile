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
                        def vmHost = '192.168.0.171'  // VM's static IP
                        def targetDir = '~/Dokumentumok/my_app'

                        // Add fingerprint to "known_hosts" to verify it
                        echo "Verify fingerprint"
                        sh "set -e; ssh-keyscan -H ${vmHost} >> ~/.ssh/known_hosts"

                        // SSH into the VM and create the directory (if it doesn't exist)
                        echo "Create directory"
                        sh '''
                        set -e;
                        ssh -i $SSH_KEY ''' + vmUser + '@' + vmHost + ''' << 'EOF'
                            mkdir -p ''' + targetDir + '''
                        EOF
                        '''

                        // Use SCP to copy the artifact to the VM
                        echo "copy the artifact"
                        sh 'set -e; scp -i $SSH_KEY my_app_latest.tar.gz ' + vmUser + '@' + vmHost + ':' + targetDir

                        // SSH into the VM and execute commands
                        echo "SSH into the VM and execute commands"
                        sh '''
                        set -e;
                        ssh -i $SSH_KEY ''' + vmUser + '@' + vmHost + ''' << 'ENDSSH'
                            cd ''' + targetDir + '''
                            
                            # Remove old unpacked files (useful if the nex archive contains fewer files or differente files)
                            find . -mindepth 1 -delete
                            
                            # Extract new archive
                            tar xzf my_app_latest.tar.gz
                            
                            if ! command -v pip3 &> /dev/null; then
                                sudo apt update
                                sudo apt install -y python3-pip
                            fi
                            if [ ! -d "myenv" ]; then
                                python3 -m venv myenv
                            fi
                            source myenv/bin/activate
                            pip3 install -r requirements.txt
                            # Kill the old app process if it exists
                            pkill -f 'python3 app.py' || true  
                            # Start the new app process
                            nohup python3 app.py &  
                        ENDSSH
                        '''
                    }
                }
            }
        }
    }
}
