import os

import docker
from docker.errors import DockerException

DOCKER_CLIENT = None


def ensure_docker_client_exists():
    global DOCKER_CLIENT
    try:
        DOCKER_CLIENT = docker.from_env()
    except DockerException:
        print(
            "Docker not found! Either not installed or not running. If you have installed Docker Desktop make sure to "
            'open it first. Search "Docker Desktop" in your applications.'
        )
        exit(1)


def check_dockerfile_exists():
    current_dir = os.getcwd()
    dockerfile_path = os.path.join(current_dir, "Dockerfile")

    if os.path.isfile(dockerfile_path):
        print("Dockerfile found.")
    else:
        raise Exception(
            "Dockerfile not found! Make sure you run `cq23_run` from the directory that contains your bot's"
            " Dockerfile."
        )


def build_and_tag_image(image_tag):
    print("Building the image...")
    current_dir = os.getcwd()
    dockerfile_path = os.path.join(current_dir, "Dockerfile")

    # Build the Docker image
    image, _ = DOCKER_CLIENT.images.build(
        path=current_dir, dockerfile=dockerfile_path, tag=image_tag, rm=True
    )

    # Print the ID of the built image
    print("Docker image built with ID:", image.id)
