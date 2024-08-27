#!/bin/bash

# Determine the current script's directory
this_file=$(realpath $0)
this_dir=$(dirname $this_file)
# Build the path to the API Application's base directory
iac_dir=$(realpath $this_dir/..)

docker buildx build --platform=linux/amd64 -t public.ecr.aws/d0s9n5w1/beaver-nginx:latest $iac_dir/docker/nginx