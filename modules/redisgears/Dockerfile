FROM redislabs/redisgears:latest as redisgears

ARG ARCH=x86_64
ARG OS=Linux
ARG GEARS_VERSION=0.4.0
ARG MODULES_DIR=/opt/redislabs/lib/modules
ARG BRANCH=0.4
ARG REPO=https://github.com/RedisGears/RedisGears.git

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

ENV PATH="${PATH}:${MODULES_DIR}/python3/bin"

RUN pip3 install ramp-packer
RUN mkdir -p /tmp/build
COPY ramp.yml /tmp/build
WORKDIR /tmp/build
RUN git clone --single-branch --branch $BRANCH $REPO
RUN cd RedisGears; ramp pack ${MODULES_DIR}/redisgears.so -m ramp.yml -A $ARCH -O $OS -o ${MODULES_DIR}/redisgears.${OS}-${ARCH}.${GEARS_VERSION}.zip
