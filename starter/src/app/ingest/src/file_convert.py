# Import
import os
import json 
import requests
import oci
import csv
import time
from datetime import datetime
from pathlib import Path
from oci.object_storage.transfer.constants import MEBIBYTE
import urllib.parse
import traceback

# Anonymization
import anonym_pdf
from PIL import Image
import subprocess
import rag_storage

# Sitemap
import base64
import pdfkit
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# DocLing
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType

# Shared
import shared
from shared import log
from shared import log_in_file
from shared import dictString
from shared import getLogDir
from shared import shared_config
from shared import shared_signer
from shared import UNIQUE_ID

## -- find_executable_path --------------------------------------------------

def find_executable_path(prefix):
    for path in os.environ['PATH'].split(os.pathsep):
        try:
            for filename in os.listdir(path):
                if filename.startswith(prefix) and os.access(os.path.join(path, filename), os.X_OK) and os.path.isfile(os.path.join(path, filename)):
                   return os.path.join(path, filename)
        except:
            log( f"\u270B <find_executable_path>Executable {prefix} not found" )
            continue
    return None

## -- CONSTANTS -------------------------------------------------------------

libreoffice_exe = find_executable_path("libreoffice")
CONVERT_PREFIX="rag_file_convert/"

## -- get_metadata_from_resource_id -----------------------------------------
def get_metadata_from_resource_id( resourceId ):
    region = os.getenv("TF_VAR_region")
    customized_url_source = "https://objectstorage."+region+".oraclecloud.com" + resourceId
    return get_upload_metadata( customized_url_source )

## -- get_upload_metadata ---------------------------------------------------

def get_upload_metadata( customized_url_source ):
    log( "customized_url_source="+customized_url_source )
    customized_url_source = urllib.parse.quote(customized_url_source, safe=':/', encoding=None, errors=None)
    log( "After encoding="+customized_url_source )
    return {'customized_url_source': customized_url_source }

## -- convertOciFunctionTika ------------------------------------------------

def convertOciFunctionTika(value):
    global signer
    log( "<convertOciFunctionTika>")
    fnOcid = os.getenv('FN_OCID')
    fnInvokeEndpoint = os.getenv('FN_INVOKE_ENDPOINT')
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    
    invoke_client = oci.functions.FunctionsInvokeClient(config=shared_config, service_endpoint=fnInvokeEndpoint, signer=shared_signer)
    # {"bucketName": "xxx", "namespace": "xxx", "resourceName": "xxx"}
    req = '{"bucketName": "' + bucketName + '", "namespace": "' + namespace + '", "resourceName": "' + resourceName + '"}'
    log( "Tika request: " + req)
    resp = invoke_client.invoke_function(fnOcid, invoke_function_body=req.encode("utf-8"))
    text = resp.data.text.encode('iso-8859-1').decode('utf-8')
    log_in_file("tika_resp", text) 
    j = json.loads(text)
    result = {
        "originalResourceName": resourceName,
        "date": UNIQUE_ID,
        "applicationName": "Tika Parser",
        "modified": UNIQUE_ID,
        "contentType": dictString(j,"Content-Type"),
        "parsedBy": dictString(j,"X-Parsed-By"),
        "creationDate": UNIQUE_ID,
        "author": dictString(j,"Author"),
        "publisher": dictString(j,"publisher"),
        "content": j["content"],
        "path": resourceId
    }
    log( "</convertOciFunctionTika>")
    return result

## -- convertTika ------------------------------------------------
# Run Tika via subprocess

