#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "[usage] cli_demo.sh <node id> <manifest path> <atomic entity uuid>"
    exit -1
fi

CLI=/Users/gabri/Workspace/fos-agent-ng/_build/default/src/fos/fos-cli-ng/fos_cli_ng.exe

IU=$(uuidgen)

printf "\nNode list - fos-cli-ng node list\n"

$CLI node list

read -n 1 -s -r -p "Press any key to continue"
printf "\n"
printf "\nNode plugin - fos-cli-ng plugin list --nu $1\n"

$CLI plugin list --nu $1

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nDefine atomic entity - fos-cli-ng entity define --nu $1 -m $2\n"

$CLI entity define --nu $1 -m $2

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nConfigure atomic entity - fos-cli-ng entity configure --nu $1 --eu $3 --iu $IU\n"

$CLI entity configure --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nRun atomic entity - fos-cli-ng entity run --nu $1 --eu $3 --iu $IU\n"

$CLI entity run --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nStop atomic entity - fos-cli-ng entity stop --nu $1 --eu $3 --iu $IU\n"

$CLI entity stop --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nClean entity- fos-cli-ng entity clean --nu $1 --eu $3 --iu $IU\n"

$CLI entity clean --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"
printf "\n"

printf "\nUndefine atomic entity - fos-cli-ng entity undefine --nu $1 --eu $3\n"

$CLI entity undefine --nu $1 --eu $3

read -n 1 -s -r -p "Press any key to exit"
printf "\n"