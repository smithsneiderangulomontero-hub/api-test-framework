pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -q -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    .venv/bin/ruff check .
                    .venv/bin/black --check .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
                    sleep 2
                    .venv/bin/pytest --html=reports/report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            sh 'pkill -f "uvicorn app.main:app" || true'
        }
    }
}
