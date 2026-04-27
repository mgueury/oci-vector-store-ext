from shared import log
from shared import log_in_file
import rag_storage
import file_convert
import shared

## -- eventDocument ---------------------------------------------------------

def eventDocument(value):
    log( "<eventDocument>")
    eventType = value["eventType"]
    # ex: /n/fr03kabcd/prefix-upload-bucket/o/country.pdf"
    resourceId = value["data"]["resourceId"]
    log( "eventType=" + eventType + " - " + resourceId ) 
    # eventType == "com.oraclecloud.objectstorage.createobject":
    # eventType == "com.oraclecloud.objectstorage.updateobject":
    # eventType == "com.oraclecloud.objectstorage.deleteobject":
    resourceName = value["data"]["resourceName"]
    resourceExtension = shared.getFileExtension(resourceName)
    log( "Extension:" + resourceExtension )

    # Content 
    result = { "content": "-" }
    if resourceExtension in [".tif"] or resourceName.endswith(".to_anonymize.pdf"):
        # This will create a JSON file in Object Storage that will create a second even with resourceExtension "json" 
        file_convert.convertOciDocumentUnderstanding(value)
        return
    elif resourceName.endswith(".anonymized.pdf"):
        file_convert.convertUploadAnonymizedPDF( value )
        return
    elif resourceExtension in [".pdf", ".txt", ".csv", ".md", ".html", ".htm", ""] or resourceName in ["_metadata_schema.json", "_all.metadata.json"] :
        # Simply copy the file to the agent bucket
        file_convert.convertUpload(value)
        return   
    elif resourceExtension in [".docx", ".doc",".pptx", ".ppt"] and file_convert.libreoffice_exe!=None:
        if rag_storage.RAG_STORAGE=="db26ai" and resourceExtension in [".pptx", ".ppt"]:
            # Convert to Markdown
            file_convert.convertUpload(value)
            return        
        else:
            # Convert to PDF            
            # Even for DB26ai, first convert to PDF (to get page numbers). Then PDF to text. (See https://github.com/docling-project/docling/discussions/1012)
            file_convert.convertLibreoffice2Pdf(value)
            return
    elif resourceExtension in [".png", ".jpg", ".jpeg", ".gif"]:
    #    file_convert.convertImage2Pdf(value)
         file_convert.convertGrokImage2Text(value)
         return    
    elif resourceExtension in [".mp3", ".mp4", ".avi", ".wav", ".m4a"]:
        # This will create a SRT file in Object Storage that will create a second even with resourceExtension ".srt" 
        file_convert.convertOciSpeech(value)
        return
    elif resourceExtension in [".selenium"]:
        # This will create a PDFs file in Object Storage with the content of each site (line) ".selenium" 
        file_convert.convertChromeSelenium2Pdf(value)
        return
    elif resourceExtension in [".crawler"]:
        # This will crawl all HTML pages of a website 
        file_convert.convertCrawler(value)
        return       
    elif resourceExtension in [".webp"]:
        # Convert webp to PNG
        file_convert.convertWebp2Png(value)
        return
    elif resourceExtension in [".srt"]:
        log("IGNORE .srt")
        return
    elif resourceName.endswith("/"):
        # Ignore
        log("IGNORE /")
        return

    if eventType in [ "com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject" ]:
        if resourceExtension in [".json"]:
            result = file_convert.convertJson(value)
        elif resourceExtension in [".png", ".jpg", ".jpeg", ".gif"]:
            result = file_convert.convertOciVision(value)
        else:
            result = file_convert.convertTika(value)

        if result:
            log_in_file("content", result["content"])
            if len(result["content"])==0:
                return 
            file_convert.convertUpload(value, result["content"], result["path"], result["originalResourceName"])    

    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        # No need to get the content for deleting
        file_convert.convertUpload(value, "-")    
              
    log( "</eventDocument>")
