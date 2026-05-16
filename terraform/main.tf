terraform{
    required_providers{
        google = {
            source = "hashicorp/google"
            version = "~> 5.0"
        }
    }
    backend "gcs" {
    bucket = "anubhaviiitb-terraform-state"
    prefix = "campaign_targeting"
    }

}

provider "google" {
    project = var.project_id
    region = var.region
}

resource "google_bigquery_dataset" "campaign_targeting_tf"{
    dataset_id = "campaign_targeting_tf"
    location = var.region
    description = "Campaign targeting features, managed by terraform"
}

# Service account for Cloud Run
resource "google_service_account" "cloud_run_api" {
  account_id   = "cloud-run-campaign-targeting"
  display_name = "Cloud Run API SA"
  project      = var.project_id
}

resource "google_project_iam_binding" "cloud_run_bq_viewer" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  members = [
    "serviceAccount:${google_service_account.cloud_run_api.email}"
  ]
}

resource "google_project_iam_binding" "cloud_run_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  members = [
    "serviceAccount:${google_service_account.cloud_run_api.email}"
  ]
}