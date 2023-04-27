#! /usr/bin/env python3.10
import shlex
import subprocess
import shutil
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Robocorp Worker Wrapper',
                    description='Manage Robocorp workers',
                    epilog='SwitchUp\'s Robocorp Worker Interface')
    parser.add_argument("--name", "-n")
    parser.add_argument("--token", "-t")
    args = parser.parse_args()

    dockerfile = "/root/robocorp"

    #build_command = f"docker image build --tag robocorpapp_dynamic_container:3.0 {dockerfile}"
    #exec_command = f"docker run -dit {args.name}:1.0"
    exec_command = f"docker run -dit -e NAME={args.name} -e LINK_TOKEN={args.token} robocorpapp_dynamic_container:3.0 --restart unless-stopped --name {args.name}"

    #docker_ps = shutil.which("docker")
    #os.execv(docker_ps, shlex.split(command))
    #subprocess.run(build_command, shell=True)
    subprocess.run(exec_command, shell=True)

