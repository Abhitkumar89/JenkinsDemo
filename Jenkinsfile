pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                echo Checking Python version
                python --version

                echo Creating virtual environment
                python -m venv venv

                echo Installing dependencies
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                echo Running pytest
                venv\\Scripts\\python -m pytest -v
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI Pipeline succeeded: All tests passed'
        }
        failure {
            echo '❌ CI Pipeline failed: Tests or setup error'
        }
        always {
            echo '📌 CI run finished'
        }
    }
}
