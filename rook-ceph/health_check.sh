#!/bin/bash

kubectl -n rook-ceph get pod -l "app=rook-ceph-tools" &>/dev/null || ( echo "rook-ceph-tools pod is not running"; exit)

for cmd in "ceph status" "ceph osd status" "ceph df" "rados df"; do
  echo ""
  echo "$cmd"
  echo "==============================="
  kubectl -n rook-ceph exec -it \
      $(kubectl -n rook-ceph get pod -l "app=rook-ceph-tools" -o jsonpath='{.items[0].metadata.name}') $cmd
done
