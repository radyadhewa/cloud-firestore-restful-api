GOOGLE_PROJECT_ID=fir-login-24502

# Build and submit the container image to Container Registry
gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/restfulapi \
  --project=$GOOGLE_PROJECT_ID

# Deploy the container image to Cloud Run
gcloud run deploy restful-api \
  --image gcr.io/$GOOGLE_PROJECT_ID/restfulapi \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --project=$GOOGLE_PROJECT_ID
