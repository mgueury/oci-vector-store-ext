#!/usr/bin/env bash
export SRC_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export ROOT_DIR=${SRC_DIR%/*}
cd $ROOT_DIR

. ./starter.sh env

# Upload Sample Files
sleep 5
echo "https://${APIGW_HOSTNAME}/${TF_VAR_prefix}/index.html" > ../sample_files/website.crawler
oci os object bulk-upload -ns $OBJECT_STORAGE_NAMESPACE -bn ${TF_VAR_prefix}-upload-bucket --src-dir ../sample_files --overwrite --content-type auto

title "INSTALLATION DONE"
echo
# echo "(experimental) Cohere with Tools and GenAI Agent:"
# echo "http://${BASTION_IP}:8081/"
# echo "-----------------------------------------------------------------------"

echo "URLs" > $FILE_DONE
append_done "-----------------------------------------------------------------------"
append_done "APEX login:"
append_done
append_done "APEX Workspace"
append_done "${ORDS_EXTERNAL_URL}/_/landing"
append_done "  Workspace: APEX_APP"
append_done "  User: APEX_APP"
append_done "  Password: $TF_VAR_db_password"
append_done
append_done "APEX APP"
append_done "${ORDS_EXTERNAL_URL}/r/apex_app/ai_agent_rag/"
append_done "  User: APEX_APP / $TF_VAR_db_password"
append_done
append_done "-----------------------------------------------------------------------"
append_done "LangGraph Agent Chat:"
append_done "${BASE_URL}/index.html"
append_done
append_done "-----------------------------------------------------------------------"
append_done "Oracle Digital Assistant (Web Channel)"
append_done "${BASE_URL}/oda.html"
append_done
if [ "$TF_VAR_openid" == "true" ]; then
    append_done "-----------------------------------------------------------------------"
    append_done "LangGraph OpenID Chat:"
    append_done "https://${APIGW_HOSTNAME}/openid/index.html"
    append_done
fi
if [ "$TF_VAR_kubernetes" == "true" ]; then
    append_done "-----------------------------------------------------------------------"
    append_done "Kubernetes Chat: http://${TF_VAR_ingress_ip}/oke/index.html"
    append_done
fi
