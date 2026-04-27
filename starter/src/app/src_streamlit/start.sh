#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
export PATH=~/.local/bin/:$PATH

. $HOME/compute/tf_env.sh

# User Interface with Streamlit
source myenv/bin/activate
streamlit run streamlit.py --server.port 8080 2>&1 | tee streamlit.log

# Ex: curl "http://$BASTION_IP:8080/"