#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

. ./tf_env.sh
. ./shared_compute.sh

# Install SQLCL
install_sqlcl

# Install SQL*Plus / SQL*Loader
install_instant_client

# Create the script to install the APEX Application
cat > import_application.sql << EOF 
create user if not exists apex_app identified by "$DB_PASSWORD" default tablespace USERS quota unlimited on USERS temporary tablespace TEMP; 
/
grant connect, resource, create role, unlimited tablespace to apex_app;
/
EXEC DBMS_CLOUD_ADMIN.ENABLE_RESOURCE_PRINCIPAL('APEX_APP');
grant execute on DBMS_CLOUD to APEX_APP;
grant execute on DBMS_CLOUD_AI to APEX_APP;
grant execute on CTX_DDL to APEX_APP;
grant execute on DBMS_SCHEDULER to APEX_APP;
grant create any job to APEX_APP;
/
-- Work-around for ADB SSO bug
begin
  apex_instance_admin.set_parameter(
    'APEX_BUILDER_AUTHENTICATION', 'DB');
  commit;
end;
/
begin
    apex_instance_admin.add_workspace(
     p_workspace_id   => null,
     p_workspace      => 'APEX_APP',
     p_primary_schema => 'APEX_APP');
end;
/
begin
    apex_application_install.set_workspace('APEX_APP');
    apex_application_install.set_application_id(1001);
    apex_application_install.generate_offset();
    apex_application_install.set_schema('APEX_APP');
    apex_application_install.set_auto_install_sup_obj( true );
end;
/
declare
    l_workspace_id number;
begin
    apex_application_install.set_workspace('APEX_APP');
    l_workspace_id := apex_util.find_security_group_id('APEX_APP');
    apex_util.set_security_group_id(l_workspace_id);
    apex_util.create_user(p_user_name           => 'APEX_APP',
                        p_email_address         => 'spam@oracle.com',
                        p_web_password          => '$DB_PASSWORD',
                        p_default_schema        => 'APEX_APP',
                        p_change_password_on_first_use => 'N',
                        p_developer_privs       => 'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',
                        p_allow_app_building_yn => 'Y',
                        p_allow_sql_workshop_yn => 'Y',
                        p_allow_websheet_dev_yn => 'Y',
                        p_allow_team_development_yn => 'Y');                          
    COMMIT;                      
end;
/
@ai_agent_rag.sql
/
begin
    apex_application_install.set_application_id(1002);
end;
/
@ai_agent_rag_admin.sql
/
begin
    apex_application_install.set_application_id(1003);
end;
/
@ai_agent_eval.sql
begin
    apex_application_install.set_application_id(1004);
end;
/
@ai_support.sql
quit
EOF

sqlcl/bin/sql ADMIN/$DB_PASSWORD@DB @import_application.sql

# Install DocChunks 
sqlcl/bin/sql ADMIN/$DB_PASSWORD@DB @doc_chunck.sql

# Install SR for SQL agent
cat > support_table.sql << EOF 
CREATE TABLE SUPPORT_OWNER (
    id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(20)
);

CREATE TABLE SUPPORT_SR (
    id NUMBER PRIMARY KEY,
    customer_name VARCHAR2(200) NOT NULL,
    subject VARCHAR2(200) NOT NULL,
    question CLOB NOT NULL,
    answer CLOB NOT NULL,
    create_date DATE DEFAULT SYSTIMESTAMP NOT NULL,
    last_update_date DATE DEFAULT SYSTIMESTAMP NOT NULL,
    owner_id NUMBER,
    embedding VECTOR,
    internal NUMBER,
    CONSTRAINT FK_SUPPORT_OWNER 
       FOREIGN KEY (owner_id) 
       REFERENCES SUPPORT_OWNER(id)
);
exit;
EOF

