# Import
import os
import array
import pprint
import oracledb
import pathlib
import shared
from shared import log
from shared import dictString
from shared import shared_config
from shared import shared_signer
import oci
from oci.object_storage.transfer.constants import MEBIBYTE

# Langchain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents import Document
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.embeddings import OCIGenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import DistanceStrategy

# Docling
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from docling.chunking import HybridChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter

from typing import List, Tuple

# -- Globals ----------------------------------------------------------------

region = os.getenv("TF_VAR_region")
embeddings = OCIGenAIEmbeddings(
    model_id=os.getenv("TF_VAR_genai_embed_model"),
    service_endpoint="https://inference.generativeai."+region+".oci.oraclecloud.com",
    compartment_id=os.getenv("TF_VAR_compartment_ocid"),
    auth_type="API_KEY" if "LIVELABS" in os.environ else "INSTANCE_PRINCIPAL"
)
# db26ai or object_storage
RAG_STORAGE = os.getenv("TF_VAR_rag_storage")
ORDS_EXTERNAL_URL = os.getenv("ORDS_EXTERNAL_URL")
DOCLING_HYBRID_CHUNK=True #False

# connection pool
pool = None

## -- createPool ------------------------------------------------------------------

def createPool():
    global pool 
    # Thick driver...
    # oracledb.init_oracle_client()
    # Create the pool with the "proxy" user
    pool = oracledb.SessionPool(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dsn=os.getenv('DB_URL'),
        min=10, max=10, increment=0,
        encoding="UTF-8",
        getmode=oracledb.SPOOL_ATTRVAL_WAIT            
    )

## -- init ------------------------------------------------------------------

def init():
    if RAG_STORAGE=="db26ai":
        createPool()

## -- close -----------------------------------------------------------------

def close():
    if RAG_STORAGE=="db26ai":
        global pool 
        pool.close()

## -- updateCount ------------------------------------------------------------------

countUpdate = 0

def updateCount(count):
    global countUpdate

    ## RAG ObjectStorage - start Ingestion when no new messsage is arriving
    if RAG_STORAGE=="db26ai":
        pass
    elif RAG_STORAGE=="vector_store":
        pass    
    else:
        if count>0:
            countUpdate = countUpdate + count 
        elif countUpdate>0:
            try:
                # XXXX
                log( "<updateCount>ingest job created")
                countUpdate = 0
            except (Exception) as e:
                log(f"\u270B <updateCount>ERROR: {e}") 

## -- upload_file -----------------------------------------------------------

def upload_file( value, object_name, file_path, content_type, metadata ):  
    log("<upload_file>")

    # Enrich metadata (based on folder name category1/category2/category3/file.txt)
    # See https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/RAG-tool-object-storage-guidelines.htm
    originalResourceName = metadata.get("originalResourceName", value["data"]["resourceName"])
    metadata['gaas-metadata-filtering-field-originalResourceName'] = originalResourceName

    parts = originalResourceName.split('/')
    if len(parts)>1:
        metadata['gaas-metadata-filtering-field-category1'] = parts[0]
    if len(parts)>2:
        metadata['gaas-metadata-filtering-field-category2'] = parts[1]
    if len(parts)>3:
        metadata['gaas-metadata-filtering-field-category3'] = parts[2]

    if RAG_STORAGE=="db26ai":
        value["metadata"] = metadata
        insertDoc( value, file_path, object_name )
    elif RAG_STORAGE=="vector_store":
        shared.responses_upload_file(file_path, metadata)
    else:
        namespace = value["data"]["additionalDetails"]["namespace"]
        bucketName = value["data"]["additionalDetails"]["bucketName"]
        bucketGenAI = bucketName.replace("-upload-bucket","-converted-bucket")        

        os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)
        upload_manager = oci.object_storage.UploadManager(os_client, max_parallel_uploads=10)
        upload_manager.upload_file(namespace_name=namespace, bucket_name=bucketGenAI, object_name=object_name, file_path=file_path, part_size=2 * MEBIBYTE, content_type=content_type, metadata=metadata)
    log("<upload_file>Uploaded "+object_name + " - " + content_type )

