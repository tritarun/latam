resource "google_storage_bucket" "test-storage-bucket" {
  name          = "watchful-pier-422221-q7_storage_bucket"
  location      = "US"
  force_destroy = true
  project = "Active project"

  public_access_prevention = "enforced"
}