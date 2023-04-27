#! /usr/bin/env python3.10
import argparse
from subprocess import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Robocorp Worker Wrapper",
        description="Manage Robocorp workers",
        epilog="SwitchUp's Robocorp Worker Interface",
    )
    parser.add_argument("--build", help="Build the worker image", action="store_true")
    parser.add_argument("--name", "-n")
    parser.add_argument("--token", "-t")
    args = parser.parse_args()

    dockerfile_location = "/root/robocorp"
    image_name = "robocorpapp_dynamic_container"
    image_version = "3.0"

    if args.build:
        build_command = f"docker image build --tag {image_name}:{image_version} {dockerfile_location}"
        run(build_command, shell=True)

    elif args.name and args.token:
        exec_command = (
            f"docker run -dit "
            f"-e NAME={args.name} -e LINK_TOKEN={args.token} "
            f"--restart unless-stopped --name {args.name} "
            f"{image_name}:{image_version}"
        )
        run(exec_command, shell=True)

    else:
        print("Invalid arguments")
        parser.print_help()
        exit(1)
