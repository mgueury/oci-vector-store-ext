# -- Variables ---------------------------------------------

# Prefix to all resources created by terraform
prefix="__TO_FILL__"

# Min length 12 characters, 2 lowercase, 2 uppercase, 2 numbers, 2 special characters. Ex: LiveLab__12345
db_password="__TO_FILL__"

# BRING_YOUR_OWN_LICENSE or LICENSE_INCLUDED
license_model="__TO_FILL__"

# Compartment
compartment_ocid="__TO_FILL__"

# RAG Storage 26ai
# rag_storage="db26ai"
# vault_ocid="__TO_FILL__"
# vault_key_ocid="__TO_FILL__"

# Vector Store
rag_storage="vector_store"
# project_ocid="__TO_FILL__"
# responses_model_id="openai.gpt-oss-120b"

# Uncomment to enable login in LangGraph application using OpenID via API Gateway and Confidential Application 
# Needs OCI Identity Domain rights.
# openid="true"