def convertTika(value):
    log( "<convertTika>")
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    
    command = ['./tika.sh', namespace, bucketName, resourceName ]
    try:
        text = subprocess.run(command, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        log("\n--- Tika finished successfully. ---")     
    except subprocess.CalledProcessError as e:
        log(f"\n\u270B Error: Tika command failed with return code {e.returncode}")
        log(f"Stderr:\n{e.stderr}")
        raise
    log_in_file("tika_resp", text) 
    j = json.loads(text)
    result = {
        "originalResourceName": resourceName,
        "date": UNIQUE_ID,
        "applicationName": "Tika Parser",
        "modified": UNIQUE_ID,
        "contentType": dictString(j,"Content-Type"),
        "parsedBy": dictString(j,"X-Parsed-By"),
        "creationDate": UNIQUE_ID,
        "author": dictString(j,"Author"),
        "publisher": dictString(j,"publisher"),
        "content": j["content"],
        "path": resourceId
    }
    log( "</convertTika>")
    return result
   
## -- convertOciVision --------------------------------------------------------------

def convertOciVision(value):
    log( "<convertOciVision>")
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    compartmentId = value["data"]["compartmentId"]
    resourceId = value["data"]["resourceId"]

    vision_client = oci.ai_vision.AIServiceVisionClient(config=shared_config, signer=shared_signer)
    job = {
        "compartmentId": compartmentId,
        "image": {
            "source": "OBJECT_STORAGE",
            "bucketName": bucketName,
            "namespaceName": namespace,
            "objectName": resourceName
        },
        "features": [
            {
                    "featureType": "IMAGE_CLASSIFICATION",
                    "maxResults": 5
            },
            {
                    "featureType": "TEXT_DETECTION"
            }
        ]
    }
    resp = vision_client.analyze_image(job)
    log_in_file("vision_resp", str(resp.data)) 

    concat_imageText = ""
    for l in resp.data.image_text.lines:
      concat_imageText += l.text + " "
    log("concat_imageText: " + concat_imageText )

    concat_labels = ""
    for l in resp.data.labels:
      concat_labels += l.name + " "
    log("concat_labels: " +concat_labels )

    result = {
        "originalResourceName": resourceName,
        "date": UNIQUE_ID,
        "modified": UNIQUE_ID,
        "contentType": "Image",
        "parsedBy": "OCI Vision",
        "creationDate": UNIQUE_ID,
        "content": concat_imageText + " " + concat_labels,
        "path": resourceId
    }
    log( "</convertOciVision>")
    return result    

## -- convertOciVisionBelgianID --------------------------------------------------------------

def convertOciVisionBelgianID(value):
    log( "<convertOciVisionBelgianID>")
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    compartmentId = value["data"]["compartmentId"]
    resourceId = value["data"]["resourceId"]

    vision_client = oci.ai_vision.AIServiceVisionClient(config=shared_config, signer=shared_signer)
    job = {
        "compartmentId": compartmentId,
        "image": {
            "source": "OBJECT_STORAGE",
            "bucketName": bucketName,
            "namespaceName": namespace,
            "objectName": resourceName
        },
        "features": [
            {
                    "featureType": "IMAGE_CLASSIFICATION",
                    "maxResults": 5
            },
            {
                    "featureType": "TEXT_DETECTION"
            }
        ]
    }
    resp = vision_client.analyze_image(job)
    log(resp.data)
    # log(json.dumps(resp,sort_keys=True, indent=4))

    name = resp.data.image_text.lines[8]
    id = resp.data.image_text.lines[19]
    birthdate = resp.data.image_text.lines[22]

    result = {
        "originalResourceName": resourceName,
        "date": UNIQUE_ID,
        "modified": UNIQUE_ID,
        "contentType": "convertOciVisionBelgianID ID",
        "parsedBy": "OCI Vision",
        "creationDate": UNIQUE_ID,
        "content": f"BelgianID: Name={name} / Id={id} / Birthdate={birthdate}",
        "path": resourceId
    }
    log( "</convertOciVisionBelgianID>")
    return result  

## -- convertOciSpeech ------------------------------------------------------
# 
# Use OCI Speech
# This will create a .json file with the result in public bucket in the folder "resourceName.speech"
# This .json file will be picked and indexed later

def convertOciSpeech(value):
    log( "<convertOciSpeech>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    compartmentId = value["data"]["compartmentId"]
    prefix = CONVERT_PREFIX + resourceName + ".speech"

    if eventType in [ "com.oraclecloud.objectstorage.updateobject", "com.oraclecloud.objectstorage.deleteobject" ]:
        # Delete previous speech conversion 
        shared.delete_bucket_folder( namespace, bucketName, prefix )

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        job = {
            "normalization": {
                    "isPunctuationEnabled": True
            },
            "compartmentId": compartmentId,
            "displayName": UNIQUE_ID,
            "modelDetails": {
                    "domain": "GENERIC",
                    "languageCode": "en-US"
            },
            "inputLocation": {
                    "locationType": "OBJECT_LIST_INLINE_INPUT_LOCATION",
                    "objectLocations": [
                        {
                                "namespaceName": namespace,
                                "bucketName": bucketName,
                                "objectNames": [
                                    resourceName
                                ]
                        }
                    ]
            },
            "outputLocation": {
                    "namespaceName": namespace,
                    "bucketName": bucketName,
                    "prefix": prefix
            },
            "additionalTranscriptionFormats": [
                    "SRT"
            ]
        }
        speech_client = oci.ai_speech.AIServiceSpeechClient(config=shared_config, signer=shared_signer)
        resp = speech_client.create_transcription_job(job)
        log_in_file("speech_resp",str(resp.data))

    log( "</convertOciSpeech>")

## -- convertOciDocumentUnderstanding ---------------------------------------

def convertOciDocumentUnderstanding(value):

    log( "<convertOciDocumentUnderstanding>")
    eventType = value["eventType"]    
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    compartmentId = value["data"]["compartmentId"]
    prefix = CONVERT_PREFIX + resourceName +".docu"

    if eventType in [ "com.oraclecloud.objectstorage.updateobject", "com.oraclecloud.objectstorage.deleteobject" ]:
        # Delete previous conversion 
        shared.delete_bucket_folder( namespace, bucketName, prefix )
        if eventType=="com.oraclecloud.objectstorage.deleteobject" and resourceName.endswith(".to_anonymize.pdf"):
            convertAnonymPDF( value, resourceName, None )

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        job = {
            "processorConfig": {
                "language": "ENG",
                "processorType": "GENERAL",
                "features": [
                    {
                        "featureType": "TEXT_EXTRACTION"
                    }
                ],
                "isZipOutputEnabled": False
            },
            "compartmentId": compartmentId,
            "inputLocation": {
                "sourceType": "OBJECT_STORAGE_LOCATIONS",
                "objectLocations": [
                    {
                        "bucketName": bucketName,
                        "namespaceName": namespace,
                        "objectName": resourceName
                    }
                ]
            },
            "outputLocation": {
                "namespaceName": namespace,
                "bucketName": bucketName,
                "prefix": prefix
            }
        }
        document_understanding_client = oci.ai_document.AIServiceDocumentClient(config=shared_config, signer=shared_signer)
        resp = document_understanding_client.create_processor_job(job)
        log_in_file("convertOciDocumentUnderstanding_resp",str(resp.data))
    log( "</convertOciDocumentUnderstanding>")

## -- chrome_webdriver ---------------------------------------------------

def chrome_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-notifications")    
    options.add_argument(f"--user-data-dir=/home/opc/chrome_profile")
    settings = {
        "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': '/tmp/',
        'download.default_directory': '/tmp/',
        'plugins.plugins_disabled': "Chrome PDF Viewer",
        'plugins.always_open_pdf_externally': "true"
    }    
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--kiosk-printing')  
    driver = webdriver.Chrome(options=options)
    return driver

## -- chrome_download_url_as_pdf ---------------------------------------------------
def chrome_download_url_as_pdf( driver, url, output_filename):
    driver.get(url)
    driver.implicitly_wait(15) 
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
        WebDriverWait(driver, 20).until(element_present) 
    except Exception as e:
        log(f"\u270B Error waiting for element: {e}")    

    print_options = {
        "marginsType": 1,         # Set margins (0 = default, 1 = no margins, 2 = minimal margins)
        "printBackground": False  # Print background graphics
    }
    params = {'behavior': 'default', 'downloadPath': os.getcwd()} # Set the download directory to current working directory
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params) # Set the download path for the PDF
    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
    pdf_data = result['data']
    with open(output_filename, "wb") as f:
        f.write(bytes(base64.b64decode(pdf_data)))
    log(f"<chrome_download_url_as_pdf> Saved {output_filename}")   

## -- convertChromeSelenium2Pdf ----------------------------------------------------
def convertChromeSelenium2Pdf(value):

    # Read the SITEMAP file from the object storage
    # The format of the file expected is a txt file. Each line contains a full URI.
    # Transforms all the links in PDF and reupload them as PDF in the same object storage
    log("<convertChromeSelenium2Pdf>")
    eventType = value["eventType"]     
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    folder=resourceName+".download"

    if eventType in [ "com.oraclecloud.objectstorage.updateobject", "com.oraclecloud.objectstorage.deleteobject" ]:
        rag_storage.delete_folder( value, folder )
    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:         
        fileList = []

        os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)

        resp = os_client.get_object(namespace_name=namespace, bucket_name=bucketName, object_name=resourceName)
        folder = resourceName
        file_name = getLogDir()+"/"+UNIQUE_ID+".sitemap"
        with open(file_name, 'wb') as f:
            for chunk in resp.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)

        if os.getenv("INSTALL_LIBREOFFICE")!="no":
            driver = chrome_webdriver()
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    try:
                        line = line.strip()  # Remove leading/trailing whitespace
                        # Handle empty lines gracefully
                        if not line:
                            continue

                        full_uri = line

                        # Print the filename with the ".pdf" extension
                        pdf_path = full_uri
                        # Remove trailing /
                        last_char = pdf_path[-1:]
                        if last_char == '/':
                            pdf_path = pdf_path[:-1]

                        pdf_path = pdf_path.replace('/', '___');
                        pdf_path = pdf_path+'.pdf'
                        log("<convertChromeSelenium2Pdf>"+full_uri)
                        if os.getenv("INSTALL_LIBREOFFICE")!="no":
                            chrome_download_url_as_pdf( driver, full_uri, getLogDir()+'/'+pdf_path)
                        else:
                            pdfkit.from_url(full_uri, getLogDir()+"/"+pdf_path)
    
                        metadata = {'customized_url_source': full_uri, 'source_type': 'HTTP' }

                        # Upload to object storage as "site/"+pdf_path
                        rag_storage.upload_file(value=value, object_name=folder+"/"+pdf_path, file_path=getLogDir()+"/"+pdf_path, content_type='application/pdf', metadata=metadata)
                        fileList.append( folder+"/"+pdf_path )
                      
                    except Exception as e:
                        log("\u270B <convertChromeSelenium2Pdf>Error parsing line: "+line+" in "+resourceName)
                        log("<convertChromeSelenium2Pdf>Exception:" + str(e))

            # Check if there are file that are in the folder and not in the sitemap
            # response = os_client.list_objects( namespace_name=namespace, bucket_name=bucketGenAI, prefix=folder, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY, limit=1000 )
            # for object_file in response.data.objects:
            #     f = object_file.name
            #     if f in fileList:
            #         fileList.remove(f)
            #     else: 
            #         rag_storage.delete_file( value=value, object_name=f )

        except FileNotFoundError as e:
            log("\u270B <convertChromeSelenium2Pdf>Error: File not found= "+file_name)
        except Exception as e:
            log("\u270B <convertChromeSelenium2Pdf>An unexpected error occurred: " + str(e))
        if os.getenv("INSTALL_LIBREOFFICE")!="no":    
            driver.quit()            
    log( "</convertChromeSelenium2Pdf>")


