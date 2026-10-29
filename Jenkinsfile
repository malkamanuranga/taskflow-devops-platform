pipeline {
  agent any
  environment { TAG = "${env.BUILD_NUMBER}" }

  stages {
    stage('Test') {
      steps { sh 'docker build --target test -t taskflow-test:$TAG app' }
    }


  
