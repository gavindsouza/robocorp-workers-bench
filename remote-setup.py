import argparse
import subprocess
import time

import requests
from dotenv import dotenv_values
from pydo import Client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Robocorp Worker Cluster Wrapper",
        description="Manage Robocorp self-hosted workers' clusters",
        epilog="Simplified Robocorp Worker Setup Management Interface",
    )
    parser.add_argument("--create", "-c")
    parser.add_argument("--num_workers", "-n", type=int)
    parser.add_argument("--delete", "-x")

    args = parser.parse_args()
    config = dotenv_values("remote-setup.env")

    if args.create and args.num_workers:
        CLUSTER_SERIES = args.create
        NUM_WORKERS = args.num_workers

        ROBOCORP_WORKER_TOKEN = config["ROBOCORP_WORKER_TOKEN"]

        DO_TOKEN = config["DO_TOKEN"]
        DO_PROJECT = config["DO_PROJECT"]
        DO_SSH_KEY_ID = config["DO_SSH_KEY_ID"]

        DROPLET_REGION = config["DROPLET_REGION"]
        DROPLET_OS = config["DROPLET_OS"]
        DROPLET_SIZE = config["DROPLET_SIZE"]

        do_client = Client(token=DO_TOKEN)

        req = {
            "name": CLUSTER_SERIES,
            "region": DROPLET_REGION,
            "size": DROPLET_SIZE,
            "image": DROPLET_OS,
            "ssh_keys": [
                DO_SSH_KEY_ID,
            ],
            "backups": False,
            "ipv6": False,
            "monitoring": True,
            "tags": ["robocorp", "temporary"],
        }

        resp = do_client.droplets.create(body=req)
        print("Droplet created: ", resp)

        DROPLET_ID = resp["droplet"]["id"]

        while True:
            if (
                status := do_client.droplets.get(DROPLET_ID)["droplet"]["status"]
            ) == "active":
                break
            print(f"Server status: {status}", end="\r")
            time.sleep(5)
        print(f"Server status: {status}")

        DROPLET_IP = do_client.droplets.get(DROPLET_ID)["droplet"]["networks"]["v4"][0][
            "ip_address"
        ]

        SSH_PREFIX = [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "ConnectionAttempts=30",
            "-o",
            "ConnectTimeout=5",
            f"root@{DROPLET_IP}",
        ]
        INIT_COMMANDS = [
            "apt-get update",
            "DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::=--force-confold -o Dpkg::Options::=--force-confdef -y --allow-downgrades --allow-remove-essential --allow-change-held-packages upgrade -yqq",
            "apt-get install git",
            "curl https://get.docker.com/ | sh",
            "git clone https://github.com/gavindsouza/robocorp-workers-bench robocorp",
            "cd robocorp",
            "cp ./base/dynamic/Dockerfile .",
            "cp ./base/conda.yaml .",
            "./worker-up.py --build",
        ]
        SETUP_COMMANDS = [
            "cd robocorp",
            f'for i in `seq 0 {NUM_WORKERS - 1}`; do   ./worker-up.py -n "{CLUSTER_SERIES}-$i" -t {ROBOCORP_WORKER_TOKEN}; done',
        ]

        init_setup_command = " && ".join(INIT_COMMANDS)
        worker_setup_command = " && ".join(SETUP_COMMANDS)

        subprocess.run([*SSH_PREFIX, init_setup_command])
        subprocess.run([*SSH_PREFIX, "reboot"])
        subprocess.run([*SSH_PREFIX, worker_setup_command])

    elif args.delete:
        do_client = Client(token=config["DO_TOKEN"])
        DELETE_SERIES = args.delete
        ROBOCORP_SERVER = config["ROBOCORP_SERVER"]
        ROBOCORP_WORKSPACE_ID = config["ROBOCORP_WORKSPACE_ID"]
        AUTH_HEADERS = {"Authorization": config["ROBOCORP_API_KEY"]}
        get_resp = requests.get(
            f"{ROBOCORP_SERVER}/workspaces/{ROBOCORP_WORKSPACE_ID}/workers",
            headers=AUTH_HEADERS,
        )

        WORKERS_TO_DELETE = {
            w["id"]: w["name"]
            for w in get_resp.json()["data"]
            if w["name"].startswith(f"{DELETE_SERIES}-")
        }
        print("Deleting workers: ", WORKERS_TO_DELETE)

        for worker_id in WORKERS_TO_DELETE:
            del_resp = requests.delete(
                f"{ROBOCORP_SERVER}/workspaces/{ROBOCORP_WORKSPACE_ID}/workers/{worker_id}",
                headers=AUTH_HEADERS,
            )

        DROPLET_ID = None
        for droplet in do_client.droplets.list()["droplets"]:
            if droplet["name"] == DELETE_SERIES:
                DROPLET_ID = droplet["id"]
                break
        if not DROPLET_ID:
            print("No droplet found. You should manually delete the droplet.")
            exit(1)

        do_client.droplets.destroy(DROPLET_ID)

    else:
        print("Invalid arguments")
        parser.print_help()
        exit(1)
