
# -- Object Storage ---------------------------------------------------------

resource "oci_objectstorage_bucket" "starter_bucket" {
  compartment_id = local.lz_serv_cmp_ocid
  namespace      = local.local_object_storage_namespace
  name           = "${var.prefix}-upload-bucket"
  access_type    = "ObjectReadWithoutList"
  object_events_enabled = true

  freeform_tags = local.freeform_tags
}

resource "oci_objectstorage_bucket" "starter_agent_bucket" {
  compartment_id = local.lz_serv_cmp_ocid
  namespace      = local.local_object_storage_namespace
  name           = "${var.prefix}-converted-bucket"
  object_events_enabled = true

  freeform_tags = local.freeform_tags
}

locals {
  local_bucket_url = "https://objectstorage.${var.region}.oraclecloud.com/n/${local.local_object_storage_namespace}/b/${var.prefix}-upload-bucket/o/"
}  

