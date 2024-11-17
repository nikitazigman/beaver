import boto3
import click

from loguru import logger


def get_current_task_definition(client, cluster, service):
    response = client.describe_services(cluster=cluster, services=[service])
    current_task_arn = response["services"][0]["taskDefinition"]
    return client.describe_task_definition(taskDefinition=current_task_arn)


@click.command()
@click.option("--cluster", help="Name of the ECS cluster", required=True)
@click.option("--service", help="Name of the ECS service", required=True)
@click.option(
    "--image",
    help="Docker image URL for the updated application",
    required=True,
)
@click.option("--container-name", help="Name of the container to update", required=True)
def deploy(cluster, service, image, container_name):
    client = boto3.client("ecs")

    # Fetch the current task definition
    logger.info("Fetching current task definition...")
    response = get_current_task_definition(client, cluster, service)

    # Iterate over container definitions and update the image for the matching container
    container_definitions = response["taskDefinition"]["containerDefinitions"]
    for container in container_definitions:
        if container["name"] == container_name:
            container["image"] = image
            logger.info(f"Updated {container_name} image to: {image}")

    # Register a new task definition
    logger.info("Registering new task definition...")
    response = client.register_task_definition(
        family=response["taskDefinition"]["family"],
        volumes=response["taskDefinition"]["volumes"],
        containerDefinitions=container_definitions,
        cpu="256",  # Modify based on your needs
        memory="512",  # Modify based on your needs
        networkMode="awsvpc",
        requiresCompatibilities=["FARGATE"],
        executionRoleArn="ecs_task_execution_role_prod",
        taskRoleArn="ecs_task_execution_role_prod",
    )
    new_task_arn = response["taskDefinition"]["taskDefinitionArn"]
    logger.info(f"New task definition ARN: {new_task_arn}")

    # Update the service with the new task definition
    logger.info("Updating ECS service with new task definition...")
    client.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=new_task_arn,
    )
    logger.info("Service updated!")


if __name__ == "__main__":
    deploy()
