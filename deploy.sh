#!/bin/bash
read -p 'Project: ' PROJECT_ID
gcloud config set project $PROJECT_ID
echo "building image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/masquerade
echo "deploying image..."
gcloud run deploy masquerade --image gcr.io/$PROJECT_ID/masquerade --platform managed --region us-central1 --port 8000
