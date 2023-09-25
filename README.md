# Deploy an Artifact with Jenkins on OracleVM

This project demonstrates how to set up a CI/CD pipeline using Jenkins running in a Docker container. The pipeline builds a Docker image from a Dockerfile, pushes it to DockerHub, and then deploys a web application artifact to a Virtual Machine (VM) running on Oracle VirtualBox.


## Table of Contents

- [Deploy an Artifact with Jenkins on OracleVM](#deploy-an-artifact-with-jenkins-on-oraclevm)
  - [Table of Contents](#table-of-contents)
  - [Set up Jenkins and create a job](#set-up-jenkins-and-create-a-job)
  - [Create a VirtualBox with ubuntu 22.04 iso image](#create-a-virtualbox-with-ubuntu-2204-iso-image)
  - [SSH Setup](#ssh-setup)
    - [VirtualBox Manager Configuration](#virtualbox-manager-configuration)
    - [SSH Server Installation on VM](#ssh-server-installation-on-vm)
    - [Sudoers File Error Fix](#sudoers-file-error-fix)
  - [Create further Jenkins credentials](#create-further-jenkins-credentials)
  - [Deploy the app](#deploy-the-app)


## Set up Jenkins and create a job

   1. Run Jenkins in detached mode:
      ```bash
      docker-compose up --build -d
      ```
   2. Retrieve the Jenkins admin password:
      ```bash
      docker exec <container_id> cat /var/jenkins_home/secrets/initialAdminPassword
      ```
    
   3. Access the Jenkins dashboard at 'localhost:8080'
   4. Create an admin user.
   5. Create a new pipeline job:
      - Click on "New Item"
      - Enter a name for the job
      - Select "Pipeline"
      - In the "Pipeline" section:
        - Definition: "Pipeline script from SCM"
        - SCM: Git
        - Repository URL: (Add your repo URL; create credentials if the repo is private)
        - Branches to build: (Specify the branches)
        - Script Path: 'Jenkinsfile'
      - Save the job.

   **Credential Tutorials:**
   - [Persoanl Access Token](https://youtu.be/AYohbnOqox0?si=LFLyRh7zO5yqRPr7) (enough for this project)
   - [SSH Keys](https://youtu.be/9-ij0cJLDz4?si=AJGXiLVGv5dkthC9) (if you want to build on every push and etc.)
   
## Create a VirtualBox with ubuntu 22.04 iso image

   - [Video](https://youtu.be/nvdnQX9UkMY?si=4ZYKGq5R6lCtqlqZ)
   - [Official Step-by-step](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview)

## SSH Setup
      
### VirtualBox Manager Configuration

  1. **Open VirtualBox Manager** and select your Ubuntu 22.04 virtual machine
  2. **Navigate to Settings**:
      - **General** -> **Advanced** -> Set **Shared Clipboard** to **Bidirectional**
      - **Network** -> Set **Attached to** to **Bridged Adapter** and you can choose the **Name** based on the **Note**

  **Note**: To find the active network interface on your host machine, run `ip a` and look for the interface with "state UP" (e.g., `enp0s3`, `eth0`, `wlp3s0`).

### SSH Server Installation on VM

   1. Open the terminal on your VM.
   <a name="ssh-server-installation-step-2"></a>
   2. Update and upgrade packages:
      ```bash
      sudo apt update && sudo apt upgrade -y
      ```
      - If you encounter a sudoers file error, follow these [steps](#sudoers-file-error-fix).
   3. Refresh snap packages:
      ```bash
      sudo snap refresh
      ```
   4. Install SSH server:
      ```bash
      sudo apt install openssh-server
      ```
   5. Start the SSH server:
      ```bash
      sudo systemctl start ssh
      ```
   6. Check SSH server status:
      ```bash
      sudo systemctl status ssh
      ```
   7. Allow SSH traffic:
      ```bash
      sudo ufw allow ssh
      ```


           4. save the file
           5. run ```exit``` to exit the superuser
           6. run again: ```sudo apt update && sudo apt upgrade -y```
      
   3. Generate SSH Keys in Jenkins Container
      1. 1. Use ```docker exec -it container_id /bin/bash``` to get a shell in the Jenkins container
      2. run ```ssh-keygen``` to generate a new SSH key pair, which will be saved "/var/jenkins_home/.ssh/id_rsa" by default
         
   4. Copy Public Key to VM
      1. In the Jenkins container terminal, run ```ssh-copy-id vm_username@vm_ip_address```
      2. run ```ip a``` to find out its IP address. Look for the "inet" address under the network interface you're using (often eth0 or enp0s3)
      3. run ```whoami``` to display the current username
     
   5.  Test SSH Connection
      1.  In the Jenkins container terminal, run ```ssh vm_username@vm_ip_address```
      2.  You are in without needing to enter a password
     
   6.  On VM set up a static IP:
       1. Backup Current Configuration: ```sudo cp /etc/netplan/*.yaml /etc/netplan/backup.yaml```
       2. Edit Netplan configuration: Open the Netplan configuration file in a text editor. The file is usually named "01-netcfg.yaml", "50-cloud-init.yaml", or something similar and is located in /etc/netplan/. ```sudo nano /etc/netplan/50-cloud-init.yaml```
       3. Modify the File:
            ```
               network:
                  version: 2
                  renderer: NetworkManager
                  ethernets:
                     enp0s3:
                        dhcp4: no
                        addresses: [192.168.0.171/24]
                        routes:
                        - to: 0.0.0.0/0
                          via: 192.168.0.1
                        nameservers:
                           addresses: [8.8.8.8, 8.8.4.4]

            ```
            1. "dhcp4": no (Dynamic Host Configuration Protocol), because you're setting a static IP instead
            2. "addresses": specifies the static IP address you want to use, I recommend to use the currently used, run: ```ip a``` and look after the "state UP" at the end of the lines which are something like "enp0s3" or "eth0" and under the "state UP" network look for the "inet" part
            3. "routes" -> "via": specifies the default route, check it with this command: ```ip route | grep default```
            4. "nameservers": specifies the DNS servers to use (in this case  Google's DNS servers)
       4. Apply Changes
          1. run: ```sudo netplan apply```

---

### Sudoers File Error Fix

If you encounter an error related to the sudoers file, follow these steps:

  1. Switch to the superuser account:
      ```bash
      su -
      ```
   2. Open the sudoers file:
      ```bash
      visudo
      ```
   3. Add your user to the end of the sudoers file:
      ```text
      your_vm_user ALL=(ALL:ALL) NOPASSWD: ALL
      ```
   4. Save the file and exit the superuser mode:
      ```bash
      exit
      ```
   
   Go [back](#ssh-server-installation-step-2) where you stopped :)
   

              

## Create further Jenkins credentials

   1. Docker Hub credential (to upload the built image to Docker Hub):
      - Kind: Username with Password
      - Scope: Global
      - Username: your_docker_hub_username
      - Password: your_docker_hub_password
      - ID: whatever_you_want
              

   2. SSH credential (to get access to the VM):
      - Kind: SSH Username with private key
      - Scope: Global
      - ID: whatever_you_want
      - Username: your_vm_username
      - Private Key -> Enter directly: enter into the Jenkins container and you can check the private key at "/var/jenkins_home/.ssh/id_rsa"

   Note: Update the credential IDs and image name in the Jenkinsfile environment section.
  

## Deploy the app

   1. Go to localhost:8080 to reach the Jenkins dashboard
   2. Click on your project
   3. On the left side click build
   4. If the build was successfully all the stages will be green 
   5. You can reach the application on the http://VM_ip_address:5000
   6. On the VM you can check if the app is running with this command: ```ps aux | grep 'app.py'```