## -- convertAnonymPDF ------------------------------------------------------------------
# Called by DocumentUnderstanding convertJson

def convertAnonymPDF(value, originalResourceName, j):
    log( "<convertAnonymPDF>")
    eventType = value["eventType"]  
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    anonymizedPdf = CONVERT_PREFIX + originalResourceName.replace(".to_anonymize.pdf", ".anonymized.pdf") 

    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)            
    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:     
        anonym_pdf_file = download_file( namespace, bucketName, originalResourceName)
        pdf_file = anonym_pdf.remove_entities(anonym_pdf_file, j)
        # Upload the anonymize file in the public bucket.
        upload_manager = oci.object_storage.UploadManager(os_client, max_parallel_uploads=10)
        upload_manager.upload_file(namespace_name=namespace, bucket_name=bucketName, object_name=anonymizedPdf, file_path=pdf_file, part_size=2 * MEBIBYTE, content_type="application/pdf")
    elif eventType in [ "com.oraclecloud.objectstorage.deleteobject" ]:
        os_client.delete_object(namespace_name=namespace, bucket_name=bucketName, object_name=anonymizedPdf)        


## -- convertUploadAnonymizedPDF ------------------------------------------------------------------
# Calculate the originalResourceName then upload the document
# Called by Document.py 
def convertUploadAnonymizedPDF(value):
    log( "<convertUploadAnonymizedPDF>")    
    # remove first directory
    resourceName = value["data"]["resourceName"]
    originalResourceName = os.path.join(*(resourceName.split(os.path.sep)[1:]))
    originalResourceName = originalResourceName.replace(".anonymized.pdf",".to_anonymize.pdf")                                                       
    convertUpload(value, None, None, originalResourceName )

