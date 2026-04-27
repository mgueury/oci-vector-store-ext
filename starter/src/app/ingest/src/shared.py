import os
import json
import requests
from datetime import datetime
import oci
import pathlib
import pprint
import base64
import mimetypes
# Responses
from oci_genai_auth import OciInstancePrincipalAuth
import httpx
from openai import OpenAI


# -- globals ----------------------------------------------------------------

# OCI Signer
if os.getenv("LIVELABS"):
    shared_config = oci.config.from_file()
    # Create a signer object from the config
    shared_signer = None
    shared_signer = oci.signer.Signer(
        tenancy=shared_config["tenancy"],
        user=shared_config["user"],
        fingerprint=shared_config["fingerprint"],
        private_key_file_location=shared_config["key_file"],
        pass_phrase=shared_config.get("pass_phrase")  # This is optional
    )
else:     
    shared_signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    shared_config = {'region': shared_signer.region, 'tenancy': shared_signer.tenancy_id}

# Log
log_file_name = None

# DB Env
db_env = None

# Create Log directory

UNIQUE_ID = "ID"

# Env Variables
REGION = os.getenv("TF_VAR_region")
COMPARTMENT_OCID = os.getenv("TF_VAR_compartment_ocid")
PROJECT_OCID = os.getenv("TF_VAR_project_ocid")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")
RESPONSES_MODEL_ID = os.getenv("TF_VAR_responses_model_id")
BUCKET_URL = os.getenv("BUCKET_URL")

## -- getLogDir -------------------------------------------------------------------
def getLogDir():
    LOG_DIR = '/tmp/app_log'
    # Create Log directory
    if os.path.isdir(LOG_DIR) == False:
        os.mkdir(LOG_DIR) 
    return LOG_DIR

## -- log_write_in_file -------------------------------------------------------------------
# Write logs in a file also 

def log_write_in_file( file_name ): 
   global log_file_name               
   log_file_name = file_name

## -- log -------------------------------------------------------------------

def log(s):
   global log_file_name
   dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   s2 = "["+dt+"] "+ str(s)
   print( s2, flush=True)
   if log_file_name:
       with open(log_file_name, "a", encoding="utf-8") as log_file:
           log_file.write(s2+'\n')       

## -- log_in_file -----------------------------------------------------------
# Log a full file 

def log_in_file(prefix, value):
    global UNIQUE_ID
    filename = getLogDir() +"/"+prefix+"_"+UNIQUE_ID+".txt"
    with open(filename, "w", encoding="utf-8") as text_file:
        text_file.write(value)
        text_file.flush() 
    log("<log_in_file>" +filename )  

## -- dictString ------------------------------------------------------------

def dictString(d,key):
   return d.get(key, "-")
   
## -- dictInt ------------------------------------------------------------

def dictInt(d,key):
   return int(float(d.get(key, 0)))

## -- image2DataUri ------------------------------------------------------------
# Converts a JPEG image file to a Base64 data URI.

def image2DataUri(image_path):
    log( f"<image2DataUri> image_path={image_path}")
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError("Error: Could not determine the MIME type of the file.")
        
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')  
    data_uri = f"data:{mime_type};base64,{encoded_string}"
    return data_uri

## -- summarizeContent ------------------------------------------------------

def summarizeContent(value,content):
    log( "<summarizeContent>")
    global signer
    compartmentId = value["data"]["compartmentId"] 
    endpoint = 'https://inference.generativeai.'+REGION+'.oci.oraclecloud.com/20231130/actions/chat'
    # Avoid Limit of 4096 Tokens
    if len(content) > 12000:
        log( "Truncating to 12000 characters")
        content = content[:12000]

    body = { 
        "compartmentId": compartmentId,
        "servingMode": {
            "modelId": os.getenv("TF_VAR_genai_cohere_model"),
            "servingType": "ON_DEMAND"
        },
        "chatRequest": {
            "maxTokens": 4000,
            "temperature": 0,
            "preambleOverride": "",
            "frequencyPenalty": 0,
            "presencePenalty": 0,
            "topP": 0.75,
            "topK": 0,
            "isStream": False,
            "message": "Summarise the following text in 200 words.\n\n"+content,
            "apiFormat": "COHERE"
        }
    }
    try: 
        resp = requests.post(endpoint, json=body, auth=shared_signer)
        resp.raise_for_status()
        log(resp)   
        log_in_file("summarizeContent_resp",str(resp.content)) 
        j = json.loads(resp.content)   
        log( "</summarizeContent>")
        return dictString(dictString(j,"chatResponse"),"text") 
    except requests.exceptions.HTTPError as err:
        log("\u270B Exception: summarizeContent") 
        log(err.response.status_code)
        log(err.response.text)
        return "-"   
    
## -- embedText -------------------------------------------------------------

