#!/bin/bash

VERSION=$(rpm -q --qf '%{VERSION}' centos-release)

if [ $VERSION -eq 6 ]; then
    reboot="sudo /sbin/shutdown -r +1";
elif [ $VERSION -eq 7 ]; then
  reboot="sudo /usr/sbin/shutdown -r +1";
else
  echo "OS not found" >&2
  exit 1
fi

eval $reboot
