# Velocity - All Versions

This Docker image provides Velocity Minecraft Proxy versions. You can easily run a Minecraft Proxy using this image.

## Quick start

```bash
docker run -it -d -p 25565:25577 --name endkind-velocity endkind/velocity:latest
```

This command starts a Velocity server in detached mode (-d), maps port 25565 from the host to the container.

## Installation and Configuration (Recommended)

```bash
docker volume create endkind-velocity

docker run -it -d -p 25565:25577 --name endkind-velocity -v endkind-velocity:/velocity --restart=always endkind/velocity:latest
```

## Using Specific Versions

When deploying your server for production or if you require version stability, consider using specific image versions. For example:

### Velocity 3.2.0-SNAPSHOT

```bash
docker run -it -d -p 25565:25577 --name endkind-velocity endkind/velocity:3.2.0-SNAPSHOT
```

By specifying a version like 3.2.0-SNAPSHOT, you ensure that your server runs a known and tested version of Velocity.

### All Supported Cersions

- `latest` uses always the newest version
- `3.4.0-SNAPSHOT`
- `3.3.0-SNAPSHOT`
- `3.2.0-SNAPSHOT`
- `3.1.2-SNAPSHOT`
- `3.1.1-SNAPSHOT`
- `3.1.1`
- `3.1.0`
- `1.1.9`
- `1.0.10`

## Environment variables

You can customize your Velocity server by setting the following environment variables:

- `MIN_RAM` (default: 32M) - Minimum RAM allocated for the server.
- `MAX_RAM` (default: 512M) - Maximum RAM allocated for the server.
- `JAVA_FLAGS` - Additional Java flags generated with [flags.sh](https://flags.sh/).
- `VELOCITY_FLAGS` - Custom Velocity server flags.
- `TZ` (example: Europe/Berlin) - Set the time zone for the server.

These environment variables allow you to tailor your Velocity server's configuration to your specific requirements. You can adjust memory allocation, specify custom Java flags, and configure various server settings to suit your needs.

## How to build

Replace `<version>` with the desired version.

```bash
docker build --build-arg VELOCITY_VERSION=<version> -t endkind/velocity:<version> .
```

## Additional Information

- [GitHub Repository](https://github.com/Endkind/velocity)
- [Docker Repository](https://hub.docker.com/r/endkind/velocity)
- [Docker Compose Example](https://github.com/Endkind/velocity/blob/main/docker-compose.yml)
- [Visit our website](https://www.endkind.net) for more information about our projects and services.
- Connect to our Minecraft server (crossplay) at `mc.endkind.net` and start your adventure!

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/) License.

### Other License

This project includes code derived from the [Velocity](https://github.com/PaperMC/Velocity) project.