# Store the config in APEX
sqlcl/bin/sql APEX_APP/$DB_PASSWORD@DB <<EOF
begin
  AI_CONFIG_UPDATE( 'agent_endpoint_ocid', '$TF_VAR_agent_endpoint_ocid' );
  AI_CONFIG_UPDATE( 'project_ocid',        '$TF_VAR_project_ocid' );
  AI_CONFIG_UPDATE( 'vector_store',        '$VECTOR_STORE' );
  AI_CONFIG_UPDATE( 'rag_storage',         '$TF_VAR_rag_storage' );
  AI_CONFIG_UPDATE( 'responses_model_id',  '$TF_VAR_responses_model_id' );  
  AI_CONFIG_UPDATE( 'region',              '$TF_VAR_region' );
  AI_CONFIG_UPDATE( 'compartment_ocid',    '$TF_VAR_compartment_ocid' );
  AI_CONFIG_UPDATE( 'genai_embed_model',   '$TF_VAR_genai_embed_model' );
  AI_CONFIG_UPDATE( 'genai_cohere_model',  '$TF_VAR_genai_cohere_model' );
  AI_CONFIG_UPDATE( 'bucket_url',          '$BUCKET_URL' );
  AI_CONFIG_UPDATE( 'rag_search_type',     'vector' );
  -- AI_EVAL
  AI_CONFIG_UPDATE( 'qa_url',              'https://$APIGW_HOSTNAME/$TF_VAR_prefix/langgraph/runs/wait' );
  AI_CONFIG_UPDATE( 'genai_meta_model',    '$TF_VAR_genai_meta_model' );
  -- AI_LANGGRAPH
  AI_CONFIG_UPDATE( 'langgraph_thread_url', 'https://$APIGW_HOSTNAME/$TF_VAR_prefix/langgraph/threads' );
  AI_CONFIG_UPDATE( 'idcs_url', '$IDCS_URL' );
  -- ORCL_DB_SSE
  -- AI_CONFIG_UPDATE( 'langgraph_startsse_url', 'https://$APIGW_HOSTNAME/$TF_VAR_prefix/orcldbsse/startsse?thread_id=' );
  commit;
end;
/
exit;
EOF

# Support table
sqlcl/bin/sql APEX_APP/$DB_PASSWORD@DB @support_table.sql

# Import the tables
/usr/lib/oracle/23/client64/bin/sqlldr APEX_APP/$DB_PASSWORD@DB CONTROL=support_owner.ctl
/usr/lib/oracle/23/client64/bin/sqlldr APEX_APP/$DB_PASSWORD@DB CONTROL=support_sr.ctl
/usr/lib/oracle/23/client64/bin/sqlldr APEX_APP/$DB_PASSWORD@DB CONTROL=ai_eval_question_answer.ctl

sqlcl/bin/sql $DB_USER/$DB_PASSWORD@DB @ras_admin.sql
sqlcl/bin/sql APEX_APP/$DB_PASSWORD@DB @ras_apex_app.sql

if [ "$TF_VAR_orcl_db_sse" == "true" ]; then

# ORCL_DB_SSE (Micronaut)
cat > orcl_db_sse.sql << EOF 
CREATE TABLE SSE_EVENTS (
  ID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY, 
  SSE_ID VARCHAR2(200),
  THREAD_ID VARCHAR2(200),
  EVENT_ORDER NUMBER,
  EVENT_NAME VARCHAR2(200),
  TYPE VARCHAR2(200),
  NAME VARCHAR2(1024),
  FINISH_REASON VARCHAR2(200),
  CREATEDATE TIMESTAMP,
  DATA_CONTENT CLOB,
  HTML_CONTENT CLOB,
  FULL_DATA CLOB
);
CREATE INDEX IDX_SSE_EVENTS_THREAD ON SSE_EVENTS(THREAD_ID);

CREATE TABLE SSE_DATA (
  ID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
  CREATEDATE TIMESTAMP
  THREAD_ID VARCHAR2(200),
  EVENT_ID VARCHAR2(200),
  EVENT_NAME VARCHAR2(200),
  EVENT_DATA CLOB,
);

CREATE INDEX IDX_SSE_DATA_THREAD ON SSE_DATA(THREAD_ID);
EOF

sqlcl/bin/sql APEX_APP/$DB_PASSWORD@DB @orcl_db_sse.sql

fi