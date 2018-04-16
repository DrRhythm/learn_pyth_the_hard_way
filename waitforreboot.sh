#!/bin/bash

key_path =

echo -n "Started at "
date
if [ -z "$1" ]
then
  echo "The hostname to wait for is a required argument"
  exit 1
fi
hostname="$1"
sleep 60 # Give it some time first to make sure it's quit responding
while ! ping -c 2 $hostname &>/dev/null
do
  true
done
# Wait for sshd to start
while ! /usr/bin/ssh -o "ConnectTimeout 5" -o "IdentityFile $key_path" -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" rundeck@$hostname -- exit
do
  sleep 2
done
echo -n "Finished at "
date
