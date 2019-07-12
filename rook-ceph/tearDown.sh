#!/bin/bash

kubectl delete -f filesystem.yaml
kubectl delete -f toolbox.yaml

kubectl -n rook-ceph delete cephcluster rook-ceph

SECS=30
echo "Waiting $SECS while cleaning all up.."
sleep $SECS

kubectl delete -f operator.yaml
kubectl delete -f common.yaml


echo "All clear"
echo "Remember to clean up the /var/lib/rook directory from your nodes"
