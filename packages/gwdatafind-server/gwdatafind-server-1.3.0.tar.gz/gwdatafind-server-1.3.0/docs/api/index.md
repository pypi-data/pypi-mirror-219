---
title: API
author: Duncan Macleod <duncan.macleod@ligo.org>
---

# GWDataFind Server API

The Application Programming Interface defines how users can interact
with a GWDataFind Server instance to retrieve data.

## API Versions

The API is versioned, and each GWDataFind Server instance implements one
or more versions of the API depending on which version of the server
software is being used.

The latest version of the API is [v1](./v1.md).

## Discovering the API version for a specific server

All GWDataFind servers support the `/version` API endpoint, which returns
the supported API version(s):

```shell
curl https://gwdatafind.example.com/api/version
```

```json
{
  "version": "1.3.0",
  "api_versions": [
    "v1",
  ]
}
```
