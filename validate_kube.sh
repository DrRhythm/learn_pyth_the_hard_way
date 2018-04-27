#!/bin/bash
ERR=3
MAX_TRIES=2
COUNT=0

while [ $COUNT -lt $MAX_TRIES ]; do
   sudo /usr/bin/bash /etc/kubernetes/validate.sh
  if [ $? -ne 0 ]; then
    sleep 120
  else
    echo "Kube is up and running"
    exit 0
  fi
  let COUNT=COUNT+1
done
echo "Too many failed attempts"
exit $ERR
