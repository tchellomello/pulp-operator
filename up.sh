#!/bin/bash

# TODO: Check if all of these are needed.
# TODO: Check if these should only ever be run once; or require
# special logic to update
kubectl create ns pulp
kubectl apply -n pulp -f deploy/crds/pulpproject_v1alpha1_pulp_crd.yaml
kubectl apply -n pulp -f deploy/crds/pulpproject_v1alpha1_pulp_cr.yaml

kubectl apply -n pulp -f deploy/service_account.yaml
kubectl apply -n pulp -f deploy/role.yaml
kubectl apply -n pulp -f deploy/role_binding.yaml
kubectl apply -n pulp -f deploy/operator.yaml
