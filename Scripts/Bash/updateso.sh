#!/bin/bash

release_file=/etc/os-release
logfile=/var/log/updater.log
errorlog=/var/log/updater_error.log

check_exit_status() {
        if [ $? -ne 0 ] # -ne -> not equal
        then
                echo "An error ocurred, please check the $errorlog file."
        fi
}

if grep -q "Arch" $release_file
then
        # The host is based on Arch, run the pacman update command
        sudo pacman -Syu 1>>$logfile 2>>$errorlog # Redirect - 1 exit standar / 2 error standar
        check_exit_status
fi

if grep -q "Pop" $release_file || grep -q "Ubuntu" $release_file
then
        # The host is based on Debian or Ubuntu,
        # Run the apt version of the command
        sudo apt update 1>>$logfile 2>>$errorlog
        check_exit_status

        sudo apt dist-upgrade -y 1>>$logfile 2>>$errorlog
        check_exit_status
fi

if grep -q "Kali" $release_file
then
        # Run the apt version of the command
        sudo apt update 1>>$logfile 2>>$errorlog
        check_exit_status

        sudo apt full-upgrade -y 1>>$logfile 2>>$errorlog
        check_exit_status
fi