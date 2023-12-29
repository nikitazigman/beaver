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
api_dir=$(realpath $this_dir/../)
docker_dir=$api_dir/docker

docker-compose -f $docker_dir/dev.yaml $@
