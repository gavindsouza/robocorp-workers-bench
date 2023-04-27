### SwitchUp's Robocorp Setup

Run `./worker-up.py` for available CLI options & help.

Copy the `conda.yaml` from the targetted robot to this folder. It will be used in the container image building process.

Steps to build & spin up a self-hosted worker:

1. `cp Dockerfile.dynamic Dockerfile`
1. `docker image build --tag robocorpapp_dynamic_container:3.0 . --no-cache`
1. `./worker-up.py -n {worker_name} -t {token}`

> Note: Add the `--no-cache` during the image building because we don't want to cache the `rcc` environment creation. Alternatively, we can add the `ADD` directive to the pypi & github URLs to do so automatically.
