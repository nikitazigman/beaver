#!/bin/bash

#############################
# up the development environment #
#############################


#######################
# List of directories #
#######################
# Determine the current script's directory
this_file=$(realpath $0)
this_dir=$(dirname $this_file)
# Build the path to the API Application's base directory
iac_dir=$(realpath $this_dir/../)
docker_dir=$iac_dir/docker

docker-compose -f $docker_dir/dev.yaml $@
