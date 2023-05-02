#! /usr/bin/env python3.10
import argparse
from subprocess import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Robocorp Worker Wrapper",
        description="Manage Robocorp self-hosted workers",
        epilog="Simplified Robocorp Worker Interface",
    )
    parser.add_argument("--name", "-n")
    parser.add_argument("--token", "-t")
    parser.add_argument(
        "--build", "-b", help="Build the worker image", action="store_true"
    )
    parser.add_argument("--dockerfile-location", "-d")
    parser.add_argument("--image-name", "-i")
    parser.add_argument("--image-version", "-v")
    args = parser.parse_args()

    dockerfile_dir = args.dockerfile_location or "/root/robocorp"
    image_name = args.image_name or "robocorpapp_dynamic_container"
    image_version = args.image_version or "3.0"

    if args.build:
        build_command = f"docker image build --tag {image_name}:{image_version} {dockerfile_dir} --no-cache"
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
