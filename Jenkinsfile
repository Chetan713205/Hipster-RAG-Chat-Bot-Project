pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }
    
    stages{
        stage('Cloning GitHub repo to Jenkins') {
            steps{
                script{
                    echo '..... Cloning from the GitHub .....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Chetan713205/Hipster-RAG-Chat-Bot-Project.git']])
                }
            }
        }
                stage('Making a virtual environment') {
            steps{
                script{
                    echo '..... Making a virtual environment .....'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install  dvc
                    '''
                }
            }
        }
    }
}