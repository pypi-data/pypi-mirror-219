from fire import Fire

from burla.config import set_api_key
from burla.remote_parallel_map import remote_parallel_map


def init_cli():
    Fire({"set_api_key": set_api_key})
