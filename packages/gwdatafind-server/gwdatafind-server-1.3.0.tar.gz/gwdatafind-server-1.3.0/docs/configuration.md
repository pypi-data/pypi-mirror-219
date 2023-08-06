---
title: Configuration
---

# Server configuration

The recommended server configuration is to use
[Apache](https://httpd.apache.org/) as a reverse proxy to
[Gunicorn](https://gunicorn.org/).

## Pre-requisites

### Diskcache

The GWDataFind Server serves information read from a 'diskcache' file
prepared by the [`diskcache`](https://computing.docs.ligo.org/ldastools/LDAS_Tools/ldas-tools-diskcacheAPI/) service.
This needs to be configured an running in order to provide the necessary
input to the GWDataFind Server.

### Apache HTTP server

Custom pre-configuration may be required to enable Apache HTTP to act as
the reverse proxy for gunicorn.

## Step-by-step

1. Configure your Yum client to include the IGWN Yum Repositories for
   [Scientific Linux 7](https://computing.docs.ligo.org/guide/software/sl7/)
   or [Rocky Linux 7](https://computing.docs.ligo.org/guide/software/rl8/)

1. Install the necessary packages using `yum`:

    ```shell
    yum install gwdatafind-server httpd python3-gunicorn
    ```

1. Move the Apache Configuration file into the right place:

    ```shell
    ln -s /usr/share/gwdatafind-server/gunicorn.conf /etc/httpd/conf.d/gwdatafind-server.conf
    ```

1. Customise the `/etc/gwdatafind-server.ini` file as required

1. Start the gwdatafind-server service and the Apache http server:

    ```shell
    systemctl start gwdatafind-server.service
    systemctl start httpd.service
    ```
