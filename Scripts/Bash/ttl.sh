#!/bin/bash

if [ $# -ne 1 ]
then
        echo "You forgot an IP address"
        echo "Syntax: ./ttl.sh <ip-address>"
        exit 1
else
        ttl=$(ping -c 1 $1 | grep "64 bytes" | cut -d " " -f 6 | tr -d "ttl=")

        if [[ $ttl -ge 0 && $ttl -le 64 ]]
        then
                echo "Linux"
        elif [[ $ttl -gt 64 && $ttl -le 128 ]]
        then
                echo "Windows"
        else
                echo "System Not Found"
        fi
fi 
