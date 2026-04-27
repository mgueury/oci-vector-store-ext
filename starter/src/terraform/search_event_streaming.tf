resource "oci_events_rule" "starter_rule" {
  actions {
    actions {
      action_type = "OSS"
      is_enabled = "true"
      stream_id  = oci_streaming_stream.starter_stream.id
    }
  }
  compartment_id = local.lz_serv_cmp_ocid
  condition      = "{\"eventType\":[\"com.oraclecloud.objectstorage.createobject\",\"com.oraclecloud.objectstorage.deleteobject\",\"com.oraclecloud.objectstorage.updateobject\"],\"data\":{\"additionalDetails\":{\"bucketName\":[\"${var.prefix}-upload-bucket\"]}}}"
  display_name = "${var.prefix}-input-rule"
  is_enabled = "true"
}

data "oci_events_rules" "starter_stream_rules" {
  #Required
  compartment_id = local.lz_serv_cmp_ocid

  #Optional
  display_name = "${var.prefix} Rule"
  state        = "ACTIVE"
}

resource "oci_streaming_stream_pool" "starter_stream_pool" {
  #Required
  compartment_id = local.lz_serv_cmp_ocid
  name           = "${var.prefix}-streampool"
}

resource "oci_streaming_stream" "starter_stream" {
  name               = "${var.prefix}-stream"
  partitions         = "1"
  retention_in_hours = "24"
  stream_pool_id     = oci_streaming_stream_pool.starter_stream_pool.id
}

