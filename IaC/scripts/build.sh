#!/bin/bash

# Determine the current script's directory
this_file=$(realpath $0)
this_dir=$(dirname $this_file)
# Build the path to the API Application's base directory
api_dir=$(realpath $this_dir/../../)
iac_dir=$(realpath $this_dir/..)

docker build -t public.ecr.aws/d0s9n5w1/beaver-api:latest --platform=linux/arm64 $api_dir/backend/apps/beaver_api
docker build -t public.ecr.aws/d0s9n5w1/beaver-nginx:latest --platform=linux/arm64 $iac_dir/docker/nginx
