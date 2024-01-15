#!/bin/bash

if [ $# -ne 1 ]
then
        echo "Your forgot an package for install"
        echo "Syntax: ./exitcodes.sh package"
        exit 1
else
package=$1

sudo apt install $package >> package_install_results.log

if [ $? -eq 0 ]
then
        echo "The installation of $package was successful."
        echo "The new command is available here:"
        which $package
else
        echo "$package failed to install." >> package_install_failure.log
fi
fi
