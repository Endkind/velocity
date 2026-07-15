FROM python:3.13-slim AS build

ARG VERSION=4.1.0-SNAPSHOT
ARG BUILD=latest

COPY get-velocity.py get-velocity.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python get-velocity.py --version $VERSION --build $BUILD --output /endkind/server.jar

FROM eclipse-temurin:25 AS runtime

LABEL Author="Endkind Ender <endkind.ender@endkind.net>"

RUN groupadd --system --gid 10001 velocity \
    && useradd --system --uid 10001 --gid velocity --home-dir /data --shell /usr/sbin/nologin velocity \
    && mkdir -p /endkind /data \
    && chown -R velocity:velocity /endkind /data

COPY --chown=velocity:velocity entrypoint.sh /endkind/entrypoint.sh
RUN chmod +x /endkind/entrypoint.sh

COPY --from=build --chown=velocity:velocity /endkind/server.jar /endkind/server.jar

WORKDIR /data
VOLUME /data

ENV MIN_RAM=32M
ENV MAX_RAM=3G
ENV JAVA_FLAGS="-XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:MaxInlineLevel=15"
ENV VELOCITY_FLAGS=""

USER velocity

ENTRYPOINT [ "/endkind/entrypoint.sh" ]
