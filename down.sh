#!/bin/bash

# TODO: Check if all of these are needed.
# TODO: Check if these should only ever be run once; or require
# special logic to update
kubectl delete -f deploy/crds/pulpproject_v1alpha1_pulp_crd.yaml
kubectl delete -f deploy/crds/pulpproject_v1alpha1_pulp_cr.yaml

kubectl delete -f deploy/service_account.yaml
kubectl delete -f deploy/role.yaml
kubectl delete -f deploy/role_binding.yaml
kubectl delete -f deploy/operator.yaml

# clean pods
kubectl -n pulp delete deployments postgres pulp-api pulp-content pulp-operator pulp-resource-manager pulp-worker redis
kubectl -n pulp delete service postgres pulp-api pulp-content redis
kubectl -n pulp delete pvc postgres-data pulp-file-storage redis-data
kubectl -n pulp delete configmap pulp-server

