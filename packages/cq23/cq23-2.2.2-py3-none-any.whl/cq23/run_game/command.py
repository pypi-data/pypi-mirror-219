import os
import shutil
import subprocess

from . import docker_tools
from .gcs import run_gcs


def clone_or_pull_repository(repository_url, folder_path):
    if not os.path.exists(folder_path):
        # Clone the repository if the folder doesn't exist
        subprocess.run(["git", "clone", repository_url, folder_path])
    else:
        # Pull the latest changes if the folder already exists
        current_dir = os.getcwd()
        os.chdir(folder_path)
        subprocess.run(["git", "pull"])
        os.chdir(current_dir)
    print(folder_path + " cloned successfully.")


def extract_arg_from_command_args(arg_name, args, default=None):
    arg_value = list(filter(lambda x: str(x).startswith(arg_name + "="), args))
    if not arg_value:
        return default
    if len(arg_value) > 1:
        raise Exception(f"Multiple `{arg_name}` arguments provided.")

    return arg_value[0][len(arg_name) + 1 :]  # noqa: E203


def copy_container_logs(game_files_abs_path, gcs_folder_name):
    src_dir = os.path.join(os.path.join(gcs_folder_name, "src"), "container_logs")
    dst_dir = os.path.join(game_files_abs_path, "replay_files")
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)
        # Copy the file to the destination directory
        shutil.copy2(src_file, dst_file)


def clean_image_name(image_name):
    """
    If the image name is one of the reserved ones, add the remote name to it.
    """
    if not image_name:
        return image_name

    if image_name in []:  # Add reserved names here when there are any
        image_name = (
            docker_tools.ECR_REGISTRY
            + "/"
            + docker_tools.SUBMISSIONS_ECR_REPO
            + ":"
            + image_name
        )
    else:
        image_name = "cq-" + image_name + ":latest"

    return image_name


def run_game(*args):
    docker_tools.ensure_docker_client_exists()
    game_files_dir = ".game_files"
    gcs_folder_name = "gcs"
    gcs_repo = "https://github.com/CALED-Team/game-communication-system.git"

    home_image = clean_image_name(
        extract_arg_from_command_args("home", args, "local-dev-client")
    )
    away_image = clean_image_name(
        extract_arg_from_command_args("away", args, "local-dev-client")
    )

    # If either of the images are the local ones, then build it.
    if "cq-local-dev-client:latest" in [home_image, away_image]:
        docker_tools.check_dockerfile_exists()
        docker_tools.build_and_tag_image(docker_tools.get_client_image_tag())

    if not os.path.exists(game_files_dir):
        os.makedirs(game_files_dir)
    os.chdir(game_files_dir)
    game_files_abs_path = os.getcwd()

    clone_or_pull_repository(gcs_repo, gcs_folder_name)
    docker_tools.pull_latest_game_server()
    run_gcs(
        gcs_folder_name,
        home_image,
        away_image,
        extract_arg_from_command_args("map", args),
    )
    docker_tools.copy_replay_files(game_files_abs_path)
    copy_container_logs(game_files_abs_path, gcs_folder_name)

    # Go back to the same directory as we were (one up)
    os.chdir(os.path.dirname(os.getcwd()))
