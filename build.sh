#!/bin/bash
buildah bud -t docker.io/tchellomello/pulp-operator:latest .
podman  push docker.io/tchellomello/pulp-operator:latest
