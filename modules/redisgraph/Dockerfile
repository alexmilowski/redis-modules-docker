ARG VERSION=1.99.7
FROM redislabs/redisgraph:$VERSION as redisgraph

ARG ARCH=x86_64
ARG OS=Linux
ARG MODULES_DIR=/usr/lib/redis/modules

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y python3 python3-pip

RUN pip3 install ramp-packer
RUN mkdir -p /tmp/build
COPY ramp.yml /tmp/build
RUN ramp pack ${MODULES_DIR}/redisgraph.so -m /tmp/build/ramp.yml -A ${ARCH} -O ${OS} -o ${MODULES_DIR}/redisgraph.${OS}-${ARCH}.${VERSION}.zip
