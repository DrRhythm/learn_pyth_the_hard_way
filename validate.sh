function fail {
    echo $1
    exit 1
}

HOST_IP=10.36.157.83

printf 'verifying docker... '
systemctl is-active docker 2>&1 >/dev/null || fail 'docker not started'
systemctl is-enabled docker 2>&1 >/dev/null || fail 'docker not enabled'
echo 'ok!'

printf 'verifying flannel... '
systemctl is-active flanneld 2>&1 >/dev/null || fail 'flannel not started'
systemctl is-enabled flanneld 2>&1 >/dev/null || fail 'flannel not enabled'
echo 'ok!'

printf 'verifying kubelet... '
systemctl is-active kubelet 2>&1 >/dev/null || fail 'kubelet not started'
systemctl is-enabled kubelet 2>&1 >/dev/null || fail 'kubelet not enabled'
nc $HOST_IP 10250 -w 3 </dev/null || fail 'kubelet port 10250 not listening'
nc $HOST_IP 10255 -w 3 </dev/null || fail 'kubelet port 10255 not listening'
echo 'ok!'

printf 'verifying etcd... '
systemctl is-active etcd 2>&1 >/dev/null || fail 'etcd service not started'
systemctl is-enabled etcd 2>&1 >/dev/null || fail 'etcd service not enabled'
systemctl is-active etcd-events 2>&1 >/dev/null || fail 'etcd-events service not started'
systemctl is-enabled etcd-events 2>&1 >/dev/null || fail 'etcd-events service not enabled'
nc 127.0.0.1 4001 -w 3 </dev/null || fail 'etcd port not available'
nc 127.0.0.1 4002 -w 3 </dev/null || fail 'etcd-events port not available'
echo 'ok!'

printf 'verifying DNS... '
(docker pull busybox) >/dev/null
(docker run --rm -t busybox nslookup google.com 192.168.172.3) >/dev/null || fail 'unable to hit kube nameserver'
(docker run --rm -t busybox nslookup kubernetes.default.svc.k8s.int.godaddy.com 192.168.172.3) >/dev/null || fail 'unable to resolve kube DNS via service discovery'
echo 'ok!'

printf 'verifying API access... '
nc 192.168.172.1 443 -w 3 </dev/null || fail 'port not available'
