#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

java -jar tika/target/docparser-1.0.0-jar-with-dependencies.jar "$@"