## -- delete_file -----------------------------------------------------------

def delete_file( value, object_name ): 
    log(f"<delete_file>{object_name}")     
    if RAG_STORAGE=="db26ai":
        deleteDocByOriginalResourceName( value )
    else:
        try: 
            namespace = value["data"]["additionalDetails"]["namespace"]
            bucketName = value["data"]["additionalDetails"]["bucketName"]
            bucketGenAI = bucketName.replace("-upload-bucket","-converted-bucket")               
            os_client = oci.object_storage.ObjectStorageClient(config=shared_config, signer=shared_signer)            
            os_client.delete_object(namespace_name=namespace, bucket_name=bucketGenAI, object_name=object_name)
        except:
           log("Exception: Delete failed: " + object_name)   
    log("</delete_file>")     

## -- delete_folder ---------------------------------------------------------

def delete_folder(value, folder):
    log( "<delete_folder> "+folder)
    if RAG_STORAGE=="db26ai":
        deleteDocByOriginalResourceName( value )
    else:
        namespace = value["data"]["additionalDetails"]["namespace"]
        bucketName = value["data"]["additionalDetails"]["bucketName"]
        bucketGenAI = bucketName.replace("-upload-bucket","-converted-bucket")
        shared.delete_bucket_folder(namespace, bucketGenAI, folder)
    log( "</delete_folder>" )    

# -- insertDoc -----------------------------------------------------------------
# See https://python.langchain.com/docs/integrations/document_loaders/

def insertDoc( value, file_path, object_name ):
    if file_path:
        extension = pathlib.Path(object_name.lower()).suffix
        resourceName = value["data"]["resourceName"]
          
        if resourceName in ["_metadata_schema.json", "_all.metadata.json"]:
            return
        elif extension in [ ".txt", ".json" ]:
            loader = TextLoader( file_path=file_path )
            docs = loader.load()
        elif extension in [ ".md", ".html", ".htm", ".pdf", ".doc", ".docx", ".ppt", ".pptx" ]:
            # Get the full file in Markdown
            loader = DoclingLoader(
                file_path=file_path,
                export_type=ExportType.MARKDOWN
            )
            docs = loader.load()
            value["content_markdown"] = True
        # elif extension in [ ".pdf" ]:
            # loader = PyPDFLoader(
            #     file_path,
            #     mode="page"
            # )
        else:
            log(f"\u270B <insertDoc> Error: unknown extension: {extension}")
            return
        docs = loader.load()        

        value["content"] = ""
        for d in docs:
            value["content"] = value["content"] + d.page_content

        log("len(docs)="+str(len(docs)))
        log("-- doc[0].metadata --------------------")
        log(pprint.pformat(docs[0].metadata))

        # source_type=OBJECT_STORAGE unless told differently via metadata
        value["source_type"] =  value["metadata"].get("source_type", "OBJECT_STORAGE" )

        # Summary 
        if len(value["content"])>250:
            value["summary"] = shared.summarizeContent(value, value["content"])
        else:    
            value["summary"] = value["content"]            
        log("Summary="+value["summary"])
        
        deleteDocByPath(value) 

        if len(value["summary"])>0:
            log("Summary="+value["summary"])
            value["summaryEmbed"] = embeddings.embed_query(value["summary"])
        else:
            log(f"\u270B Summary is empty... Skipping {resourceName}")
            return
            
        insertTableDocs(value)
        insertTableDocsChunck(value, docs, file_path)  

# -- insertTableDocs -----------------------------------------------------------------
# Normal insert

