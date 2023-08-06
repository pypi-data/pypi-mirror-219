from . import docker_tools


def build(*args):
    if not args:
        print("Provide a name for the image to be built: cq23 build my_cool_bot")
        exit(1)

    if len(args) > 1:
        print(
            "The name can't have spaces in it. Only alphabet characters, numbers, - and _ are allowed."
        )
        exit(1)

    name = args[0]
    if any([not str(c).isalnum() and c not in ["-", "_"] for c in name]):
        print(
            "Invalid characters in the name. Only alphabet characters, numbers, - and _ are allowed."
        )
        exit(1)

    if name[0] in ["-", "_"] or name[-1] in ["-", "_"]:
        print("Name can't end with - or _.")
        exit(1)

    if name in ["local-dev-client"]:
        print("This is a reserved name. Choose another name.")
        exit(1)

    docker_tools.ensure_docker_client_exists()
    docker_tools.check_dockerfile_exists()
    docker_tools.build_and_tag_image("cq-" + name)
    print(
        "Image successfully built! You can use this name in the cq23 run command:", name
    )
