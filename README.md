# The Items Service

## Overview
The Items Service was created as an exercise.
It implements a REST API in Python for accessing and manipulating a storage of items.
Each item has a *name* which is unique and a *description*.
Items can be *created*, *queried*, *updated*, *deleted* and *listed*.

The service itself can be found in the `service` directory.
Also, a simple command line client can be found in the `client` directory.

## Testing
`functional_tests.py` provides functional (end-to-end) tests for the service and the client.

Redis should already be installed and running.
```bash
pip install -r test_requirements.txt

# set env vars for Redis
# you should customize these according to your environment
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
# !!! make sure that your database has no important data in it !!!

# choose an unused port
export SERVICE_PORT=11111

python functional_tests.py
```

Unit tests for the service and the client can be found in their respective directories.

---

For more information, see `client/README.md` and `service/README.md`.
