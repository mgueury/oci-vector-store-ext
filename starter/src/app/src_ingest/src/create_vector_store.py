import time
import os
from datetime import datetime
import httpx
from oci_genai_auth import OciInstancePrincipalAuth
from openai import OpenAI

def main() -> None:
    COMPARTMENT_OCID = os.getenv("TF_VAR_compartment_ocid")
    PREFIX = os.getenv("TF_VAR_prefix")
    REGION = os.getenv("TF_VAR_region")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    
    print("<create_vector_store.py>")

    cp_client = OpenAI(
        base_url=f"https://generativeai.{REGION}.oci.oraclecloud.com/20231130/openai/v1",
        api_key="unused",
        http_client=httpx.Client(
            auth=OciInstancePrincipalAuth(),
            headers={
                "opc-compartment-id": COMPARTMENT_OCID,
            },
        ),
    )

    vector_store = cp_client.vector_stores.create(
        name=f"{PREFIX}-vs-{timestamp}",
        description=f"{PREFIX} vector store",
        expires_after={"anchor": "last_active_at", "days": 365}, # 1 YEAR ? 
        metadata={"prefix": "{PREFIX}"},
    )

    print(vector_store)
  
    elapsed = 0
    vector_store_id=vector_store.id
    while elapsed < 500:
        vector_store = cp_client.vector_stores.retrieve(vector_store_id)
        print( vector_store.status )
        if vector_store.status != "in_progress":
            break
        time.sleep(5)  
        elapsed += 5

    print(f"Time {elapsed} secs")
    if vector_store.status == "completed":
        print("Vector store created successfully.")
    elif elapsed>=500:
        print("Timeout reached before completion.")
    else:
        print("Vector store creation failed. Status={vector_store.status}")
        exit( 1 )

    # Create bash file
    with open("responses_env.sh", "w") as f:
        f.write(f'# VECTOR_STORE {PREFIX}-vs-{timestamp}"\n')
        f.write(f'export VECTOR_STORE_ID="{vector_store.id}"\n')

    print("responses_env.sh file created.")

if __name__ == "__main__":
    main()

    
