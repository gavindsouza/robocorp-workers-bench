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

Steps to build & spin up a self-hosted worker:

* Generate a `Dockerfile`

```bash
cp Dockerfile.dynamic Dockerfile
```

* Setup appropriate conda.yaml

```bash
cp {your-robot-conda} conda.yaml
```

* Build a worker image

```bash
./worker-up.py --build -i rc_dynamic -v 1.0
```

* Spin up a worker using a single or group token

```bash
./worker-up.py -i rc_dynamic -v 1.0 -n {worker_name} -t {token}
```

#### Notes

Copy the `conda.yaml` from the targetted robot to this folder. It will be used in the container image building process.

Added the `--no-cache` during the image building because we don't want to cache the `rcc` environment creation. Alternatively, we can add the `ADD` directive to the pypi & github URLs to do so automatically.
