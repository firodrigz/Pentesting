#!/bin/bash

# Operation only for IPV4 addresses.
# Designed to analyze all 255 hosts by scanning to detect "active" IPs. 
# Requires the entry of the first 3 octets belonging to the network portion

if [ $# -ne 1 ]
then
echo "You forgot an IP address"
echo "Syntax: ./ipsweep.sh 10.0.2"
exit 1
else
for ip in `seq 1 254`; do 
ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &
done
fi