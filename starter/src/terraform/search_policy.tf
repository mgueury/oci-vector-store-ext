variable no_policy { default=null }

resource "oci_identity_policy" "starter_search_policy" {
    count          = var.no_policy=="true" ? 0 : 1      
    provider       = oci.home    
    name           = "${var.prefix}-policy"
    description    = "${var.prefix} policy"
    compartment_id = local.lz_serv_cmp_ocid

    statements = [
        "allow any-user to manage object-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${oci_core_instance.starter_compute.id}'",
        "allow any-user to manage generative-ai-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${oci_core_instance.starter_compute.id}'",
        "allow any-user to manage stream-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${oci_core_instance.starter_compute.id}'",
        "allow any-user to manage genai-agent-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${oci_core_instance.starter_compute.id}'",
        "allow any-user to manage ai-service-language-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${oci_core_instance.starter_compute.id}'",
        "allow any-user to manage ai-service-speech-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${oci_core_instance.starter_compute.id}'",
        "allow any-user to manage generative-ai-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${data.oci_database_autonomous_database.starter_atp.autonomous_database_id}'",
        "allow any-user to manage genai-agent-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${data.oci_database_autonomous_database.starter_atp.autonomous_database_id}'",
        "allow any-user to manage object-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${data.oci_database_autonomous_database.starter_atp.autonomous_database_id}'",
        # OpenID
        "allow any-user to read secret-family in compartment id ${local.lz_app_cmp_ocid} where ALL {request.principal.type= 'ApiGateway'}",
        # Kubernetes
        "allow any-user to manage generative-ai-family in compartment id ${local.lz_serv_cmp_ocid} where ALL {request.principal.type='instance'}"

    ]
}

# "allow any-user to manage object-family in compartment id ${local.lz_serv_cmp_ocid} where request.principal.id='${data.oci_database_autonomous_database.starter_atp.autonomous_database_id}'",
# "allow any-user to manage object-family in compartment id ${local.lz_serv_cmp_ocid} where ALL { request.principal.id='${data.oci_database_autonomous_database.starter_atp.autonomous_database_id}', request.permission = 'PAR_MANAGE' }", */
# allow group xxxx-ai to use generative-ai-family in compartment id xxxxxx

