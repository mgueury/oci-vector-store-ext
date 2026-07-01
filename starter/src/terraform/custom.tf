resource "null_resource" "custom_dependency" {
    provisioner "local-exec" {
        command = <<-EOT
        cd ${local.project_dir}
        ENV_FILE=target/tf_env.sh
        append() {
            echo "$1" >> $ENV_FILE
        }    
        append_export() {
            if [ "$2" != "" ] && [ "$2" != "-" ]; then
                echo "export $1=\"$2\"" >> $ENV_FILE
            fi 
        }
        append "# OpenID"
        append_export "TF_VAR_openid_client_id" "${local.openid_client_id}"
        append_export "TF_VAR_openid_client_secret" "${local.openid_client_secret}"
        EOT
    }
    depends_on = [ null_resource.tf_env, oci_streaming_stream_pool.starter_stream_pool, oci_identity_policy.starter_search_policy ]

    triggers = {
        always_run = "${timestamp()}"
    }   
}
