# Nourient Cloud Run deployment

This deployment intentionally packages the existing FastAPI services into one
Cloud Run container. Nginx exposes only browser-facing endpoints; services
continue to communicate through `127.0.0.1` inside the container.

## Required runtime configuration

Set these environment variables on the Cloud Run service:

```text
ENVIRONMENT=production
FIREBASE_PROJECT_ID=nourient-38381
BQ_DATA_PROJECT_ID=<existing BigQuery project id>
BQ_BILLING_PROJECT_ID=<new trial project id>
BQ_MAXIMUM_BYTES_BILLED=50000000
CORS_ALLOW_ORIGINS=https://app.example.com
GEMINI_API_KEY=<Secret Manager secret>
PINECONE_API_KEY=<Secret Manager secret>
```

`BQ_DATA_PROJECT_ID` continues to own the tables. Query jobs run in
`BQ_BILLING_PROJECT_ID`, so the new trial project is billed for eligible query
processing. The Cloud Run service account needs BigQuery Job User in the new
project and BigQuery Data Viewer on the existing dataset.

For Firestore/Firebase Admin, grant the Cloud Run service account
`roles/datastore.user` in the existing Firebase project. The application uses
Cloud Run Application Default Credentials and does not place a service-account
key in the image.

## Build

After authenticating `gcloud` to the new trial account and selecting its
project, run:

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_IMAGE=asia-south1-docker.pkg.dev/NEW_PROJECT_ID/nourient/nourient-api:latest
```

Then deploy that image to Cloud Run with 1 vCPU, 2 GiB memory, a 600-second
timeout, concurrency 1, minimum instances 0, and maximum instances 1.

Never place JSON keys or `.env` files in Git or the Docker image.