## -- convertJson ------------------------------------------------------------------

def convertJson(value):
    log( "<convertJson>")
    global signer
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    
    log(f"<convertJson>namespace={namespace}" )
    log(f"<convertJson>bucketName={bucketName}" )
    log(f"<convertJson>resourceName={resourceName}" )
    # Read the JSON file from the object storage
    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)
    resp = os_client.get_object(namespace_name=namespace, bucket_name=bucketName, object_name=resourceName)
    file_name = getLogDir()+"/"+UNIQUE_ID+".json"
    with open(file_name, 'wb') as f:
        for chunk in resp.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)

    with open(file_name, 'r') as f:
        file_content = f.read()
    log("Read file from object storage: "+ file_name)
    j = json.loads(file_content)   

    if ".docu/" in resourceName:
        # DocUnderstanding
        originalResourceName = resourceName[:resourceName.index(".json")][resourceName.index("/results/")+9:]
        originalResourceId = "/n/" + namespace + "/b/" + bucketName + "/o/" + originalResourceName
        if originalResourceName.endswith(".to_anonymize.pdf"):
            convertAnonymPDF( value, originalResourceName, j )
            return None  
        else: 
            concat_text = ""
            pages = {}
            for p in j.get("pages"):
                pageNumber = p.get("pageNumber")
                page = ""
                for l in p.get("lines"):
                    page += l.get("text") + "\n"
                pages[str(pageNumber)] = page
                concat_text += page + " "         
            result = {
                "originalResourceName": originalResourceName,
                "date": UNIQUE_ID,
                "applicationName": "OCI Document Understanding",
                "modified": UNIQUE_ID,
                "contentType": j["documentMetadata"]["mimeType"],
                "creationDate": UNIQUE_ID,
                "content": concat_text,
                "pages": pages,
                "path": originalResourceId
            }            
    else:
        # Speech
        originalResourceName = resourceName[:resourceName.index(".json")][resourceName.index("bucket_")+7:]
        originalResourceId = "/n/" + namespace + "/b/" + bucketName + "/o/" + originalResourceName
        result = {
            "originalResourceName": originalResourceName,
            "date": UNIQUE_ID,
            "applicationName": "OCI Speech",
            "modified": UNIQUE_ID,
            "contentType": j["audioFormatDetails"]["format"],
            "creationDate": UNIQUE_ID,
            "content": j["transcriptions"][0]["transcription"],
            "path": originalResourceId
        }
    log( "</convertJson>")
    return result

