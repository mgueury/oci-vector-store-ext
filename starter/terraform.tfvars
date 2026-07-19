# -- Variables ---------------------------------------------

# Prefix to all resources created by terraform
prefix="__TO_FILL__"

# IP Range that can access port like 80/443 on the internet. Typically:
# - All internet - 0.0.0.0/0
# - or <your_laptop_ip>/32. Get your Laptop IP using, by example, https://whatismyipaddress.com
public_ip_filter="__TO_FILL__"

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
project_ocid="__TO_FILL__"
genai_model="openai.gpt-oss-120b"

# Uncomment to enable login in LangGraph application using OpenID via API Gateway and Confidential Application 
# Needs OCI Identity Domain rights.
# openid="true"

# LangFuse
# langfuse_public_key="pk-lf-change-it"
# langfuse_secret_key="sk-lf-change-it"
# langfuse_base_url="http://langfuse-compute.##PREFIX##web.##PREFIX##vcn.oraclevcn.com:3000"