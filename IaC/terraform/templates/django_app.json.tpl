[
    {
        "name": "beaver-api",
        "image": "${docker_image_url_django}",
        "essential": true,
        "cpu": 10,
        "memory": 512,
        "portMappings": [
            {
                "containerPort": 8000,
                "protocol": "tcp"
            }
        ],
        "command": [
            "gunicorn",
            "-w",
            "3",
            "-b",
            ":8000",
            "hello_django.wsgi:application"
        ],
        "environment": [],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/ecs/beaver-api",
                "awslogs-region": "${region}",
                "awslogs-stream-prefix": "beaver-api-log-stream"
            }
        }
    }
]