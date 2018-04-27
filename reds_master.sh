#!/bin/bash

REDIS_HOST=@node.hostname@
REDIS_PORT=6379

case $(hostname -s) in
  *olaredis*)
    MASTER_NAME=ola
    REDIS_CONFIG=/etc/redis_ola_6379.conf
    ;;
  *payredis*)
    MASTER_NAME=securepay
    REDIS_CONFIG=/etc/redis_securepay_6379.conf
    ;;
  *)
    echo "Unknown cluster..."
    exit 1
esac

REDIS_PASS=`awk '/^masterauth/ {print $2}' ${REDIS_CONFIG}`

if redis-cli -h ${REDIS_HOST} -p ${REDIS_PORT} -a ${REDIS_PASS} ROLE | grep -q "@option.role@"; then
    echo "Verified @node.name@ is currently a @option.role@ for '${MASTER_NAME}'..."
    exit 0
else
    echo "@node.name@ is not a @option.role@ for '${MASTER_NAME}'.  Exiting..."
    exit 1
fi


#!/bin/bash

REDIS_HOST=@node.hostname@
REDIS_PORT=6379
REDIS_PASS=`awk '/^masterauth/ {print $2}' /etc/redis_ola_6379.conf`

REDIS_SENTINEL_PORT=26379
MASTER_NAME='ola'

if redis-cli -h ${REDIS_HOST} -p ${REDIS_PORT} -a ${REDIS_PASS} ROLE | grep -q 'master'; then
    echo "Initiating failover of '${MASTER_NAME}' master @node.name@..."
    redis-cli -p ${REDIS_SENTINEL_PORT} sentinel failover ${MASTER_NAME}

    sleep 30

    # Verify master has been failed over, and this node is not the current master according the sentinels
    if redis-cli -p ${REDIS_SENTINEL_PORT} sentinel master ${MASTER_NAME} | grep -q @node.hostname@; then
       echo "@node.name@ is the current '${MASTER_NAME}' master, and has not been failed over successfully.  Skipping patching..."
       exit 1
    else
        echo "Master failover complete.  Patching @node.name@..."
        exit 0
    fi
else
    echo "@node.name@ is not the current '${MASTER_NAME}' master.  Exiting..."
    exit 1
fi
