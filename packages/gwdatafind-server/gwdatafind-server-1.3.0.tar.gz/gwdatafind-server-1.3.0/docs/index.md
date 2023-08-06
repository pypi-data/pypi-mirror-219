---
title: Introduction
author: Duncan Macleod <duncan.macleod@ligo.org>
---

# GWDataFind Server

The GWDataFind Server is [Flask](https://flask.palletsprojects.com/)
application that implements a REST API for the discovery of data URLs.

The GWDataFind Server is developed and used by the
[LIGO Scientific Collaboration](https://www.ligo.org) to enable easy
discovery of gravitational-wave observatory data for researchers.

## Installation

The recommended method for installing GWDataFind Server is via
the RPMs distributed in the IGWN Yum Repositories for
[Scientific Linux 7](https://computing.docs.ligo.org/guide/software/sl7/)
and [Rocky Linux 7](https://computing.docs.ligo.org/guide/software/rl8/):

```shell
yum install gwdatafind-server
```

## Configuration

See [_Configuration_](configuration.md).

## API

See [_API_](api/index.md).
