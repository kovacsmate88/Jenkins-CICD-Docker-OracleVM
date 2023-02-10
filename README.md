# Leeeeeeeroy Jenkins

## Story

So far you have been building everything manually. You also heard about CI/CD tools which build the things you need instead of you! Not wanting to do work has never paid off so well!

## What are you going to learn?

- How to use Jenkins
- How to create a freestyle project in Jenkins
- How to build an application in Jenkins
- How to deploy an artifact in Jenkins

## Tasks

1. Install Jenkins locally in your computer, use the Jenkins docker image
    - Docker is installed.
    - You can see the Jenkins dashboard on ```localhost:8080```.

2. Build an image with Jenkins from one of your already existing Dockerfiles, and push it to ECR.
    - The image is pushed to your ECR.

3. Build one of your already existing web application with Jenkins, and save the artifact.
    - Your artifact is successfully built.

4. Deploy the artifact of your app with Jenkins to a virtual machine (use VirtualBox for this task).
    - Your application is running inside a virtual machine.

## General requirements

None

## Hints

- To get the password for the Jenkins installation, use the ```docker logs``` command.

## Background materials

- <i class="far fa-exclamation"></i> [Jenkins installation in Docker](https://www.jenkins.io/doc/book/installing/docker/)
- <i class="far fa-exclamation"></i> [Jenkins installation troubleshooting](https://docs.google.com/document/d/1g15mOqGiMcdQhvkEg-75_WkE-m5NJA-__uk0gIA3WUE/edit)
- <i class="far fa-video"></i> [Jenkins installation in Docker](https://www.youtube.com/watch?v=UQMAKQPxnHs&ab_channel=TravelsCode)
