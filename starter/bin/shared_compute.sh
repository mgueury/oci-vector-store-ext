# -- Shared Compute Functions ------------------------------------------------

title() {
  line='-------------------------------------------------------------------------'
  NAME=$1
  echo
  echo "-- $NAME ${line:${#NAME}}"
  echo  
}
export -f title

install_java() {
  # Install the JVM (jdk or graalvm)
  if [ "$TF_VAR_java_vm" != "jdk" ]; then
    if grep -q 'export JAVA_HOME' $HOME/.bashrc; then
      echo "Java already installed " 
      return
    fi
    # GraalVM
    if [ "$TF_VAR_java_version" == 8 ]; then
      sudo dnf install -y graalvm21-ee-8-jdk 
      export JAVA_HOME=/usr/lib64/graalvm/graalvm22-ee-java8
    elif [ "$TF_VAR_java_version" == 11 ]; then
      sudo dnf install -y graalvm22-ee-11-jdk
      export JAVA_HOME=/usr/lib64/graalvm/graalvm22-ee-java11
    elif [ "$TF_VAR_java_version" == 17 ]; then
      sudo dnf install -y graalvm22-ee-17-jdk 
      export JAVA_HOME=/usr/lib64/graalvm/graalvm22-ee-java17
    elif [ "$TF_VAR_java_version" == 21 ]; then
      sudo dnf install -y graalvm-21-jdk
      export JAVA_HOME=/usr/lib64/graalvm/graalvm-java21
    else
      sudo dnf install -y graalvm-25-jdk
      export JAVA_HOME=/usr/lib64/graalvm/graalvm-java25    
      # sudo update-alternatives --set native-image $JAVA_HOME/lib/svm/bin/native-image
    fi   
    sudo update-alternatives --set java $JAVA_HOME/bin/java
    echo "export JAVA_HOME=${JAVA_HOME}" >> $HOME/.bashrc
  else
    # JDK 
    # Needed due to concurrency
    sudo dnf install -y alsa-lib 
    if [ "$TF_VAR_java_version" == 8 ]; then
      sudo dnf install -y java-1.8.0-openjdk
    elif [ "$TF_VAR_java_version" == 11 ]; then
      sudo dnf install -y java-11  
    elif [ "$TF_VAR_java_version" == 17 ]; then
      sudo dnf install -y java-17        
    elif [ "$TF_VAR_java_version" == 21 ]; then
      sudo dnf install -y java-21         
    else
      sudo dnf install -y java-25  
      # Trick to find the path
      # cd -P "/usr/java/latest"
      # export JAVA_LATEST_PATH=`pwd`
      # cd -
      # sudo update-alternatives --set java $JAVA_LATEST_PATH/bin/java
    fi
  fi

  # JMS agent deploy (to fleet_ocid )
  if [ -f jms_agent_deploy.sh ]; then
    chmod +x jms_agent_deploy.sh
    sudo ./jms_agent_deploy.sh
  fi
}
export -f install_java

# Install tnsnames.ora
install_tnsname() {
    # Run SQLCl
    # Install the tables
    export TNS_ADMIN=$HOME/db
    mkdir -p $TNS_ADMIN
    cat > $TNS_ADMIN/tnsnames.ora <<EOT
DB = $DB_URL
EOT
}
export -f install_tnsname

# Download
function download()
{
   echo "Downloading - $1"
   wget -nv $1
}
export -f download

# Install SQLCL 
install_sqlcl() {
    install_java
    install_tnsname
    cd $HOME/db
    if [ ! -f sqlcl-latest.zip ]; then
        download https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip
        rm -Rf sqlcl
        unzip sqlcl-latest.zip
    fi 
    cd -
}  
export -f install_sqlcl

# Install Python
install_python() {
    sudo dnf install -y python3.12 python3.12-pip python3-devel wget
    sudo update-alternatives --set python /usr/bin/python3.12
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH=$HOME/.local/bin:$PATH
    uv venv myenv
    source myenv/bin/activate
    if [ -f requirements.txt ]; then 
      uv pip install -r requirements.txt
    elif [ -f src/requirements.txt ]; then 
      uv pip install -r src/requirements.txt
    fi 
}
export -f install_python

