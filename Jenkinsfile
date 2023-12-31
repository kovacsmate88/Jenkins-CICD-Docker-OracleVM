pipeline {
    agent any 

    environment {

        DOCKER_CREDENTIAL_ID = 'Docker-Hub'
        IMAGE_NAME = 'mate8817/leroy-jenkins'
        VERSION = '${BUILD_NUMBER}'
        SSH_CREDENTIAL_ID = 'SSH-into-VM'
        
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
                    sh "tar czf my_app_${BUILD_NUMBER}.tar.gz ./app/app.py ./app/templates/ ./app/requirements.txt"
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
                    withCredentials([sshUserPrivateKey(credentialsId: "${SSH_CREDENTIAL_ID}", keyFileVariable: 'SSH_KEY')]) {
                        def vmUser = 'vboxuser'
                        def vmHost = '192.168.0.171'  // VM's static IP
                        def targetDir = '~/Dokumentumok/my_app'

                        // Add fingerprint to "known_hosts" to verify it
                        echo "Verify fingerprint"
                        sh "set -e; ssh-keyscan -H ${vmHost} >> ~/.ssh/known_hosts"

                        // Conditionally create or clean the directory
                        sh """
                            set -e;
                            if ssh -i $SSH_KEY ${vmUser}@${vmHost} "[ -d ${targetDir} ]"; then
                                ssh -i $SSH_KEY ${vmUser}@${vmHost} "cd ${targetDir}; rm -rf ./*"
                            else
                                ssh -i $SSH_KEY ${vmUser}@${vmHost} "mkdir -p ${targetDir}"
                            fi
                        """

                        // Use SCP to copy the artifact to the VM
                        echo "copy the artifact"
                        sh 'set -e; scp -i $SSH_KEY my_app_${BUILD_NUMBER}.tar.gz ' + vmUser + '@' + vmHost + ':' + targetDir

                        // SSH into the VM and execute commands
                        echo "SSH into the VM and deploy the application"
                        sh """
                            ssh -i $SSH_KEY ${vmUser}@${vmHost} '
                                cd ${targetDir};
                                
                                # Extract the archive
                                tar xzf my_app_${BUILD_NUMBER}.tar.gz;

                                # Install python3.10-venv if not already installed
                                if ! dpkg -l | grep python3.10-venv; then 
                                    sudo apt update; 
                                    sudo apt install -y python3.10-venv; 
                                fi;
                                
                                # Install pip3 if not already installed
                                if ! command -v pip3 &> /dev/null; then 
                                    sudo apt update; 
                                    sudo apt install -y python3-pip; 
                                fi;
                                
                                # Create virtual environment
                                python3 -m venv myenv;
                                
                                # Activate virtual environment and install requirements
                                source myenv/bin/activate;
                                pip3 install -r ./app/requirements.txt;
                                
                                # Kill the old app process if it exists
                                pkill -f 'python3 app.py' || true
                                
                                # Start the new app process
                                nohup python3 ./app/app.py > /dev/null 2>&1 & exit 0
                            '
                        """
                    }
                }
            }
        }
    }
}
