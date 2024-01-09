#!/bin/bash

program=$1

if  command -v $program  # [ -f $program ] // /user/bin/$program
then
        echo "$program is available, let's run it..."
else
        echo "$program is NOT available, installing it..."
        sudo apt update && sudo apt install -y $program
fi

$program
