#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

if [ -f shared_compute.sh ]; then
  # Docker mode
  . ./shared_compute.sh
  export TF_VAR_java_vm="jdk"
  # Do not install LibreOffice, the dependency makes the DockerImage 18GB
  export INSTALL_LIBREOFFICE="no"
fi

install_sqlcl
. ./env.sh INSTALL
livelab_oci_config

function download()
{
   echo "Downloading - $1"
   wget -nv $1
}

# Anonymize
sudo dnf install -y poppler-utils mesa-libGL

# Python 
install_python

# PDFKIT
if [ ! -f /tmp/wkhtmltox-0.12.6-1.centos8.x86_64.rpm ]; then
    download https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.centos8.x86_64.rpm 
    sudo dnf localinstall -y wkhtmltox-0.12.6-1.centos8.x86_64.rpm
    mv *.rpm /tmp
fi

# LibreOffice (convert docx to PDF)
if [ "${INSTALL_LIBREOFFICE}" != "no" ]; then
    install_libreoffice
    # Chrome + Selenium to get webpage
    install_chrome
fi 
cd $SCRIPT_DIR

# Java
install_java

# Vector Store
if [ "$TF_VAR_rag_storage" == "vector_store" ]; then
    if [ -f responses_env.sh ]; then
        cat "File responses_env.sh exists already."
    else 
        echo "Vector Store"
        source myenv/bin/activate
        python src/create_vector_store.py
        exit_on_error "create_vector_store.py failed"

        . ./resource_env.sh
        # Store the config in APEX
        export TNS_ADMIN=$HOME/db
        $HOME/db/sqlcl/bin/sql APEX_APP/$DB_PASSWORD@DB <<EOF
begin
    AI_CONFIG_UPDATE( 'vector_store_id', '$VECTOR_STORE_ID' );
end;
/
exit;
EOF

    fi
fi    

# Build Tika
cd src/tika
sudo dnf install -y maven
mvn package
cd -
