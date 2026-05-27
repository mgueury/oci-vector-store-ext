#!/usr/bin/env bash
title "Before Config"
if [ "$TF_VAR_rag_storage" == "db26ai" ]; then
  # Use the KB of 26ai 
  if [ -f src/terraform/genai_kb_26ai._tf ]; then
    echo "before_config.sh: RAG Storage db26ai"
    mv src/terraform/genai_kb_26ai._tf src/terraform/genai_kb_26ai.tf
    mv src/terraform/genai_kb_os.tf src/terraform/genai_kb_os._tf
  fi
fi

if [ "$TF_VAR_kubernetes" == "true" ]; then
  echo "before_config.sh: Kubernetes"
  cp -R ../advanced/kubernetes/src/* src/. 
  sed -i '/local_oke_ocid = ""/d' src/terraform/build.tf 
  sed -i 's/"TF_VAR_deploy_type" "private_compute"/"TF_VAR_deploy_type" "kubernetes"/' src/terraform/build.tf 
fi

if [ "$TF_VAR_openid" == "true" ]; then
  echo "before_config.sh: OpenID"
  cp -R ../advanced/openid/src/* src/. 
fi

# LiveLabs
if [ "$LIVELABS" == "true" ]; then
  if ! grep -q 'vcn_id=' $PROJECT_DIR/terraform.tfvars; then
    echo "before_config.sh: LiveLabs"
    cp -R ../advanced/livelabs/* . 
    # No Policy not APIGW for LiveLabs
    mv src/terraform/search_policy.tf src/terraform/search_policy._tf
    mv src/terraform/apigw.tf src/terraform/apigw._tf
    mv src/terraform/genai_apigw.tf src/terraform/genai_apigw._tf
    sed -i '/oci_apigateway_gateway.starter_apigw/d' src/terraform/build.tf 
  fi
fi