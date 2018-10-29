#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "[usage] cli_demo.sh <node id> <manifest path> <atomic entity uuid>"
    exit -1
fi

CLI=/Users/gabri/Workspace/fos-agent-ng/_build/default/src/fos/fos-cli-ng/fos_cli_ng.exe

IU=$(uuidgen)

printf "\nNode list - fos-cli-ng node list"

$CLI node list

read -n 1 -s -r -p "Press any key to continue"

printf "\nNode plugin - fos-cli-ng plugin list --nu $1"

$CLI plugin list --nu $1

read -n 1 -s -r -p "Press any key to continue"

printf "\nDefine entity - fos-cli-ng entity define --nu $1 -m $2"

$CLI entity define --nu $1 -m $2

read -n 1 -s -r -p "Press any key to continue"


printf "\Configure entity- fos-cli-ng entity configure --nu $1 --eu $3 --iu $IU"

$CLI entity configure --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"

printf "\Run entity- fos-cli-ng entity run --nu $1 --eu $3 --iu $IU"

$CLI entity run --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"

printf "\Stop entity- fos-cli-ng entity stop --nu $1 --eu $3 --iu $IU"

$CLI entity stop --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"

printf "\Clean entity- fos-cli-ng entity clean --nu $1 --eu $3 --iu $IU"

$CLI entity clean --nu $1 --eu $3 --iu $IU

read -n 1 -s -r -p "Press any key to continue"

printf "\Undefine entity- fos-cli-ng entity undefine --nu $1 --eu $3"

$CLI entity undefine --nu $1 --eu $3

read -n 1 -s -r -p "Press any key to continue"