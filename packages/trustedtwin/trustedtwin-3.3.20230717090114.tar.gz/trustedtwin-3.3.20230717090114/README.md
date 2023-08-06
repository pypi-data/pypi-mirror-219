TrustedTwin Python Client
===

Trusted Twin API Client version 1.+. 

Local development
---

After cloning repo:
```shell
cd python-client
export TRUSTED_TWIN_CORE_VER=1.0.0
export OPEN_API_SPEC_FILE_PATH=$PATH_TO_SWAGGER_FILE
```

`TRUSTED_TWIN_CORE_VER` is variable setting library version.  
`OPEN_API_SPEC_FILE_PATH` is variable which points to `tt_api.yaml` which is used
for generating endpoints definitions.

After exporting variables, execute commands:

```shell
make
. load_envs.sh
```

To build library:
```shell
make dist
```

To clean build:
```shell
make clean
```

Deployment process GitLab/GitHub
---
