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

stage('Deploy') {
      steps {
        sh 'kubectl apply -f k8s/'
        sh 'kubectl -n taskflow set image deployment/taskflow taskflow=taskflow:$TAG'
        sh 'kubectl -n taskflow rollout status deployment/taskflow'
      }
    }
  }
} } }
  
