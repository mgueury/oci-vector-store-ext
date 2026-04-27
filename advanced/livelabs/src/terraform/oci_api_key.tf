# OCI API Key to create .oci/config + oci_api_key.pem to use instead of InstancePrincipal
variable current_user_ocid {}

resource "tls_private_key" "tls_api_key" {
  algorithm   = "RSA"
  rsa_bits = "2048"
}

resource "oci_identity_api_key" "oci_api_key" {
    provider = oci.home
    #Required
    key_value = trimspace(tls_private_key.tls_api_key.public_key_pem)
    user_id = var.current_user_ocid
}
