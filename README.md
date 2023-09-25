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
    - [Generate SSH Keys in Jenkins Container](#generate-ssh-keys-in-jenkins-container)
    - [Copy Public Key to VM](#copy-public-key-to-vm)
    - [Test SSH Connection](#test-ssh-connection)
    - [Static IP Configuration on VM](#static-ip-configuration-on-vm)
    - [Sudoers File Error Fix](#sudoers-file-error-fix)
    - [Netplan File Example](#netplan-file-example)
  - [Jenkins credentials](#jenkins-credentials)
    - [Docker Hub Credentials](#docker-hub-credentials)
    - [SSH Credentials for VM](#ssh-credentials-for-vm)
  - [Deploying the App](#deploying-the-app)


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
        - Repository URL: (Add this repo URL; create credentials if the repo is private, but you dont need yet, this repo is public)
        - Branches to build: (Specify the branches)
        - Script Path: 'Jenkinsfile'
      - Save the job.

   <a name="credential-tutorials"></a>
   **Credential Tutorials:**
   - [Persoanl Access Token](https://youtu.be/AYohbnOqox0?si=LFLyRh7zO5yqRPr7) (enough for this project)
   - [SSH Keys](https://youtu.be/9-ij0cJLDz4?si=AJGXiLVGv5dkthC9) (if you want to build the project on every push and etc.)

 
## Create a VirtualBox with ubuntu 22.04 iso image

   I recommend to checkout both
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

### Generate SSH Keys in Jenkins Container

   1. Access the Jenkins container:
      ```bash
      docker exec -it <container_id> /bin/bash
      ```
   2. Generate SSH keys:
      ```bash
      ssh-keygen
      ```

   Note: The SSH key pair will be saved "/var/jenkins_home/.ssh/id_rsa" by default.

### Copy Public Key to VM

   1. Open the terminal on your VM
   2. Find the VM's IP address:
      ```bash
      ip a
      ```
   3. Find the username of the VM:
      ```bash
      whoami
      ```
   4. On the host machine access the Jenkins container:
      ```bash
      docker exec -it <container_id> /bin/bash
      ```
   5. Copy the SSH key to the VM:
      ```bash
      ssh-copy-id <vm_username>@<vm_ip_address>
      ```

### Test SSH Connection

   1. From host try to connect to the VM via SSH:
      ```bash
      ssh <vm_username>@<vm_ip_address>
      ```
   
### Static IP Configuration on VM

   1. Backup current configuration:
      ```bash
      sudo cp /etc/netplan/*.yaml /etc/netplan/backup.yaml
      ```
   2. Edit Netplan configuration:
      - The file is usually named "01-netcfg.yaml", "50-cloud-init.yaml", or something similar and is located in /etc/netplan/
      ```bash
      sudo nano /etc/netplan/50-cloud-init.yaml
      ```
   <a name="static-ip-configuration-on-vm-step-3"></a>
   3. Modify the file as shown [here](#netplan-file-example)
   4. Apply changes:
      ```bash
      sudo netplan apply
      ```
       
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

### Netplan File Example

Here's how to modify the Netplan configuration file:

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
   2. "addresses": Specifies the static IP address, I recommend to use the currently used, run: `ip a` and look for the interface with "state UP" (e.g., `enp0s3`, `eth0`, `wlp3s0`) and under it look for the "inet" part
   3. "routes" -> "via": Specifies the default route, check it with this command: `ip route | grep default`
   4. "nameservers" -> "addresses": Specifies the DNS servers (Google's DNS in this case)

   Go [back](#static-ip-configuration-on-vm-step-3) where you stopped :)
   

## Jenkins credentials

   You didn't have to create earlier because this repo is public but if you didn't whatch [these](#credential-tutorials) videos, I recommend to.

### Docker Hub Credentials

   1. **Purpose**: To upload the built image to Docker Hub
   2. **Steps**:
       - **Kind**: Username with Password
       - **Scope**: Global
       - **Username**: `your_docker_hub_username`
       - **Password**: `your_docker_hub_password`
       - **ID**: `whatever_you_want`
                 
### SSH Credentials for VM

   1. **Purpose**: To get access to the VM
   2. **Steps**:
       - **Kind**: SSH Username with private key
       - **Scope**: Global
       - **ID**: `whatever_you_want`
       - **Username**: `your_vm_username`
       - **Private Key**: check out the "Enter directly"
       - **Add**: Copy paste the Jenkins containers private key.
       - **Note**: To find the private key, enter the Jenkins container and navigate to `/var/jenkins_home/.ssh/id_rsa`.

> **Important**: Update the credential IDs and image name in the Jenkinsfile environment section.
  

## Deploying the App

   1. **Prerequisites**:
       - The VM is running
       - The Jenkins container is running

   2. **Deployment Steps**:
       1. Navigate to `localhost:8080` to access the Jenkins dashboard.
       2. Click on your project.
       3. On the left side, click "Build".
       4. If the build is successful, all stages will appear in green.
       5. The application will be accessible at `http://VM_ip_address:5000`.