def insertTableDocs( value ):  
    global pool
    dbConn = pool.acquire()
    cur = dbConn.cursor()
    log("<insertTableDocs>")
    # log(pprint.pformat(value))    
    # CLOB at the end (content, summary) to avoid BINDING error: ORA-24816: Expanded non LONG bind data supplied after actual LONG or LOB column
    stmt = """
        INSERT INTO docs (
            status, application_name, author, translation, content_type,
            creation_date, modified, category1, category2, category3, parsed_by,
            resource_name, original_resource_name, path, title, region, summary_embed, source_type,
            content, summary
        )
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20)
        RETURNING id INTO :21
    """
    resourceName=value["data"]["resourceName"]
    # provided title if not resourceName
    title = value.get("title", resourceName)
    # resourceName is only valid when the file is in OBJECT_STORAGE
    if value.get("source_type")!='OBJECT_STORAGE':
        resourceName = ""

    metadata = value["metadata"]
  
    # Original Resource Name (ex: Speech and Document Understanding that create a second file)
    id_var = cur.var(oracledb.NUMBER)

    data = (
            "CHUNCKED",
            dictString(value,"applicationName"), 
            dictString(value,"author"),
            dictString(value,"translation"),
            # array.array("f", result["summaryEmbed"]),
            dictString(value,"contentType"),
            dictString(value,"creationDate"),
            dictString(value,"modified"),
            dictString(metadata, "gaas-metadata-filtering-field-category1"),
            dictString(metadata, "gaas-metadata-filtering-field-category2"),
            dictString(metadata, "gaas-metadata-filtering-field-category3"),
            dictString(value,"parsed_by"),
            resourceName,                               # resourceName that caused the event to be started (used for deletion, ex: mp3.json for speech) 
            dictString(metadata, "gaas-metadata-filtering-field-originalResourceName"), # originalResourceName (ex: mp3 filename for speech)
            value["metadata"]["customized_url_source"], # path
            title,         
            os.getenv("TF_VAR_region"),
            str(dictString(value,"summaryEmbed")),            
            dictString(value,"source_type"),
            dictString(value,"content"),
            dictString(value,"summary"),
            id_var
        )
    try:
        cur.execute(stmt, data)
        dbConn.commit()
        # Get generated id
        id = id_var.getvalue()    
        log("<insertTableDocs> returning id=" + str(id[0]) )        
        value["docId"] = id[0]
        log(f"<insertTableDocs> Successfully inserted {cur.rowcount} records.")
    except (Exception) as error:
        log(f"\u270B <insertTableDocs> Error inserting records: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if dbConn:
            pool.release(dbConn)

# -- insertTableDocsChunck -----------------------------------------------------------------

def insertTableDocsChunck(value, docs, file_path):  
    
    log("<langchain insertTableDocsChunck>")
    log("-- docs --------------------")
    log(pprint.pformat(docs))

    if value.get("content_markdown"):
        if DOCLING_HYBRID_CHUNK:
            # Advantage: preseve the page numbers / read images PDF
            # Disadvantage: slow
            chunck_loader = DoclingLoader(
                file_path=file_path,
                export_type=ExportType.DOC_CHUNKS,
                chunker=HybridChunker()
            )
            docs_chunck = chunck_loader.load()

            # Convert the docling metadata format
            for d in docs_chunck:
                # Prov format to page_label
                try:
                    d.metadata["page_label"] = d.metadata["dl_meta"]["doc_items"][0]["prov"][0]["page_no"]
                    # log(f"metadata page_label={d.metadata["page_label"]}")
                except (Exception) as e:
                    log(f"metadata page_label - Warning {e}")
                # Headers to something like MarkdownHeaderTextSplitter
                try:
                    if d.metadata["dl_meta"].get("hedings"):
                        for i, h in enumerate(d.metadata["dl_meta"]["headings"]):
                            d.metadata[f"Header_{i+1}"]=h        
                            # log(f"metadata Header_{i+1}={h}")
                except (Exception) as e:
                    log(f"metadata header - Warning {e}")
        else:
            # Advantage: fast
            splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[
                    ("#", "Header_1"),
                    ("##", "Header_2"),
                    ("###", "Header_3"),
                ],
            )
            docs_chunck = [split for doc in docs for split in splitter.split_text(doc.page_content)]
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)      
        docs_chunck = splitter.split_documents(docs)

    # There is no standard in Langchain chuncking on the metadata.
    for d in docs_chunck:
        d.metadata["doc_id"] = dictString(value,"docId")        
        d.metadata["resource_name"] = value["data"]["resourceName"]
        d.metadata["content_type"] = dictString(value,"contentType")
        d.metadata["path"] = value["metadata"]["customized_url_source"]
        # Copy OCI Agent Filters key
        for k, v in value["metadata"].items():
            if k.startswith( "gaas-metadata-filtering-field-" ):
                short_key = k.split("filtering-field-",1)[1]
                d.metadata[short_key] = v

    global pool
    dbConn = pool.acquire()                
    try:
        log("-- docs_chunck --------------------")  
        log(pprint.pformat( docs_chunck ))
        vectorstore = OracleVS( client=dbConn, table_name="docs_langchain", embedding_function=embeddings, distance_strategy=DistanceStrategy.DOT_PRODUCT )
        vectorstore.add_documents( docs_chunck )
        log("</langchain insertDocsChunck>")
    except (Exception) as error:
        log(f"\u270B <insertTableDocsChunck> Error vectorstore: {error}")
    finally:
        if dbConn:
            pool.release(dbConn)

