#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "[usage] cli_demo.sh <entity manifest path> <entity uuid>"
    exit -1
fi

CLI=/Users/gabri/Workspace/fos-agent-ng/_build/default/src/fos/fos-cli-ng/fos_cli_ng.exe

IU=$(uuidgen)

printf "\nNode list - fos-cli-ng node list"

$CLI node list

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nOnboard entity - fos-cli-ng entity onboard -m $1\n"

$CLI entity onboard -m $1

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nOffload entity - fos-cli-ng entity offload --eu $2\n"

$CLI entity offload --eu $2

read -n 1 -s -r -p "Press any key to exit"
printf "\n"