# Install LibreOffice
install_libreoffice() {
    export STABLE_VERSIONS=`curl -s https://download.documentfoundation.org/libreoffice/stable/`
    # export LIBREOFFICE_VERSION=`echo $STABLE_VERSIONS | sed 's/.*<td valign="top">//' | sed 's/\/<\/a>.*//' | sed 's/.*\/">//'`
    # Version 26.2 is incompatible with RHEL8...
    export LIBREOFFICE_VERSION=`echo $STABLE_VERSIONS | sed 's/.*>25.8/25.8/' | sed 's/\/<\/a>.*//' | sed 's/.*\/">//'`
    echo LIBREOFFICE_VERSION=$LIBREOFFICE_VERSION
    cd /tmp
    export LIBREOFFICE_TGZ="LibreOffice_${LIBREOFFICE_VERSION}_Linux_x86-64_rpm.tar.gz"
    if [ ! -f $LIBREOFFICE_TGZ ]; then
        sudo dnf group install -y "Server with GUI"

        download https://download.documentfoundation.org/libreoffice/stable/${LIBREOFFICE_VERSION}/rpm/x86_64/$LIBREOFFICE_TGZ
        tar -xzvf $LIBREOFFICE_TGZ
        cd LibreOffice*/RPMS
        sudo dnf install *.rpm -y
    fi 
    export LIBRE_OFFICE_EXE=`find ${PATH//:/ } -maxdepth 1 -executable -name 'libreoffice*' | grep "libreoffice"`
    echo LIBRE_OFFICE_EXE=$LIBRE_OFFICE_EXE
    cd -
} 
export -f install_libreoffice   

# Install Chrome
install_chrome() {
    cd /tmp
    export CHROME_RPM="google-chrome-stable_current_x86_64.rpm"
    if [ ! -f $CHROME_RPM ]; then
      cd /tmp
      download https://dl.google.com/linux/direct/$CHROME_RPM
      sudo dnf localinstall -y $CHROME_RPM
    fi
    cd -
} 
export -f install_chrome   

# Install InstantClient (including SqlPlus)
install_instant_client() {
    install_tnsname

    # Install SQL*InstantClient
    if [[ `arch` == "aarch64" ]]; then
        sudo dnf install -y oracle-release-el8 
        sudo dnf install -y oracle-instantclient19.19-basic oracle-instantclient19.19-sqlplus oracle-instantclient19.19-tools
    else
        export INSTANT_VERSION=23.26.0.0.0-1
        cd /tmp
        if [ ! -f /tmp/oracle-instantclient-basic-${INSTANT_VERSION}.el8.x86_64.rpm ]; then
            wget -nv https://download.oracle.com/otn_software/linux/instantclient/2326000/oracle-instantclient-basic-${INSTANT_VERSION}.el8.x86_64.rpm
            wget -nv https://download.oracle.com/otn_software/linux/instantclient/2326000/oracle-instantclient-sqlplus-${INSTANT_VERSION}.el8.x86_64.rpm
            wget -nv https://download.oracle.com/otn_software/linux/instantclient/2326000/oracle-instantclient-tools-${INSTANT_VERSION}.el8.x86_64.rpm
            sudo dnf install -y oracle-instantclient-basic-${INSTANT_VERSION}.el8.x86_64.rpm oracle-instantclient-sqlplus-${INSTANT_VERSION}.el8.x86_64.rpm oracle-instantclient-tools-${INSTANT_VERSION}.el8.x86_64.rpm
        fi 
        cd -
    fi
}
export -f install_instant_client   

# Create a OCI Config for LiveLab (that does not support instance principal)
livelab_oci_config()
{  
   if [ "$LIVELABS" != "" ]; then
     mkdir -p $HOME/.oci

     # OCI Config file
     cat > $HOME/.oci/config << EOF
[DEFAULT]
user=$TF_VAR_current_user_ocid
fingerprint=$FINGERPRINT
tenancy=$TF_VAR_tenancy_ocid
region=$TF_VAR_region
key_file=/home/opc/.oci/oci_api_key.pem
EOF
     echo "livelab_oci_config: .oci/config created"

     # oci_api_key.pem
     cat > $HOME/.oci/oci_api_key.pem << EOF
$OCI_API_KEY_PEM
OCI_API_KEY

EOF
    chmod 600 $HOME/.oci/config
    chmod 600 $HOME/.oci/oci_api_key.pem
  fi 
}
export -f livelab_oci_config  
