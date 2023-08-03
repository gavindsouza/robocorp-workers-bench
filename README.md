### Simplified Robocorp Setup

Run `./worker-up.py` for available CLI options & help.

```bash
usage: Robocorp Worker Wrapper [-h] [--name NAME] [--token TOKEN] [--build] [--dockerfile-location DOCKERFILE_LOCATION] [--image-name IMAGE_NAME]
                               [--image-version IMAGE_VERSION]

Manage Robocorp self-hosted workers

options:
  -h, --help            show this help message and exit
  --name NAME, -n NAME
  --token TOKEN, -t TOKEN
  --build, -b           Build the worker image
  --dockerfile-location DOCKERFILE_LOCATION, -d DOCKERFILE_LOCATION
  --image-name IMAGE_NAME, -i IMAGE_NAME
  --image-version IMAGE_VERSION, -v IMAGE_VERSION

Simplified Robocorp Worker Management Interface
```

#### Steps to setup a Cluster of self-hosted workers

Steps to build & spin up a self-hosted worker:

1. Generate a `Dockerfile` that outlines the worker environment

I prefer using the dynamic workers for quickly spinning up workers that I can discard later.

```bash
cp ./base/dynamic/Dockerfile Dockerfile
```

2. Setup appropriate conda.yaml that outlines robot runtime context

A conda file that resembles the environment your robots need. This ensures a suitable environment is generated while building the image to avoid any slow downs during executing robot processes.

```bash
cp {your-robot-conda} conda.yaml
```

3. Build a worker image

Build the common image which will be used for spinning up new workers.

```bash
./worker-up.py --build -i rc_dynamic -v 1.0
```

4. Spin up a worker using a single or group token

Each worker started translates to a container spun up using the image generated in the previous step.

```bash
./worker-up.py -i rc_dynamic -v 1.0 -n {worker_name} -t {token}
```

#### Gavin's Workflow

1. Provision a new server & SSH to it
1. `apt update && apt upgrade -y && apt install git`
1. `curl https://get.docker.com/ | sh`
1. `git clone https://github.com/switchup-de/robocorp-workers-bench robocorp`
1. `cd robocorp`
1. `cp ./base/dynamic/Dockerfile .`
1. `cp ./base/conda.yaml .`
1. `./worker-up.py --build`
1. `export ROBOCORP_GROUP_TOKEN=${NEW_TOKEN_GENERATED_IN_CONTROL_ROOM}`
1. ```for i in `seq 1 N`; do   ./worker-up.py -n "a-$i" -t $ROBOCORP_GROUP_TOKEN; done```


```bash
# for copy pastin' - update token & worker count values (first & last lines)
export ROBOCORP_GROUP_TOKEN=${NEW_TOKEN_GENERATED_IN_CONTROL_ROOM}
apt update && apt upgrade -y && apt install git
curl https://get.docker.com/ | sh
git clone https://github.com/switchup-de/robocorp-workers-bench robocorp
cd robocorp
cp ./base/dynamic/Dockerfile .
cp ./base/conda.yaml .
./worker-up.py --build
for i in `seq 1 N`; do   ./worker-up.py -n "a-$i" -t $ROBOCORP_GROUP_TOKEN; done
```

#### Notes

Copy the `conda.yaml` from the targetted robot to this folder. It will be used in the container image building process.

Added the `--no-cache` during the image building because we don't want to cache the `rcc` environment creation. Alternatively, we can add the `ADD` directive to the pypi & github URLs to do so automatically.