## -- convertUpload ---------------------------------------------------
# Parameters:
#   content: (default none): text content of the file
#   fileName: (default none): fileName when already downloaded (ex: test.anonymized.pdf )

def convertUpload(value, content=None, path=None, originalResourceName=None):

    log( "<convertUpload>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceGenAI = resourceName
    
    if content:
        resourceGenAI = resourceGenAI + ".convert.txt"   

    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        # Set the original URL source (GenAI Agent)
        if path==None:
            path = value["data"]["resourceId"]
        region = os.getenv("TF_VAR_region")
        customized_url_source = "https://objectstorage."+region+".oraclecloud.com" + path
        log( "customized_url_source="+customized_url_source )
        metadata = get_upload_metadata( customized_url_source )
        if originalResourceName:
            metadata["originalResourceName"] = originalResourceName 

        file_name = getLogDir()+"/"+resourceName
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        if not content:
            contentType = value["contentType"]
            resp = os_client.get_object(namespace_name=namespace, bucket_name=bucketName, object_name=resourceName)
            with open(file_name, 'wb') as f:
                for chunk in resp.data.raw.stream(1024 * 1024, decode_content=False):
                    f.write(chunk)
        else:
            contentType = "text/html"
            with open(file_name, 'w') as f:
                f.write(content)

        rag_storage.upload_file( value=value, object_name=resourceGenAI, file_path=file_name, content_type=contentType, metadata=metadata)
        os.remove( file_name )
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        rag_storage.delete_file( value=value, object_name=resourceGenAI)
    log( "</convertUpload>")                                  

## -- convertLibreoffice2Pdf ------------------------------------------------------------

def convertLibreoffice2Pdf(value):
    log( "<convertLibreoffice2Pdf>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    resourceGenAI = str(Path(resourceName).with_suffix('.pdf'))
      
    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        office_file = download_file( namespace, bucketName, resourceName)
        log( f'libreoffice_exe={libreoffice_exe}' )
        cmd = [ libreoffice_exe ] + '--convert-to pdf --outdir'.split() + [getLogDir(), office_file]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.wait(timeout=30)
        stdout, stderr = p.communicate()
        time.sleep(10) 
        pdf_file = str(Path(office_file).with_suffix('.pdf'))
        if os.path.exists(pdf_file):
            log( f"<convertLibreoffice2Pdf> pdf found {pdf_file}")
        else:
            raise subprocess.SubprocessError(stderr)
        metadata = get_metadata_from_resource_id( resourceId )
        log( "pdf_file=" + pdf_file )
        log( "metadata=" + str(metadata) )
        log( "resourceGenAI=" + resourceGenAI )
        rag_storage.upload_file( value=value, object_name=resourceGenAI, file_path=pdf_file, content_type="application/pdf", metadata=metadata)
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        rag_storage.delete_file( value=value, object_name=resourceGenAI )
    log( "</convertLibreoffice2Pdf>")

## -- download_file ---------------------------------------------------------

def download_file(namespace,bucketName,resourceName):
    log( "<download_file>")
    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)
    resp = os_client.get_object(namespace_name=namespace, bucket_name=bucketName, object_name=resourceName)
    # Remove the directory name
    file_name = getLogDir()+"/"+os.path.basename(resourceName)
    # Download the file
    with open(file_name, 'wb') as f:
        for chunk in resp.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    log( "</download_file>")            
    return file_name

## -- save_image_as_pdf -----------------------------------------------------

def save_image_as_pdf( file_name, images ):
    # Save image with PIL
    if len(images) == 1:
        images[0].save(file_name)
    else:
        im = images.pop(0)
        im.save(file_name, save_all=True,append_images=images)

## -- convertGrokImage2Text --------------------------------------------------
#
# Convert the Image file to text using "xai.grok-4" in "us-chicago-1"

def convertGrokImage2Text(value, content=None, path=None):
    log( "<convertGrokImage2Text>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    resourceGenAI = resourceName+".txt"
  
    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        # Set the original URL source (GenAI Agent)
        metadata = get_metadata_from_resource_id( resourceId )

        image_file = download_file( namespace, bucketName, resourceName)     
        text = shared.generic_chat("describe the image", image_path=image_file, a_model="xai.grok-4", a_region="us-chicago-1")

        dest_file = getLogDir()+"/"+UNIQUE_ID+".md"        
        with open(dest_file, 'w', encoding='utf-8') as f_out:
            f_out.write(text)   

        rag_storage.upload_file( value=value, object_name=resourceGenAI, file_path=dest_file, content_type="text/markdown", metadata=metadata)
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        rag_storage.delete_file( value=value, object_name=resourceGenAI )
    log( "</convertGrokImage2Text>")

## -- convertImage2Pdf ------------------------------------------------------
#
# Convert the Image to PDF

def convertImage2Pdf(value, content=None, path=None):
    log( "<convertImage2Pdf>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    resourceGenAI = resourceName+".pdf"
  
    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        # Set the original URL source (GenAI Agent)
        metadata = get_metadata_from_resource_id( resourceId )

        image_file = download_file( namespace, bucketName, resourceName)     
        image = Image.open(image_file)
        pdf_file = getLogDir()+"/"+UNIQUE_ID+".pdf"
        save_image_as_pdf( pdf_file, [image] )         

        rag_storage.upload_file( value=value, object_name=resourceGenAI, file_path=pdf_file, content_type="application/pdf", metadata=metadata)
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        rag_storage.delete_file( value=value, object_name=resourceGenAI )
    log( "</convertImage2Pdf>")

## -- convertWebp2Png -----------------------------------------------------
#
# Convert the Webp file and store the .png in the public bucket.
# That .png will be picked later and indexed.

def convertWebp2Png(value, content=None, path=None):
    log( "<convertWebp2Png>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    resourceGenAI = resourceName+".png"
  
    os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        # Set the original URL source (GenAI Agent)
        metadata = get_metadata_from_resource_id( resourceId )

        image_file = download_file( namespace, bucketName, resourceName)     
        image = Image.open(image_file).convert("RGB")
        png_file = getLogDir()+"/"+UNIQUE_ID+".png"
        image.save(png_file, "png")   
        upload_manager = oci.object_storage.UploadManager(os_client, max_parallel_uploads=10)
        upload_manager.upload_file(namespace_name=namespace, bucket_name=bucketName, object_name=resourceGenAI, file_path=png_file, part_size=2 * MEBIBYTE, content_type="image/png", metadata=metadata)
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        log( "<convertWebp2Png> Delete")
        try: 
            os_client.delete_object(namespace_name=namespace, bucket_name=bucketName, object_name=resourceGenAI)
        except:
           log("Exception: Delete failed: " + resourceGenAI)   
    log( "</convertWebp2Png>")    

## -- run_crawler ------------------------------------------------------------

def run_crawler(url):
    """
    Executes the spider and, upon completion, reads and
    prints the contents of the generated links.csv file.
    """
    # Define the command to run the Spider.
    # The command assumes you are running this script from the
    # root directory of the project (where scrapy.cfg is located).
    crawler_command = ['./crawler.sh', url]
    
    # Define the path to the output CSV file.
    output_dir = '/tmp/crawler'
    csv_filename = 'links.csv'
    csv_file_path = os.path.join(output_dir, csv_filename)

    log("--- Starting Crawler. Please wait... ---")   
    try:
        # Run the command. The 'check=True' argument will raise an
        # exception if the command fails, which is good for error handling.
        # result = subprocess.check_output(crawler_command, check=True, capture_output=True, text=True)
        result = subprocess.run(crawler_command, check=True, stdout=subprocess.PIPE).stdout
        log("\n--- Crawler finished successfully. ---")
        
    except subprocess.CalledProcessError as e:
        # Handle cases where the command fails.
        log(f"\n\u270B Error: Crawler command failed with return code {e.returncode}")
        log(f"Stderr:\n{e.stderr}")
        raise

## -- convertCrawler ------------------------------------------------------------------
def convertCrawler(value):
    log( "<convertCrawler>")
    eventType = value["eventType"]     
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    folder=resourceName+".download"

    if eventType in [ "com.oraclecloud.objectstorage.updateobject", "com.oraclecloud.objectstorage.deleteobject" ]:
        rag_storage.delete_folder( value, folder )
    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:         
        fileList = []

        os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)

        resp = os_client.get_object(namespace_name=namespace, bucket_name=bucketName, object_name=resourceName)
        file_name = getLogDir()+"/"+UNIQUE_ID+".crawler"
        with open(file_name, 'wb') as f:
            for chunk in resp.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)

        try:
            with open(file_name, 'r') as f:
                for line in f:
                    try:
                        line = line.strip()  # Remove leading/trailing whitespace
                        # Handle empty lines gracefully
                        if not line:
                            continue

                        full_uri = line
                        run_crawler(full_uri)
                        # Check if the CSV file was created by the spider.
                        CRAWLER_DIR='/tmp/crawler'
                        csv_file_path=CRAWLER_DIR+'/links.csv'
                        log(f"\n--- Reading data from '{csv_file_path}'... ---")
                       
                        # Open and read the CSV file.
                        if not os.path.exists(csv_file_path):
                            log(f"Error: The file '{csv_file_path}' was not created.")
                            log("Please check the spider's output for any errors.")
                            return

                        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                            # Use DictReader for easy access to columns by their header.
                            reader = csv.DictReader(csvfile)            
                            # Loop through each row and print the URL and filename.
                            for row in reader:
                                url = row.get('url', 'N/A')
                                filename = row.get('filename', 'N/A')
                                title = row.get('title', 'N/A')
                                filename = filename[len(CRAWLER_DIR)+1:]
                                log(f"URL: {url} - Filename: {filename}")
                                metadata=  {'customized_url_source': url, 'source_type': 'HTTP' } 
                                # value["data"]["resourceName"] = title   
                                value["title"] = title   
                                rag_storage.upload_file(value=value, object_name=folder+"/"+filename, file_path=CRAWLER_DIR+"/"+filename, content_type='text/html', metadata=metadata)
                                fileList.append(filename)
                        
                    except Exception as e:
                        log("\u270B <convertCrawler>Error parsing line: "+line+" in "+resourceName)
                        log(f"<convertCrawler>Exception: {e}")
                        log(traceback.format_exc())

            # Check if there are file that are in the folder and not in the crawler
            # response = os_client.list_objects( namespace_name=namespace, bucket_name=bucketGenAI, prefix=folder, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY, limit=1000 )
            # for object_file in response.data.objects:
            #     f = object_file.name
            #     if f in fileList:
            #         fileList.remove(f)
            #     else: 
            #         rag_storage.delete_file( value=value, object_name=f )                    

        except FileNotFoundError as e:
            log("\u270B <convertCrawler>Error: File not found= "+file_name)
        except Exception as e:
            log("\u270B <convertCrawler>An unexpected error occurred: " + str(e))     
    log( "</convertCrawler>")

## -- convertDocling ------------------------------------------------------------

def convertDocling(value):
    log("<convertDocling>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    resourceGenAI = str(Path(resourceName).with_suffix('.md'))
      
    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        # Set the original URL source (GenAI Agent)
        metadata = get_metadata_from_resource_id( resourceId )
        orig_file = download_file( namespace, bucketName, resourceName)     
        dest_file = getLogDir()+"/"+UNIQUE_ID+".md"
        loader = DoclingLoader(
            file_path=orig_file,
            export_type=ExportType.MARKDOWN
        )
        docs = loader.load()        
        value["content"] = ""
        for d in docs:
            value["content"] = value["content"] + d.page_content
        with open(dest_file, 'w', encoding='utf-8') as f_out:
            f_out.write(value["content"])       
        rag_storage.upload_file( value=value, object_name=resourceGenAI, file_path=dest_file, content_type="text/markdown", metadata=metadata)
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        rag_storage.delete_file( value=value, object_name=resourceGenAI )
    log("</convertDocling>")



