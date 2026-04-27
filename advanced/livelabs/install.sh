#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

cd ../../starter

cp -r ../advanced/livelabs/* .
rm install.sh
mv src/terraform/apigw.tf src/terraform/apigw._tf 
mv src/terraform/genai_apigw.tf src/terraform/genai_apigw._tf 
mv src/terraform/genai_streamlit.tf src/terraform/genai_streamlit._tf 

sed -i 's/oci_apigateway_/# oci_apigateway_/' src/terraform/build.tf 
sed -i 's/assign_public_ip.*= false/assign_public_ip = true/' src/terraform/compute.tf 
