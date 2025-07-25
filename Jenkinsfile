pipeline {
    agent any

    stages{
        stage('Cloning GitHub repo to Jenkins') {
            steps{
                script{
                    echo '..... Cloning from the GitHub .....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Chetan713205/Hipster-RAG-Chat-Bot-Project.git']])
                }
            }
        }
    }
}