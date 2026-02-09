pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                  python3 -m venv venv
                  . venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                  . venv/bin/activate
                  pytest --junit-xml=test-results.xml
                '''
            }
        }
    }

    post {
        always {
            echo 'Finished CI run'
        }
        success {
            echo 'Tests passed!'
        }
        failure {
            echo 'Some tests failed 😕'
        }
    }
}
