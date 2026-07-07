#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

cd ../../..
cp -R oci-genai-agent-ext rm-genai-agent-ext
cd 
rm -Rf rm-genai-agent-ext/starter/terraform/.terraform*
rm -Rf rm-genai-agent-ext/starter/terraform/old
rm -Rf rm-genai-agent-ext/starter/terraform/_tf
rm -Rf rm-genai-agent-ext/starter/target

echo "NEXT STEPS"
echo "cd rm-genai-agent-ext/starter"
echo "./starter.sh rm create"
echo "./starter.sh rm build"