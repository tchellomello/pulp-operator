#!/bin/bash
kubectl -n pulp delete -f deploy/operator.yaml

# clean stuff
kubectl -n pulp delete deployments postgres pulp-api pulp-content pulp-resource-manager pulp-worker redis
kubectl -n pulp delete service postgres pulp-api pulp-content redis
kubectl -n pulp delete pvc postgres-data pulp-file-storage redis-data
kubectl -n pulp delete configmap pulp-server

kubectl -n pulp delete -f deploy/service_account.yaml
kubectl -n pulp delete -f deploy/role_binding.yaml
kubectl -n pulp delete -f deploy/role.yaml

kubectl -n pulp delete -f deploy/crds/pulpproject_v1alpha1_pulp_crd.yaml
kubectl -n pulp delete -f deploy/crds/pulpproject_v1alpha1_pulp_cr.yaml
