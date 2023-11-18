FROM eclipse-temurin:latest
RUN apt-get update && apt-get install -y \
    curl \
    jq

LABEL Author Endkind Ender <endkind.ender@endkind.net>

COPY getVelocity.sh /endkind/getVelocity.sh
COPY docker-entrypoint.sh /endkind/docker-entrypoint.sh

RUN chmod +x /endkind/getVelocity.sh
RUN chmod +x /endkind/docker-entrypoint.sh

ARG VELOCITY_VERSION=latest
RUN echo "$VELOCITY_VERSION" > /endkind/velocity_version

WORKDIR /velocity

VOLUME /velocity

ENV MIN_RAM=32M
ENV MAX_RAM=512M
ENV JAVA_FLAGS="-XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15"

ENTRYPOINT ["/endkind/docker-entrypoint.sh"]