# -- deleteDocByOriginalResourceName ------------------------------------------

def deleteDocByOriginalResourceName( value ):  
    global pool
    dbConn = pool.acquire()  
    cur = dbConn.cursor()
    originalResourceName = value["data"]["resourceName"]
    log(f"<deleteDocByOriginalResourceName> originalResourceName={originalResourceName}")

    # Delete the document record
    try:
        cur.execute("delete from docs where original_resource_name=:1", (originalResourceName,))
        dbConn.commit()
        log(f"<deleteDocByOriginalResourceName> docs: Successfully {cur.rowcount} deleted")
    except (Exception) as error:
        log(f"<deleteDocByOriginalResourceName> docs: Error deleting: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()

    # Delete from the table directly..
    cur = dbConn.cursor()
    stmt = "delete FROM docs_langchain WHERE JSON_VALUE(metadata,'$.originalResourceName')=:1"
    try:
        cur.execute(stmt, (originalResourceName,))
        dbConn.commit()
        log(f"<deleteDocByOriginalResourceName> docs_langchain: Successfully {cur.rowcount} deleted")
    except (Exception) as error:
        log(f"<deleteDocByOriginalResourceName> docs_langchain: Error deleting: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()    
        if dbConn:
            pool.release(dbConn)            

# -- deleteDocByPath --------------------------------------------------------

def deleteDocByPath( value ):  
    global pool
    dbConn = pool.acquire() 
    cur = dbConn.cursor()
    path =  value["metadata"]["customized_url_source"]
    log(f"<deleteDocByPath> path={path}")

    # Delete the document record
    try:
        cur.execute("delete from docs where path=:1", (path,))
        dbConn.commit()
        log(f"<deleteDocByPath> docs: Successfully {cur.rowcount} deleted")
    except (Exception) as error:
        log(f"<deleteDocByPath> docs: Error deleting: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()

    # Delete from the table directly..
    cur = dbConn.cursor()
    stmt = "delete FROM docs_langchain WHERE JSON_VALUE(metadata,'$.path')=:1"
    try:
        cur.execute(stmt, (path,))
        dbConn.commit()
        log(f"<deleteDocByPath> docs_langchain: Successfully {cur.rowcount} deleted")
    except (Exception) as error:
        log(f"<deleteDocByPath> docs_langchain: Error deleting: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close() 
        if dbConn:
            pool.release(dbConn)              

# -- queryDb ----------------------------------------------------------------

def queryDb( type, question, embed ):
    global pool
    dbConn = pool.acquire() 
    result = [] 
    try:
        cur = dbConn.cursor()
        about = "about("+question+")";
        if type=="search": 
            # Text search example
            query = """
            SELECT filename, path, TO_CHAR(content) content_char, content_type, region, page, summary, score(99) score FROM docs_chunck
            WHERE CONTAINS(content, :1, 99)>0 order by score(99) DESC FETCH FIRST 10 ROWS ONLY
            """
            cursor.execute(query,(about,))
        elif type=="semantic":
            query = """
            SELECT filename, path, TO_CHAR(content) content_char, content_type, region, page, summary, cohere_embed <=> :1 score FROM docs_chunck
                ORDER BY score FETCH FIRST 10 ROWS ONLY
            """
            cursor.execute(query,(array.array("f", embed),))
        else: # type in ["hybrid","rag"]:
            query = """
            WITH text_search AS (
                SELECT id, score(99)/100 as score FROM docs_chunck
                WHERE CONTAINS(content, :1, 99)>0 order by score(99) DESC FETCH FIRST 10 ROWS ONLY
            ),
            vector_search AS (
                SELECT id, cohere_embed <=> :2 AS vector_distance
                FROM docs_chunck
            )
            SELECT o.filename, o.path, TO_CHAR(content) content_char, o.content_type, o.region, o.page, o.summary,
                (0.3 * ts.score + 0.7 * (1 - vs.vector_distance)) AS score
            FROM docs_chunck o
            JOIN text_search ts ON o.id = ts.id
            JOIN vector_search vs ON o.id = vs.id
            ORDER BY score DESC
            FETCH FIRST 10 ROWS ONLY
            """
            cur.execute(query,(about,array.array("f", embed),))
    #        FULL OUTER JOIN text_search ts ON o.id = ts.id
    #        FULL OUTER JOIN vector_search vs ON o.id = vs.id
        rows = cur.fetchall()
        for row in rows:
            result.append( {"filename": row[0], "path": row[1], "content": str(row[2]), "contentType": row[3], "region": row[4], "page": row[5], "summary": str(row[6]), "score": row[7]} )  
        for r in result:
            log("filename="+r["filename"])
            log("content: "+r["content"][:150])
        return result
    except Exception as error:
        log(f"<queryDb> Exception: {error}")
        raise
    finally:
        # Close the cursor and connection
        if cur:
            cur.close() 
        if dbConn:
            pool.release(dbConn)              

# -- row2Dict -----------------------------------------------------------------------

def row2Dict( column_names, row ):
    processed_row = []
    for value in row:
        # log( f"fvalue {value} / type {type(value)}" )
        if isinstance(value, oracledb.LOB):
            # Convert Read LOB
            # log( "<row2Dict> Reading LOB")
            processed_row.append(value.read())
        else:
            # Keep everything else as is
            processed_row.append(str(value))
    # Manually map the row (tuple) to the column names
    row_dict = dict(zip(column_names, processed_row))
    return row_dict

# -- rasCreateSession ----------------------------------------------------------------------

def rasCreateSession( cur, auth_header ):
    if auth_header:
        plsql_block = """
        DECLARE 
            sessionid RAW(16); 
            username varchar2(1024);
        BEGIN
            username := ai_plsql.get_username_from_auth_header( :auth_header );
            SYS.DBMS_XS_SESSIONS.CREATE_SESSION(username, sessionid);
            SYS.DBMS_XS_SESSIONS.ATTACH_SESSION(sessionid);
            :sessionid := sessionid;
        END;
        """        
        sessionid_var = cur.var(oracledb.DB_TYPE_RAW, size=16)
        cur.execute(plsql_block, { ":auth_header": auth_header, ":sessionid": sessionid_var } )
        session_id_bytes = sessionid_var.getvalue()
        print("Session ID:", session_id_bytes.hex() if session_id_bytes else None)
        return session_id_bytes

# -- rasDestroySession ----------------------------------------------------------------------

def rasDestroySession( cur, auth_header, sessionid ):
    if auth_header:
        plsql_block = """
        BEGIN
            SYS.DBMS_XS_SESSIONS.DETACH_SESSION;
            SYS.DBMS_XS_SESSIONS.DESTROY_SESSION(:sessionid);
        END;
        """
        cur.execute(plsql_block, sessionid=sessionid)        

# -- queryFirstRecord ----------------------------------------------------------------------

def queryFirstRecord( query, params, auth_header=None ):
    log(f"<queryFirstRecord>")    
    global pool
    dbConn = pool.acquire() 
    cur = dbConn.cursor()
    result = [] 
    try:    
        sessionid = rasCreateSession( cur, auth_header )
        cur.execute(query,params)    
        column_names = [col[0] for col in cur.description]
        for row in cur.fetchall():
            result=row2Dict(column_names, row)
            log(pprint.pformat(result))   
            return result  
        log("<queryFirstRecord>Not found")    
        return {"error": "Not found"}   
    except Exception as error:
        log(f"<queryFirstRecord> Exception: {error}")
        raise
    finally:
        # Close the cursor and connection
        rasDestroySession( cur, auth_header, sessionid )
        if cur:
            cur.close() 
        if dbConn:
            pool.release(dbConn)  


# -- queryAllRecords ----------------------------------------------------------------------

def queryAllRecords( query, params, auth_header=None ):
    log(f"<queryAllRecords>")    
    global pool
    dbConn = pool.acquire() 
    cur = dbConn.cursor()
    result = [] 
    try:      
        sessionid = rasCreateSession( cur, auth_header )
        cur.execute(query,params)    
        result = []
        column_names = [col[0] for col in cur.description]
        for row in cur.fetchall():
            row_dict = row2Dict(column_names, row)
            result.append(row_dict)  
        log(pprint.pformat(result)) 
        return result 
    except Exception as error:
        log(f"<queryAllRecords> Exception: {error}")
        raise
    finally:
        # Close the cursor and connection
        rasDestroySession( cur, auth_header, sessionid )
        if cur:
            cur.close() 
        if dbConn:
            pool.release(dbConn)  

# -- getDocByPath ----------------------------------------------------------------------

def getDocByPath( path ):
    log(f"<getDocByPath> path={path}")    
    global pool
    dbConn = pool.acquire() 
    try:     
        query = "SELECT path, content, content_type, region, summary FROM docs WHERE path=:1"
        cur = dbConn.cursor()
        cur.execute(query,(path,))
        column_names = [col[0] for col in cur.description]
        for row in cur.fetchall():
            result=row2Dict(column_names, row)
            log(pprint.pformat(result))   
            return result  
        log("<getDocByPath>Docs not found by path: " + path)

        # Tries with the title
        query = "SELECT path, content, content_type, region, summary FROM docs WHERE title=:1"
        return queryFirstRecord( query, (path,))
    except Exception as error:
        log(f"<getDocByPath> Exception: {error}")
        raise
    finally:
        # Close the cursor and connection
        if cur:
            cur.close() 
        if dbConn:
            pool.release(dbConn)  
    

# -- getDocList ----------------------------------------------------------------------

def getDocList():
    log(f"<getDocList>")    
    query = "SELECT title, path FROM docs"
    return queryAllRecords( query, None )

# -- insertTableIngestLog -----------------------------------------------------------------

def insertTableIngestLog( p_status, p_resource_name, p_event_type, p_log_file_name, p_time_start, p_time_end, p_time_secs ):  
    if RAG_STORAGE!="db26ai":
        return

    global pool
    dbConn = pool.acquire() 
    cur = dbConn.cursor()

    log("<insertTableIngestLog>")
    # log(pprint.pformat(value))    
    # CLOB at the end (content, summary) to avoid BINDING error: ORA-24816: Expanded non LONG bind data supplied after actual LONG or LOB column
    try:
        stmt = """
            INSERT INTO ai_agent_rag_ingest_log (
                status, resource_name, event_type, content, time_start, time_end, time_secs
            )
            VALUES (:1, :2, :3, :4, :5, :6, :7)
            RETURNING id INTO :8
        """ 
        # Original Resource Name (ex: Speech and Document Understanding that create a second file)
        id_var = cur.var(oracledb.NUMBER)
        f = open(p_log_file_name)
        content = f.read()
        data = (
                p_status,
                p_resource_name,
                p_event_type.replace("com.oraclecloud.objectstorage.", ""), 
                content,
                p_time_start,
                p_time_end,
                p_time_secs,
                id_var
            )

        cur.execute(stmt, data)
        dbConn.commit()
        # Get generated id
        id = id_var.getvalue()    
        log("<insertTableIngestLog> returning id=" + str(id[0]) )        
        log(f"<insertTableIngestLog> Successfully inserted {cur.rowcount} records.")
        updateDocStatus( p_status, p_resource_name )
    except (Exception) as error:
        log(f"\u270B <insertTableIngestLog> Error inserting records: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if dbConn:
            pool.release(dbConn)              

# -- updateDocStatus -----------------------------------------------------------------

def updateDocStatus( p_status, p_resource_name ):  
    if RAG_STORAGE!="db26ai":
        return

    global pool
    dbConn = pool.acquire() 
    cur = dbConn.cursor()

    log("<updateDocStatus>")
    try:
        # Update files that are:
        # - Uploaded from APEX and of type .crawler, .selenium where original file was not replaced
        # - Status NEW, or OK -> 1 Error in 1 child resource will cause an ERROR in the parent 
        stmt = """
            UPDATE DOCS set status=:1 where resource_name=:2 and status in ('NEW','OK')
        """ 
        data = (
                p_status,
                p_resource_name
            )
        cur.execute(stmt, data)
        log(f"<updateDocStatus> Successfully updated {cur.rowcount} records.")
    except (Exception) as error:
        log(f"\u270B <updateDocStatus> Error updating records: {error}")
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if dbConn:
            pool.release(dbConn)                   

# -- 


# -- findServiceRequest -----------------------------------------------------------------

def findServiceRequest(question: str, auth_header: str) -> dict:
    log(f"<findServiceRequest> question={question} auth_header={auth_header}")   
    # query = """WITH text_search AS (
    #         SELECT id, score(99)/100 as score FROM support_sr
    #         WHERE CONTAINS(question, :1, 99)>0 order by score(99) DESC FETCH FIRST 10 ROWS ONLY
    #     ),
    #     vector_search AS (

    #         SELECT id, vector_distance(embedding, to_vector(ai_plsql.genai_embed( :2 ))) AS vector_distance
    #         FROM support_sr
    #     )
    #     SELECT o.ID, o.SUBJECT, o.QUESTION, o.ANSWER 
    #     from SUPPORT_SR o
    #     JOIN text_search ts ON o.id = ts.id
    #     JOIN vector_search vs ON o.id = vs.id
    #     ORDER BY score DESC
    #     FETCH FIRST 10 ROWS ONLY;"""    
    query = f"""
            SELECT id, vector_distance(embedding, to_vector(ai_plsql.genai_embed( :1 ))) AS score, '{ORDS_EXTERNAL_URL}/r/apex_app/ai_support/support-sr?p2_id='||id DEEPLINK, o.SUBJECT, o.QUESTION, o.ANSWER 
            FROM support_sr o
            ORDER BY score ASC
            FETCH FIRST 10 ROWS ONLY"""    
    return queryAllRecords( query, (question, ),auth_header)


# -- getDocByPath ----------------------------------------------------------------------

def getServiceRequest( id, auth_header ):
    log(f"<getServiceRequest> id={id} auth_header={auth_header}")    
    query = f"select ID, '{ORDS_EXTERNAL_URL}/r/apex_app/ai_support/support-sr?p2_id='||id DEEPLINK, SUBJECT, QUESTION, ANSWER from SUPPORT_SR where id=:1"
    return queryFirstRecord( query, (id,), auth_header)
  
  # https://xxxxx/ords/r/apex_app/ai_support/support-sr?p2_id={id}