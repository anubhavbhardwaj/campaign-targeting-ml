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