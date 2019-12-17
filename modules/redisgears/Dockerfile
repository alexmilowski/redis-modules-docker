ARG VERSION=0.4.0
FROM redislabs/redisgears:$VERSION as redisgears

ARG VERSION
ARG ARCH=x86_64
ARG OS=Linux
ARG MODULES_DIR=/opt/redislabs/lib/modules

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y python3 python3-pip

RUN pip3 install ramp-packer
RUN mkdir -p /tmp/build
COPY ramp.yml /tmp/build
RUN ramp pack ${MODULES_DIR}/redisgears.so -m /tmp/build/ramp.yml -A ${ARCH} -O ${OS} -o ${MODULES_DIR}/redisgears.${OS}-${ARCH}.${VERSION}.zip
