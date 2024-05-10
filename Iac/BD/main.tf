# # See versions at https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance#database_version
# resource "google_sql_database_instance" "latam-instance" {
#   name             = "latam-instance"
#   region           = "us-central1"
#   database_version = "MYSQL_8_0"
#   settings {
#     tier = "db-f1-micro"
#     ip_configuration {
#       authorized_networks {
#         name            = "Open-Internet"
#         value           = "0.0.0.0/0"
#       }
#     }
#   }
#   # set `deletion_protection` to true, will ensure that one cannot accidentally delete this instance by
#   # use of Terraform whereas `deletion_protection_enabled` flag protects this instance at the GCP level.
#   deletion_protection = false
# }


# resource "google_sql_database" "latam-database" {
#   name     = "latam-database"
#   instance = google_sql_database_instance.instance_latam.name
# }

# resource "google_sql_user" "users" {
#   name     = "root"
#   instance = google_sql_database_instance.instance_latam.name
#   password = "latamadmin1234$"
# }
