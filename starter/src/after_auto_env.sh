if grep -q 'STREAM_OCID' $TARGET_DIR/tf_env.sh; then
    echo "tf_env.sh already modified"
else 
    ## Set env variables needed for env.sh
    get_attribute_from_tfstate "STREAM_OCID" "starter_stream" "id"
    get_attribute_from_tfstate "TENANCY_NAME" "tenant_details" "name"
    get_attribute_from_tfstate "STREAM_MESSAGE_ENDPOINT" "starter_stream" "messages_endpoint"

    get_id_from_tfstate "APP_SUBNET_OCID" "starter_app_subnet" 
    get_id_from_tfstate "DB_SUBNET_OCID" "starter_db_subnet" 

    append_tf_env "# STREAMING CONNECTION"
    append_tf_env "export STREAM_MESSAGE_ENDPOINT=\"$STREAM_MESSAGE_ENDPOINT\""
    append_tf_env "export STREAM_OCID=\"$STREAM_OCID\""
    append_tf_env "export STREAM_USERNAME=\"$TENANCY_NAME/$TF_VAR_username/$STREAM_OCID\""
    append_tf_env
    append_tf_env "# GENERATIVE AI MODEL"
    oci generative-ai model-collection list-models --compartment-id $TF_VAR_compartment_ocid --all > $TARGET_DIR/genai_models.json 
    export TF_VAR_genai_meta_model=$(jq -r '.data.items[]|select(.vendor=="meta" and (.capabilities|index("CHAT")))|.["display-name"]' $TARGET_DIR/genai_models.json | head -n 1)
    append_tf_env "export TF_VAR_genai_meta_model=\"$TF_VAR_genai_meta_model\""

    export TF_VAR_genai_cohere_model=$(jq -r '.data.items[]|select(.vendor=="cohere" and (.capabilities|index("CHAT")))|.["display-name"]' $TARGET_DIR/genai_models.json | head -n 1)
    append_tf_env "export TF_VAR_genai_cohere_model=\"$TF_VAR_genai_cohere_model\""

    export TF_VAR_genai_embed_model="cohere.embed-multilingual-v3.0"
    # export TF_VAR_genai_embed_model=$(jq -r '.data.items[]|select(.vendor=="cohere" and (.capabilities|index("TEXT_EMBEDDINGS")) and ."time-on-demand-retired"==null)|.["display-name"]' $TARGET_DIR/genai_models.json | head -n 1)
    append_tf_env "export TF_VAR_genai_embed_model=\"$TF_VAR_genai_embed_model\""
    append_tf_env

    append_tf_env "export TF_VAR_rag_storage=\"$TF_VAR_rag_storage\""

    # LiveLabs
    if [ "$APIGW_HOSTNAME" = "" ]; then
       append_tf_env "# LiveLabs Green Button"    
       # Instance Principal Replacement
       append_tf_env "export LIVELABS=\"true\""
       get_attribute_from_tfstate "OCI_API_KEY_PEM" "tls_api_key" "private_key_pem"
       get_attribute_from_tfstate "FINGERPRINT" "oci_api_key" "fingerprint"
       append_tf_env "export OCI_API_KEY_PEM=\"$OCI_API_KEY_PEM\""
       append_tf_env "export FINGERPRINT=\"$FINGERPRINT\""
       append_tf_env "export TF_VAR_tenancy_ocid=\"$TF_VAR_tenancy_ocid\""
       append_tf_env "export TF_VAR_current_user_ocid=\"$TF_VAR_current_user_ocid\""
       get_attribute_from_tfstate "COMPUTE_PUBLIC_IP" "starter_compute" "public_ip"
       append_tf_env "export COMPUTE_PUBLIC_IP=\"$COMPUTE_PUBLIC_IP\""
       export BASE_URL="http://${COMPUTE_PUBLIC_IP}"
       export NLB_IP=$COMPUTE_PUBLIC_IP
       # Using the self sign certificate for the IP
       export ORDS_EXTERNAL_URL="https://${COMPUTE_PUBLIC_IP}/ords"

    else 
       export BASE_URL="https://${APIGW_HOSTNAME}/${TF_VAR_prefix}"
       export NLB_IP=`jq -r '.resources[] | select(.name=="starter_nlb") | .instances[0].attributes.ip_addresses[] | select(.is_public==true) | .ip_address' $STATE_FILE`
       echo "NLB_IP=$NLB_IP"
       export ORDS_EXTERNAL_URL=https://${APIGW_HOSTNAME}/ords
    fi 
    append_tf_env "export BASE_URL=\"$BASE_URL\""
    append_tf_env "export NLB_IP=\"$NLB_IP\""
    append_tf_env "export ORDS_EXTERNAL_URL=\"$ORDS_EXTERNAL_URL\""

    # Kubernetes
    if [ "$TF_VAR_deploy_type" == "kubernetes" ]; then
        append_tf_env "export LANGGRAPH_URL=\"http://langgraph-service:2024\""
        append_tf_env "export MCP_SERVER_URL=\"http://mcp-server-service:2025/mcp\""
    else 
        append_tf_env "export LANGGRAPH_URL=\"http://127.0.0.1:2024\""
        append_tf_env "export MCP_SERVER_URL=\"http://localhost:2025/mcp\""
    fi
    export LANGGRAPH_APIKEY="##TF_VAR_db_password##"

    # Vector Store
    if [ "$TF_VAR_rag_storage" == "vector_store" ]; then
        append_tf_env "export TF_VAR_responses_model_id=\"$TF_VAR_responses_model_id\""
        append_tf_env "export TF_VAR_project_ocid=\"$TF_VAR_project_ocid\""
    fi
fi
