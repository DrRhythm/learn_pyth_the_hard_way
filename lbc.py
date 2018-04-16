#!/bin/bash

# Side A = Odds active
# Side B = Evens active
# Side C = All active

if [ "@option.Cluster@" == "all" ]
then
  clusters="admin pre sfapp"
else
  clusters="@option.Cluster@"
fi

for cluster in $clusters
do
  case ${cluster} in
    admin)
      backends="admin-out admin-out-443 provisioning-out"
      num=2
      ;;
    pre)
      backends="preview-out preview-out-443"
      num=2
      ;;
    sfapp)
      backends="storefront-out storefront-out-443"
      num=2
      ;;
    *)
      echo "Something went wrong: Unknown Cluster '${cluster}' Exiting." >&2
      exit 1;
    ;;
  esac

  case @option.Side@ in
    A|B)
      if [ "@option.Side@" = "A" ]; then
        order=(1 2)
      elif [ "@option.Side@" = "B" ]; then
        order=(2 1)
      else
        echo "How did I get here?" >&2
        exit 1
      fi
      for server in $(eval echo p3tlqsc${cluster}00{${order[0]}..${num}..2}); do
        for backend in $backends; do
          if [ ! -z "$command" ]; then
            command="$command; set server ${backend}/${server} state ready"
          else
            command="set server ${backend}/${server} state ready"
          fi
        done
      done
      for server in $(eval echo p3tlqsc${cluster}00{${order[1]}..${num}..2}); do
        for backend in $backends; do
          command="$command; set server ${backend}/${server} state maint"
        done
      done
    ;;
    C)
      for server in $(eval echo p3tlqsc${cluster}00{1..${num}}); do
        for backend in $backends; do
          if [ ! -z "$command" ]; then
            command="$command; set server ${backend}/${server} state ready"
          else
            command="set server ${backend}/${server} state ready"
          fi
        done
      done
      ;;
    *)
      echo "Something went wrong: Unknown SwingType '@option.Side@' Exiting." >&2
      exit 1;
    ;;
  esac
done

echo "$command" |nc -U  /var/run/haproxy.sock
