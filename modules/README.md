# Packaging Modules

## An Example: How to Add Specific Versions of Modules

In the following example, we will add specific versions of two modules:

 * [RedisGears](https://github.com/RedisGears/RedisGears) version 0.4.0
 * [RedisGraph](https://github.com/RedisGraph/RedisGraph) versin 1.99.7

For each of these modules, there is a version tag (v0.4.0 and v1.99.7, respectively) and a built container by redislabs:
 * [redislabs/redisgears:0.4.0](https://hub.docker.com/layers/redislabs/redisgears/0.4.0/images/sha256-59dabf459cacf135b833e110396317df23b824ba1fa413a051def3ceb7604da8)
 * [redislabs/redisgraph:1.99.7](https://hub.docker.com/layers/redislabs/redisgraph/1.99.7/images/sha256-7b17e367d5aca8876ffcbfbb5becfa4c6ad37b2d48a06418d9e3f82e3a695761)

The script [ramp.sh](ramp.sh) will pull a metadata file called `ramp.yml`. This file is used by the [RAMP packaging](https://github.com/RedisLabs/RAMP) tool from Redis Labs to package the module for use in
Redis Enterprise. The Redis Enterprise product uses this packaging to load modules for use in the cluster.

In this example, for each module:

 1. Use the `ramp.sh` script to pull the latest metadata file.
 2. Use `docker build` to install RAMP and package the built module in the target environment (e.g. Linux/x86_64).

Afterwards, we'll use the `dockerfile.py` and `docker build` together to build a variant of Redis Enterprise with the newly packaged modules in the right place to be loaded.

The process is as follows:

 1. Package the RedisGears module:

    ```bash
    cd modules/redisgears
    ../ramp.sh https://github.com/RedisGears/RedisGears.git tags/v0.4.0
    docker build -t yourdockerid/redisgear .
    cd ../..
    ```
 1. Package the RedisGraph module:

    ```bash
    cd modules/redisgraph
    ../ramp.sh https://github.com/RedisGears/RedisGears.git tags/v1.99.7
    docker build -t yourdockerid/redisgraph .
    cd ../..
    ```
 1. Build the Redis Enterprise variant image with the two modules:

    ```bash
    python dockerfile.py --baseimage redislabs/redis \
      --module-image redisgears yourdockerid/redisgears: \
      --module-image redisgraph yourdockerid/redisgraph: \
      modules/redisgears/module.yaml modules/redisgraph/module.yaml > Dockerfile
    docker build -t yourdockerid/rp+gears+graph .
    ```

The resulting image can be used in place of `redislabs/redis` but keep in mind
that you have to build a new variant for every release of the modules or base
image (Redis Enterprise).

For this particular example, please note:

 * The versions of the packaged modules are listed in the `module.yaml` files,
   respectively. If you choose a different version, you will have to edit these
   files.
 * The RedisGears module contains a version of Python 3. This version of python
   will be accessible in the resulting image at `/opt/redislabs/lib/modules/python3`.
   You can control which version is used by changing the `PythonHomeDir` option
   when you create a database. If you want other versions of Python, you'll need
   to adjust the docker build and `modules.yaml` as appropriate to include that
   version.


## Packing Your Own Module

The overall process is that you need to build a RAMP package in the architecture
of the target image. You can do this by building in the module docker image
(e.g., within `redislabs/redisgears:latest`).

The process is as follows:

 1. Pull a local copy of the RAMP YAML file (see [redisgears/ramp.sh](redisgears/ramp.sh)) or author one from scratch.
 2. Create a `Dockerfile` to build the RAMP zip file (see [redisgears/Dockerfile](redisgears/Dockerfile)).
 3. Describe the module and ensure the RAMP zip artifact specified to be copied to the modules directory (see [redisgears/module.yaml](redisgears/module.yaml))
 4. Generate a `Dockerfile` via `dockerfile.py` by including the `module.yaml` as one your inputs and ensure you specify the source image via `--module-image`.
 5. Build the image via `docker build`.
