# Import
import oci
import os
import json 
import datetime
import time
import traceback
import shared
from shared import log
from shared import shared_config
from shared import shared_signer
from shared import log_write_in_file
from shared import log_in_file
from shared import UNIQUE_ID
import rag_storage
import document

from datetime import datetime, timezone
from base64 import b64decode

## -- Globals --------------------------------------------------------------

updateList = {} # Dictionary of parsed files
updateCount = 0

## -- stream_cursor --------------------------------------------------------

def stream_cursor(sc, sid, group_name, instance_name):
    log("<stream_cursor>")
    cursor_details = oci.streaming.models.CreateGroupCursorDetails(group_name=group_name, instance_name=instance_name,
                                                                   type=oci.streaming.models.
                                                                   CreateGroupCursorDetails.TYPE_TRIM_HORIZON,
                                                                   commit_on_get=True)
    response = sc.create_group_cursor(sid, cursor_details)
    return response.data.value

## -- stream_loop --------------------------------------------------------

def stream_loop(client, stream_id, initial_cursor):
    global UNIQUE_ID
    global updateList
    global updateCount        
    updateCount = 0
    cursor = initial_cursor

    while True:
        get_response = client.get_messages(stream_id, cursor, limit=10)
        # No messages to process. return.
        if not get_response.data:
            updateList = {}
            rag_storage.updateCount( updateCount )
            return
        # Process the messages
        log("<stream_loop> Read {} messages".format(len(get_response.data)))
        for message in get_response.data:
            timeStart = datetime.now()
            updateCount += 1
            status = 'PROCESSING'
            try:
                log_file_name = shared.getLogDir() + f"/message_{timeStart.strftime("%Y_%m_%d_%H_%M_%S_%f")}.log"
                log_write_in_file(log_file_name)
                log(f"\n\n-- STREAM LOOP - MESSAGE {updateCount} -----------------------------------------------------------------------------------------" )
                if message.key is None:
                    key = "Null"
                else:
                    key = b64decode(message.key.encode()).decode()
                json_value = b64decode(message.value.encode()).decode(); 
                log(json_value)

                shared.UNIQUE_ID = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
                log_in_file("stream", json_value)
                value = json.loads(json_value)

                # Check if that resourceName was parsed already once in this stream_loop (and if yes, if before or after the received event)
                resourceName = value["data"]["resourceName"] 
                eventTime = value["eventTime"] 
                eventType = value["eventType"]
                if eventType in ["com.oraclecloud.objectstorage.createobject", "com.oraclecloud.objectstorage.updateobject"]:
                    parsed_datetime_naive = datetime.strptime(eventTime.rstrip('Z'), '%Y-%m-%dT%H:%M:%S')
                    eventTime_utc = parsed_datetime_naive.replace(tzinfo=timezone.utc)
                    if updateList.get(resourceName):
                        if eventTime_utc<updateList.get(resourceName):
                            log(f"\u2705 {resourceName} Skipped - Parsed at {updateList.get(resourceName)} after event {eventTime_utc}")
                            status = 'SKIPPED'
                            continue
                        else:
                            log(f"<stream_loop>{resourceName} Modified after last parsing. {updateList.get(resourceName)} before event {eventTime_utc}")
                    else:
                        log(f"<stream_loop>{resourceName}")
                    # Not parsed yet or update after the last parsing   
                    updateList[resourceName]=datetime.now(timezone.utc)
                
                # DEBUG
                # for k, v in updateList.items():
                #    log(f"updateList - {k} - {v}")
                document.eventDocument(value)
                log( f"\u2705 {resourceName}")     
                status = 'DONE'             
            except:
                log( f"\u274C Exception: stream_loop") 
                log( traceback.format_exc())
                status = 'ERROR'             
            timeEnd = datetime.now()
            timeDiff = timeEnd - timeStart # Result is of timedelta type
            timeSecs = timeDiff.total_seconds()
            log(f"Time: {timeSecs} secs")
            rag_storage.insertTableIngestLog( status, resourceName, eventType, log_file_name, timeStart, timeEnd, timeSecs )                
            log_write_in_file(None)                
                
        log("<stream_loop> Processed {} messages".format(len(get_response.data)))        
            
        # get_messages is a throttled method; clients should retrieve sufficiently large message
        # batches, as to avoid too many http requests.
        time.sleep(1)
        # use the next-cursor for iteration
        cursor = get_response.headers["opc-next-cursor"]

## -- main ------------------------------------------------------------------

ociMessageEndpoint = os.getenv('STREAM_MESSAGE_ENDPOINT')
ociStreamOcid = os.getenv('STREAM_OCID')

stream_client = oci.streaming.StreamClient(config=shared_config, service_endpoint=ociMessageEndpoint, signer=shared_signer)
while True:
    try:
        while True:
            rag_storage.init()
            group_cursor = stream_cursor(stream_client, ociStreamOcid, "app-group", "app-instance-1")
            stream_loop(stream_client, ociStreamOcid, group_cursor)
            rag_storage.close()
            time.sleep(30)
    except:
        log("----------------------------------------------------------------------------")
        log("\u274C <main>Exception in streamloop")
        log(traceback.format_exc())
        # Resetting Stream - This is needed when you have the cursor that is too old (5 mins without using it) 
        # Error: 400 - The cursor is outside the retention period and is now invalid.
        # Some message will be lost. Trim_horizon take the oldest one.
        # update_group_response = stream_client.update_group(
        #     stream_id=ociStreamOcid,
        #     group_name="app-group",
        #     update_group_details=oci.streaming.models.UpdateGroupDetails(type="TRIM_HORIZON"))
