import logging
import asyncio
from importlib import import_module
from snow import Snow


logging.basicConfig(level=logging.DEBUG)

# Config
ADDRESS = "<instance_name>.service-now.com"
CREDENTIALS = "<username>", "<password>"
EXAMPLE = "read.nested"


def run_example(path):
    module = import_module(path)
    if not hasattr(module, "main"):
        raise AttributeError(f"Missing member main() in example {path}")

    example = import_module(path).main(app)
    asyncio.run(example)


app = Snow(ADDRESS, basic_auth=CREDENTIALS)
run_example(EXAMPLE)