# Ideally all vectors should be created in one call
def embedText(c):
    global signer
    log( "<embedText>")
    endpoint = 'https://inference.generativeai.'+REGION+'.oci.oraclecloud.com/20231130/actions/embedText'
    body = {
        "inputs" : [ c ],
        "servingMode" : {
            "servingType" : "ON_DEMAND",
            "modelId" : os.getenv("TF_VAR_genai_embed_model")
        },
        "truncate" : "START",
        "compartmentId" : COMPARTMENT_OCID
    }
    resp = requests.post(endpoint, json=body, auth=shared_signer)
    resp.raise_for_status()
    log(resp)    
    # Binary string conversion to utf8
    log_in_file("embedText_resp", resp.content.decode('utf-8'))
    j = json.loads(resp.content)   
    log( "</embedText>")
    return dictString(j,"embeddings")[0]     

## -- generic_chat -----------------------------------------------------------

def generic_chat(prompt, image_path=None, a_model=None, a_region=None):
    global signer
    log( "<generic_chat>")
    model = a_model or os.getenv("TF_VAR_genai_meta_model")
    endpoint = 'https://inference.generativeai.'+a_region+'.oci.oraclecloud.com/20231130/actions/chat'
    body = { 
        "compartmentId": COMPARTMENT_OCID,
        "servingMode": {
            "modelId": model,
            "servingType": "ON_DEMAND"
        },
        "chatRequest": {
            "apiFormat": "GENERIC",
            "maxTokens": 600,
            "temperature": 0,
            "topP": 0.75,
            "topK": 0,
            "messages": [
                {
                    "role": "USER", 
                    "content": [
                        {
                            "type": "TEXT",
                            "text": prompt
                        }
                    ]
                }  
            ]
        }
    }
    if image_path:
        body["chatRequest"]["messages"][0]["content"].append(
            {
                "type": "IMAGE",
                "imageUrl": {
                    "url": image2DataUri(image_path)
                }
            }
        )

    resp = requests.post(endpoint, json=body, auth=shared_signer)
    resp.raise_for_status()
    log(resp)    
    # Binary string conversion to utf8
    log_in_file("generic_chat_resp", resp.content.decode('utf-8'))
    j = json.loads(resp.content)   
    # Get the text
    chatResponse = j["chatResponse"]
    if chatResponse.get("text"):
        s=chatResponse["text"]
    else:
        s=chatResponse["choices"][0]["message"]["content"][0]["text"]
    # Remove JSON prefix if there    
    if s.startswith('```json'):
        start_index = s.find("{") 
        end_index = s.rfind("}")+1
        s = s[start_index:end_index]
    log( "</generic_chat>")
    return s

## -- cohere_chat -----------------------------------------------------------

def cohere_chat(prompt, chatHistory, documents):
    global signer
    log( "<cohere_chat>")
    endpoint = 'https://inference.generativeai.'+REGION+'.oci.oraclecloud.com/20231130/actions/chat'
    #         "modelId": "ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyafhwal37hxwylnpbcncidimbwteff4xha77n5xz4m7p6a",
    #         "modelId": os.getenv("TF_VAR_genai_cohere_model"),
    body = { 
        "compartmentId": COMPARTMENT_OCID,
        "servingMode": {
            "modelId": os.getenv("TF_VAR_genai_cohere_model"),
            "servingType": "ON_DEMAND"
        },
        "chatRequest": {
            "maxTokens": 600,
            "temperature": 0,
            "preambleOverride": "",
            "frequencyPenalty": 0,
            "presencePenalty": 0,
            "topP": 0.75,
            "topK": 0,
            "isStream": False,
            "message": prompt,
            "chatHistory": chatHistory,
            "documents": documents,
            "apiFormat": "COHERE"
        }
    }
    log_in_file("cohere_chat_request", json.dumps(body)) 
    resp = requests.post(endpoint, json=body, auth=shared_signer)
    resp.raise_for_status()
    log(resp)    
    # Binary string conversion to utf8
    log_in_file("cohere_chat_resp", resp.content.decode('utf-8'))
    j = json.loads(resp.content)   
    s = j["chatResponse"]
    log( "</cohere_chat>")
    return s

## -- appendChunk -----------------------------------------------------------

def appendChunck(result, text, char_start, char_end ):
    chunck = text[char_start:char_end]
    result.append( { "chunck": chunck, "char_start": char_start, "char_end": char_end } )
    log("chunck (" + str(char_start) + "-" + str(char_end-1) + ") - " + chunck)      

## -- cutInChunks -----------------------------------------------------------

