#!/bin/bash

cd "$(dirname "$0")/.."
while true; do
  STATUS=$(gcloud builds list --project=nourient-508220 --limit=1 --format="value(status)")
  echo "Status: $STATUS"
  if [ "$STATUS" = "SUCCESS" ]; then
    echo "Build succeeded! Deploying to Cloud Run..."
    gcloud run deploy nourient-backend \
      --image asia-south1-docker.pkg.dev/nourient-508220/nourient/nourient-api:latest \
      --region asia-southeast1 \
      --platform managed \
      --allow-unauthenticated \
      --cpu 4 --memory 8Gi --timeout 600 \
      --set-env-vars ENVIRONMENT=production,FIREBASE_PROJECT_ID=nourient-38381,CORS_ALLOW_ORIGINS=https://nourient.renalka.dev,BQ_DATA_PROJECT_ID=nourient,BQ_BILLING_PROJECT_ID=nourient-508220,BQ_MAXIMUM_BYTES_BILLED=50000000 \
      --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,PINECONE_API_KEY=PINECONE_API_KEY:latest" \
      --project=nourient-508220
    echo "Deployment script finished."
    gcloud beta run domain-mappings create --service=nourient-backend --domain=api.nourient.renalka.dev --region=asia-southeast1 --project=nourient-508220
    exit 0
  elif [ "$STATUS" = "FAILURE" ] || [ "$STATUS" = "TIMEOUT" ] || [ "$STATUS" = "INTERNAL_ERROR" ] || [ "$STATUS" = "CANCELLED" ]; then
    echo "Build failed with status $STATUS"
    exit 1
  fi
  sleep 30
done
