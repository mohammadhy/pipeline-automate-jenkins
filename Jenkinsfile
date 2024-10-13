pipeline {
    agent any
    environment {
      REGISTERY='192.168.1.104:5000'
      IMAGE= '${env.JOB_NAME}'
    }
    
    stages {
        stage('checkout') {
            steps {
              git branch: 'develop', credentialsID: '267895444wdw6494', url: '192.168.1.104:3000/python.git' '
                }
            }
        stage('Get Short SHA'){
          steps {
            script {
              env.CI_COMMIT_SHORT_SHA=sh(
                script:'git rev-parse --short HEAD',
                returnStdout: true).trim()
            }
          }
        }
        
    }
}