import logging
import asyncio
import sys
from importlib import import_module
from aiosnow import Client


# Config
ADDRESS = "<instance_name>.service-now.com"
CREDENTIALS = "<username>", "<password>"
DEBUG = True


if len(sys.argv) != 2:
    print(
        f"Usage: run.py <path.to.example>\nExample: python3 examples/run.py table.read.nested"
    )
    sys.exit(1)


def run_example(path, client):
    module = import_module(path)
    if not hasattr(module, "main"):
        raise AttributeError(f"Missing member main() in example {path}")

    example = import_module(path).main(client)
    asyncio.run(example)


if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

run_example(sys.argv[1], client=Client(ADDRESS, basic_auth=CREDENTIALS))
