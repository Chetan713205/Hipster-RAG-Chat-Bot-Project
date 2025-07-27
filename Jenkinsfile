pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'gen-lang-client-0389229415'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
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
                    pip install  dvc
                    '''
                }
            }
        }

        stage('Build and Push Image to GCR'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo '..... Build and Push Image to GCR .....'
                        sh '''
                        set -e
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=\"${GOOGLE_APPLICATION_CREDENTIALS}\"
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -f Dockerfile \
                            --cache-from gcr.io/${GCP_PROJECT}/rag-project:latest \
                            -t gcr.io/${GCP_PROJECT}/rag-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/rag-project:latest
                        '''
                    }
                }
            }
        }

        stage('Deploying to Kubernetes'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' ),
                                 string(credentialsId: 'HUGGINGFACE_API_TOKEN', variable: 'HUGGINGFACE_API_TOKEN'),
                                 string(credentialsId: 'HF_TOKEN', variable: 'HF_TOKEN'),
                                 string(credentialsId: 'HUGGINGFACE_API_TOKEN', variable: 'HUGGINGFACEHUB_API_TOKEN'),
                                 string(credentialsId: 'HUGGINGFACE_REPO_ID', variable: 'HUGGINGFACE_REPO_ID'),
                                 string(credentialsId: 'PINECONE_API_KEY', variable: 'PINECONE_API_KEY'),
                                 string(credentialsId: 'PINECONE_INDEX_NAME', variable: 'PINECONE_INDEX_NAME'),
                                 string(credentialsId: 'GROQ_API_KEY', variable: 'GROQ_API_KEY')]){
                    script{
                        echo '..... Deploying to Kubernetes .....'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=\"${GOOGLE_APPLICATION_CREDENTIALS}\"
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials rag-app-cluster --region us-central1

                        kubectl create secret generic ml-app-secrets \
                        --from-literal=HUGGINGFACE_API_TOKEN="${HUGGINGFACE_API_TOKEN}" \
                        --from-literal=HF_TOKEN="${HF_TOKEN}" \
                        --from-literal=HUGGINGFACEHUB_API_TOKEN="${HUGGINGFACEHUB_API_TOKEN}" \
                        --from-literal=PINECONE_API_KEY="${PINECONE_API_KEY}" \
                        --from-literal=PINECONE_INDEX_NAME="${PINECONE_INDEX_NAME}" \ 
                        --from-literal=HUGGINGFACE_REPO_ID="${HUGGINGFACE_REPO_ID}" \
                        --from-literal=GROQ_API_KEY="${GROQ_API_KEY}" \
                        --dry-run=client -o yaml | kubectl apply -f -
                        
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}