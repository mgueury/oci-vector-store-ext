#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

. $HOME/compute/shared_compute.sh

# Python 
install_python

# Langgraph
sudo firewall-cmd --zone=public --add-port=2024/tcp --permanent

