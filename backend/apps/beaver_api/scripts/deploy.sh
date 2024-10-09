#!/bin/bash

# Set variables
REGISTRY_URL="public.ecr.aws/d0s9n5w1"
IMAGE_NAME="beaver-api"
IMAGE_TAG="latest"

# Determine the current script's directory
this_file=$(realpath $0)
this_dir=$(dirname $this_file)
# Build the path to the API Application's base directory
api_dir=$(realpath $this_dir/../)
project_root=$(realpath $api_dir/../../../)

# Step 1: Authenticate with ECR
echo "Authenticating with ECR..."
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

if [ $? -ne 0 ]; then
    echo "Authentication failed. Exiting."
    exit 1
fi

# Step 2: Build the Docker image
echo "Building Docker image..."
docker build -t $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG --platform=linux/arm64 $api_dir

if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi

echo "Docker image built: $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG"

# Step 3: Push the Docker image
echo "Pushing Docker image to ECR..."
docker push $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG

if [ $? -ne 0 ]; then
    echo "Docker push failed. Exiting."
    exit 1
fi

echo "Docker image pushed: $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG"

# Step 4: Apply Terraform changes
echo "Applying Terraform changes..."
cd $project_root/IaC/terraform
terraform init
terraform apply -auto-approve

if [ $? -ne 0 ]; then
    echo "Terraform apply failed. Exiting."
    exit 1
fi

echo "Terraform changes applied successfully."

echo "Deployment completed successfully!"
