# Leeeeeeeroy Jenkins


## What are you going to learn?

- How to use Jenkins
- How to create a freestyle project in Jenkins
- How to build an application in Jenkins
- How to deploy an artifact in Jenkins

## Tasks

1. Install Jenkins locally in your computer, use the Jenkins docker image
    - run: docker-compose up --build -d (detached mode)
    - to get the jenkins password run: ```docker exec container_id cat /var/jenkins_home/secrets/initialAdminPassword```
    - go to Jenkins dashboard: ```localhost:8080```
    - create an admin user
    - click new item to create a job
    - choose pipeline 
    - go to pipeline section
    - definition: Pipeline script from SCM
    - SMC: Git
    - add repo url (if the repo is private you have to create credentials)
    - watch the 2 best credential tutorial videos: 
      - https://youtu.be/AYohbnOqox0?si=LFLyRh7zO5yqRPr7
      - https://youtu.be/9-ij0cJLDz4?si=AJGXiLVGv5dkthC9
    - set up the branches which one u want to build 
    - leave scripth path : Jenkinsfile
    - hit: Save

2. Build an image with Jenkins from one of your already existing Dockerfiles, and push it to ECR.
    - The image is pushed to your ECR.

3. Build one of your already existing web application with Jenkins, and save the artifact.
    - Your artifact is successfully built.

4. Deploy the artifact of your app with Jenkins to a virtual machine (use VirtualBox for this task).
   
  1. create a VirtualBox with ubuntu 22.04 iso image based on these 2 tutorial: 
   - https://youtu.be/nvdnQX9UkMY?si=4ZYKGq5R6lCtqlqZ
   - https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview
   
  2. SSH Setup:
      1. Set up VM to ssh connection:
         1. Open the VM Virtual Box Manager
         2. Select your ubuntu 22.04 virtual machine
         3. Top Middle select settings -> General -> Advanced -> Shared clipboard -> Bidirectional go back to Settings -> Network -> Attached to: Briged Adapter -> Name: to check which network interface is active on the host, run: ```ip a``` and at the end of the lines which are staretd like this: 1. lo: or 2: enp0s25 or 3: wlp3s0: look after "state UP" and in my case the "wlps30" is in UP state
            1. With these settings you can copy-paste from host to virtual box and vice versa
         4. Install SSH Server on VirtualBox VM:
            1. Open the terminal
            2. run: ```sudo apt update && sudo apt upgrade -y```
               - if you get this error after you typed the password: vboxuser is not in the sudoers file.  This incident will be reported.
                 1. run ```su -``` to switch to the superuser (root) account
                 2. run: ```visudo```
                 3. under this: ```%sudo   ALL=(ALL:ALL) ALL``` add this: ```your_ubuntu_user ALL=(ALL:ALL) ALL``` 
                 4. save the file
                 5. run ```exit``` to exit the superuser
                 6. run again: ```sudo apt update && sudo apt upgrade -y```
            3. run: ```sudo snap refresh```
            4. now download the ssh server: ```sudo apt install openssh-server```
            5. start ssh server: ```sudo systemctl start ssh```
            6. check ssh server: ```sudo systemctl status ssh```
            7. allow ssh traffic on the VM: ```sudo ufw allow ssh```
         5. Get VM's IP Address and Username
            1. run ```ip a``` to find out its IP address. Look for the "inet" address under the network interface you're using (often eth0 or enp0s3)
            2. run ```whoami``` to display the current username
         6. Access Jenkins Container Terminal
            1. Use ```docker exec -it container_id /bin/bash``` to get a shell in the Jenkins container
         7. Generate SSH Keys in Jenkins Container
            1. run ```ssh-keygen``` to generate a new SSH key pair, which will be saved "/var/jenkins_home/.ssh/id_rsa" by default
            2. check the keys with ```ls /root/.ssh/```
         8. Copy Public Key to VM
            1. In the Jenkins container terminal, run ```ssh-copy-id vm_username@vm_ip_address```
            2. Enter the VM user's password
         9. Test SSH Connection
            1.  In the Jenkins container terminal, run ```ssh vm_username@vm_ip_address```
            2.  You are in without needing to enter a password
        1.  Exit SSH Session
            1. type exit
            2. VM is set up to SSH connection
   
   
   3. Jenkins Configuration:
      1. Install Plugins: Make sure the SSH plugin is installed in Jenkins.
      2. Add SSH Credentials:
        - Go to "Manage Jenkins" -> "Manage Credentials" -> "(global)" -> "Add Credentials".
        - Choose "SSH Username with private key" and fill in the details.
  
   4. Deploy the app
      1. on host run: ```export HOST_IP=$(hostname -I | awk '{print $1}')```
      2. 



## Background materials

- <i class="far fa-exclamation"></i> [Jenkins installation in Docker](https://www.jenkins.io/doc/book/installing/docker/)
- <i class="far fa-exclamation"></i> [Jenkins installation troubleshooting](https://docs.google.com/document/d/1g15mOqGiMcdQhvkEg-75_WkE-m5NJA-__uk0gIA3WUE/edit)
- <i class="far fa-video"></i> [Jenkins installation in Docker](https://www.youtube.com/watch?v=UQMAKQPxnHs&ab_channel=TravelsCode)
