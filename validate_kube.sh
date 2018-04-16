#!/bin/bash

VERSION=$(rpm -q --qf '%{VERSION}' centos-release)
ERR=3
MAX_TRIES=5
COUNT=0
SLEEPTIME=@option.sleeptime@
SVC_NAME=@option.servicename@

if [ $VERSION -eq 6 ]; then
  restart="/sbin/service $SVC_NAME restart"
  status="/sbin/service $SVC_NAME status";
elif [ $VERSION -eq 7 ]; then
  restart="/usr/bin/systemctl restart $SVC_NAME"
  status="/usr/bin/systemctl status $SVC_NAME";
else
  echo "OS not found"
  exit 1
fi

while [ $COUNT -lt $MAX_TRIES ]; do
  sudo $status
  if [ $? -ne 0 ]; then
    sudo $restart
    sleep $SLEEPTIME
    sudo $status
  else
    echo "$SVC_NAME is currently running"
    exit 0
  fi
  let COUNT=COUNT+1
done
echo "Too many failed attempts"
exit $ERR
