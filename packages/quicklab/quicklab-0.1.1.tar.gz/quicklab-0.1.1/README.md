# quicklab

Start Jupyter Lab sessions on the cloud

## Features

* VM creation
* Jupyter on Docker
* SSL certificates (ZeroSSL & Caddy)
* Volumes management (Creation, Resizing, deletion, formating, etc)
* DNS A record creation (Google, Cloudflare)
* Automatic shutdown by inactivity (by Jupyter)
* GPU Provisioning (nvidia-smi installation, docker configuration, etc)
* Linux image creation (Packer)
* Entities types for autocompletion
* Logging into cloud provider log service

Only Google Cloud Platform supported for now, but relatively easy to add new
cloud providers.

## Usage

For users:

* [Quickstart](docs/quickstart.md)

For administrators:

* [Deploy](docs/deploy.md)
* [Images](docs/images.md)
* [Volumes](docs/volumes.md)
* [Permissions](docs/permissions.md)

## Acknowledgments

* Original work from [LabMachine](https://github.com/nuxion/labmachine)

## License

Work licensed under MPL 2.0. See [LICENSE](LICENSE) for more.
