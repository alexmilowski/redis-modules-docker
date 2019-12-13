# Packaging Modules

## An Example: Adding RedisGears

The follow commands will build a RAMP packaging of RedisGears for use in
Redis Enterprise. Afterwards, it will build a variant of Redis Enterprise image
with RedisGears packaged.

```bash
cd modules/redisgears
./ramp.sh 0.4
docker build -t yourdockerid/redisgears .
cd ../..
python dockerfile.py --baseimage redislabs/redis --module-image redisgears yourdockerid/redisgears:latest modules/redisgears/module.yaml > Dockerfile
docker build -t yourdockerid/redis-enterprise-with-gears .
```

The resulting image will allow you to enable the RedisGears module when
you create a new cluster and database.

Note that this particular version uses Python 2.7 but the RegisGears image will
package Python 3. To enable Python 3, you need to change the `command_line_args`
to point to `/opt/redislabs/lib/modules/python3`. You can do this in the `ramp.yml`
file to change the default or when you add the module during database creation.

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
