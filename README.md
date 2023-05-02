### Simplified Robocorp Setup

Run `./worker-up.py` for available CLI options & help.

```bash
usage: Robocorp Worker Wrapper [-h] [--build] [--name NAME] [--token TOKEN] [--group-token GROUP_TOKEN] [--dockerfile-location DOCKERFILE_LOCATION]
                               [--image-name IMAGE_NAME] [--image-version IMAGE_VERSION]

Manage Robocorp self-hosted workers

options:
  -h, --help            show this help message and exit
  --build               Build the worker image
  --name NAME, -n NAME
  --token TOKEN, -t TOKEN
  --group-token GROUP_TOKEN, -g GROUP_TOKEN
  --dockerfile-location DOCKERFILE_LOCATION, -d DOCKERFILE_LOCATION
  --image-name IMAGE_NAME, -i IMAGE_NAME
  --image-version IMAGE_VERSION, -v IMAGE_VERSION

Simplified Robocorp Worker Interface
```

Steps to build & spin up a self-hosted worker:

1. Generate a `Dockerfile`

`cp Dockerfile.dynamic Dockerfile`

1. Setup appropriate conda.yaml

`cp {your-robot-conda} conda.yaml`

1. Build a worker image

`./worker-up.py --build -i rc_dynamic -v 1.0`

1. Spin up a worker using a single or group token

`./worker-up.py -n {worker_name} -t {token}`


#### Notes

Copy the `conda.yaml` from the targetted robot to this folder. It will be used in the container image building process.

Added the `--no-cache` during the image building because we don't want to cache the `rcc` environment creation. Alternatively, we can add the `ADD` directive to the pypi & github URLs to do so automatically.