def cutInChunks(text):
    result = []
    prev = ""
    i = 0
    last_good_separator = 0
    last_medium_separator = 0
    last_bad_separator = 0
    MAXLEN = 250
    char_start = 0
    char_end = 0

    i = 0
    while i<len(text)-1:
        i += 1
        cur = text[i]
        cur2 = prev + cur
        prev = cur

        if cur2 in [ ". ", ".[" , ".\n", "\n\n" ]:
            last_good_separator = i
        if cur in [ "\n" ]:          
            last_medium_separator = i
        if cur in [ " " ]:          
            last_bad_separator = i
        # log( 'cur=' + cur + ' / cur2=' + cur2 )
        if i-char_start>MAXLEN:
            char_end = i
            if last_good_separator > 0:
               char_end = last_good_separator
            elif last_medium_separator > 0:
               char_end = last_medium_separator
            elif last_bad_separator > 0:
               char_end = last_bad_separator
            # XXXX
            if text[char_end] in [ "[", "(" ]:
                appendChunck( result, text, char_start, char_end )
            else:     
                appendChunck( result, text, char_start, char_end )
            char_start=char_end 
            last_good_separator = 0
            last_medium_separator = 0
            last_bad_separator = 0
    # Last chunck
    appendChunck( result, text, char_start, len(text) )

    # Overlapping chuncks
    if len(result)==1:
        return result
    else: 
        result2 = []
        chunck_count=0
        chunck_start=0
        for c in result:
            chunck_count = chunck_count + 1
            if chunck_count==4:
                appendChunck( result2, text, chunck_start, c["char_end"] )
                chunck_start = c["char_start"]
                chunck_count = 0
        if chunck_count>0:
            appendChunck( result2, text, chunck_start, c["char_end"] )
        return result2
    

## -- getFileExtension ------------------------------------------------------

def getFileExtension(resourceName):
    lowerResourceName = resourceName.lower()
    return pathlib.Path(lowerResourceName).suffix

## -- delete_bucket_folder --------------------------------------------------

def delete_bucket_folder(namespace, bucketName, folder):
    log( "<delete_bucket_folder> "+folder)
    try:
        os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)    
        response = os_client.list_objects( namespace_name=namespace, bucket_name=bucketName, prefix=folder, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY, limit=1000 )
        for object_file in response.data.objects:
            f = object_file.name
            log( "<delete_bucket_folder> Deleting: " + f )
            os_client.delete_object( namespace_name=namespace, bucket_name=bucketName, object_name=f )
            log( "<delete_bucket_folder> Deleted: " + f )
    except:
        log("\u270B <delete_bucket_folder> Exception: delete_bucket_folder") 
        log(traceback.format_exc())            
    log( "</delete_bucket_folder>" )    

## -- delete_bucket_folder --------------------------------------------------

def responses_get_client():
    client = OpenAI(
        base_url=f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/20231130/openai/v1",
        api_key="unused",
        http_client=httpx.Client(
            auth=OciInstancePrincipalAuth(),
            headers={
                "opc-compartment-id": COMPARTMENT_OCID,
            },
        ),
    )
    return client

## -- responses_upload_file --------------------------------------------------

def responses_upload_file( file_path, metadata ):  
    log("<responses_upload_file>")
    log(f"file_path={file_path}")

    client = responses_get_client()

    with open(file_path, "rb") as f:
        # warning: repeating means you're uploading a new version of the same file
        # and it will create a new file each time. In production,
        # you should store the file ID and reuse it.
        file = client.files.create(
            file=f,
            purpose="user_data",
            extra_headers={"OpenAI-Project": PROJECT_OCID},
        )
        print(file)
        file_id = file.id

    print(file_id)
    create_result = client.vector_stores.files.create(
        vector_store_id=VECTOR_STORE_ID,
        file_id=file_id,
        attributes=metadata
    )    
    log( f"<responses_upload_file>Uploaded ${file_path}" )

## -- responses_format --------------------------------------------------

def responses_format(response):
    log(pprint.pformat( response ))
                
    # 1. Get the assistant message
    message = next(
        (o for o in response.output if o.type == "message"),
        None
    )
    
    if not message:
        return None

    content = message.content[0]

    # 2. Extract text
    text = content.text

    citations = []

    for item in response.output:
        if getattr(item, "type", None) != "file_search_call":
            continue

        for result in getattr(item, "results", []):
            entry = {
                "customized_url_source": result.attributes.get("customized_url_source"),
                "file_name": getattr(result, "filename", None),
                "score": getattr(result, "score", None),
            }
            citations.append(entry)
    citations_sorted = sorted(citations, key=lambda x: x["score"] or 0, reverse=True)            

    return {
        "response": text,
        "citation": citations_sorted
    }

## -- responses_upload_file --------------------------------------------------

def responses_search( question ):  
    log("<responses_search>")

    provider_name, separator, model_name = RESPONSES_MODEL_ID.partition(".")
    if provider_name == "google":
        role_instructions = "user"
    else:
        role_instructions = "system"

    client = responses_get_client()

    response = client.responses.create(
        model=RESPONSES_MODEL_ID,
        temperature=0.0,
        input=[
            {
                # cannot use system if provider is google
                "role": role_instructions,
                "content": (
                    "Answer using only information from the retrieved documents. "
                    "You may summarize or synthesize information that is explicitly supported by the retrieved text. "
                    "Do not use outside knowledge. "
                    "If the retrieved documents do not contain enough information to answer, say exactly: "
                    "'I don't have sufficient information in the documents.'"
                ),
            },
            {"role": "user", "content": question},
        ],
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
                "max_num_results": 10,
            }
        ],
        extra_headers={"OpenAI-Project": PROJECT_OCID},
        tool_choice="required",
        include=["file_search_call.results"],
    )
    return responses_format( response )

