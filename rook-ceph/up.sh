#!/bin/bash
## docs at https://rook.io/docs/rook/v1.0/ceph-quickstart.html
## Helm Chart instructions available at https://rook.io/docs/rook/v1.0/helm-operator.html
### MAKE SURE TO CREATE THE DIRECTORY /var/lib/rook on the nodes

kubectl create -f common.yaml
kubectl create -f operator.yaml

echo "verify the rook-ceph-operator, rook-ceph-agent, and rook-discover pods are in the `Running` state before proceeding"
echo "Then CTRL+C to continue...."
kubectl -n rook-ceph get pod -w -o wide

kubectl create -f cluster-test.yaml

# toolbox
kubectl create -f toolbox.yaml

# create filesystem
kubectl create -f filesystem.yaml
