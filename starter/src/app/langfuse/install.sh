#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

. $HOME/compute/shared_compute.sh

# Podman and GIT
install_docker_tools

# LangFuse Source
git clone https://github.com/langfuse/langfuse.git

# Podman-compose
python -m pip install --user podman-compose

# Firewall 
sudo firewall-cmd --zone=public --add-port=3000/tcp --permanent
