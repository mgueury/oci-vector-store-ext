. $HOME/compute/tf_env.sh

export DB_USER="apex_app"

# LangFuse
# export LANGFUSE_PUBLIC_KEY=<your_public_key>
# export LANGFUSE_SECRET_KEY=<your_secret_key>
export LANGFUSE_HOST=http://localhost:3000


# export LANGSMITH_TRACING=true
# export LANGSMITH_TRACING=true
# export LANGSMITH_API_KEY=<your-api-key>
# export LANGSMITH_WORKSPACE_ID=agext

# Python VirtualEnv
if [ -d myenv ]; then
  source myenv/bin/activate
fi

# Responses
if [ -f $HOME/app/ingest/responses_env.sh ]; then
    . $HOME/app/ingest/responses_env.sh
fi 

# TNS_ADMIN
export TNS_ADMIN=$HOME/db

# During Initialisation - Store the env db in the database
# After Initialisation  - Use the env stored in the database as source of True
# Read Variables in database 
if [ "$1" != "INSTALL" ]; then
  if [ "$DB_URL" != "" ]; then
    $HOME/db/sqlcl/bin/sql $DB_USER/$DB_PASSWORD@DB <<EOF
      set linesize 1000
      set heading off
      set feedback off
      set echo off
      set verify off  
      spool /tmp/config.env
      select 'export TF_VAR_' || key || '="' || value || '"' from APEX_APP.AI_AGENT_RAG_CONFIG;
      spool off
EOF
  fi

  while read line; do
    if [ "$line" != "" ]; then
      eval $line
    fi
  done </tmp/config.env
  rm /tmp/config.env
fi

