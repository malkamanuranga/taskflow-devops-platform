pipeline {
  agent any
  environment { TAG = "${env.BUILD_NUMBER}" }

  stages {
    stage('Test') {
      steps { sh 'docker build --target test -t taskflow-test:$TAG app' }
    }
   stage('Load into kind') {
      steps { sh 'kind load docker-image taskflow:$TAG --name devops' }
    }


  
