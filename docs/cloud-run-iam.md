# Cloud Run IAM setup

## Workload Identity Federation (GitHub Actions)

Grant the GitHub Actions service account the following roles:

- `roles/run.admin` (deploy Cloud Run services)
- `roles/iam.serviceAccountUser` (impersonate runtime service account)
- `roles/cloudbuild.builds.editor` (Cloud Build submit)
- `roles/storage.admin` (push container images to GCR)
- `roles/aiplatform.user` (call Vertex AI Gemini)

The runtime Cloud Run service account should have:

- `roles/aiplatform.user` (call Vertex AI Gemini)
- `roles/storage.objectViewer` (read documents or indexes from GCS if needed)

If you store vector indexes or documents in GCS, ensure the runtime service account has
bucket-level access (at least `storage.objectViewer` for reads).
