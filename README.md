# redis-modules-docker

This repository contains a simple utility for building Docker images for Redis with various module support. The utility generates a Dockerfile that can be used to build a target image from the source images that contains all each module, specify their configuration, and configures the Redis server to load the modules.

For example, you can build your own image with RedisGraph and RedisGears (see [modules.yaml](modules.yaml)) via:

```bash
% python dockerfile.py modules.yaml > Dockerfile
% docker build -t redismodules .
```

# Usage

Each YAML input file specifies a number of modules to combine. The simplest invocation is:

```bash
% python dockerfile.py modules.yaml
```

This will produce the example file [Dockerfile.example](Dockerfile.example) that combines the `RedisGraph` and `RedisGears` modules.

Any number of YAML files can be specified as input and the order of the modules is preserved. If the same module (matched by 'name') is listed more than once, the last specified module will be used.

There are also some other options:

 * `--output` specifies a output file
 * `--exclude` specifies a module to exclude from the output
 * `--baseimage` controls the base image for the target image
 * `--libdir` controls the library directory inside the image
 * `--expose` controls the port exposed by the image


# Describing Configurations using YAML

The base image (typically `redis:latest`) can be agumented by adding a number of
modules. The simplest usage is to describe a set of modules to be added.
From that description, the program will generate necessary commands to build
a Docker image that will run Redis with all the specified modules.

## Describing Modules

Modules can be described in a YAML file either as a single module or a sequence
of modules.  A module must of a `kind` property with a value of `Module`
and must also have a `name` and `image` property. For the module to be
loaded, the `command` property must also be specified for any additional Redis
server command options (e.g., a `--loadmodule` option).

For example, the RedisGraph module is described as:

```YAML
kind: Module
name: redisgraph
image: redislabs/redisgraph:edge
artifacts:
 - source: "/usr/lib/redis/modules/redisgraph.so"
script: |
 RUN set -ex;\
     apt-get update;\
     apt-get install -y --no-install-recommends libgomp1;
command: [ "--loadmodule", "/opt/redislabs/lib/modules/redisgraph.so" ]
```

The `artifacts` property specifies a sequence of source files to copy from the
image (e.g., the shared library for the module). Minimally, the `source`
property must specify the location of the file from the module image. Optionally, a
`target` property can specified the destination on the target. The `source`
and `target` values follow the same rules as the
[Docker COPY](https://docs.docker.com/engine/reference/builder/#copy) command.

For example, for the RedisGears, the python3 directory is copied via:

```YAML
artifacts:
- source: "$REDIS_MODULES/python3"
  target: "$REDIS_MODULES/python3"
```

An optional `script` property can specify additional docker commands to run
for the target image.

## Describing Targets

There are a number of operations performed to product a working target image.
This process can be controlled by using a YAML object with a `kind` property
with value `Target` (see [full.yaml](full.yaml)).

The following properties may be specified:

 * `baseimage` - the base image for the target image
 * `expose` - the port to be exposed by the container
 * `script` - the build script to run for the base image
 * `libdir` - the library directory to use during the build
 * `modules` - a sequence of Modules (kind: Module) to include in the target

# Using Modules with Enterprise

Modules need to be packaged for Redis Enterprise to load the module. See [modules](modules)
for more information.
