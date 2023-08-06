import random
import re
import os
import getpass
import yaml
import time


import asyncio

import click

from glom import glom


from .main import main, CONTEXT_SETTINGS
from .config import (
    config,
    banner,
    RESET,
    BLUE,
    PINK,
    YELLOW,
    GREEN,
)


from .. import parse_uri, soft, expandpath
from ..containers import gather_values, deindent_by
from ..mixer import save_yaml
from ..persistence import find_files
from ..inventory import *

from pycelium.definitions import IP_INFO, REAL, ETC
from pycelium.shell import Reactor, DefaultExecutor, LoopContext
from pycelium.scanner import HostInventory
from pycelium.installer import Installer
from pycelium.pastor import Pastor


@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def inventory(env):
    # banner("User", env.__dict__)
    pass


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--network", multiple=True)
@click.option("--user", multiple=True, default=['user'])
@click.option("--password", multiple=True, default=['123456'])
@click.option("--shuffle", default=True, type=bool)
@click.option("--cycles", default=1, type=int)
@click.pass_obj
def explore(env, network, user, shuffle, password, cycles):
    """
    - [ ] get users from config yaml file or command line
    """
    config.callback()

    conquered = dict()
    ctx = dict(env.__dict__)

    top = expandpath(INVENTORY_ROOT)
    while cycles != 0:
        print(f"{YELLOW} Remain cycles: {cycles}{RESET}")
        cycles -= 1
        print(f"network: {network}")
        print(f"user: {user}")
        for ctx in credentials(
            network, user, shuffle, password, env.__dict__
        ):
            print("{_progress:.2%} {_printable_uri:>40}".format_map(ctx))
            host = ctx['host']
            if host in conquered:
                print(f"{host} is alredy conquered! :), skiping")
                continue

            data, path = explore_single_host(ctx, host)
            if data:
                ctx['observed_hostname'] = observed_hostname = (
                    data.get('observed_hostname') or host
                )
                conquered[host] = data
                conquered[observed_hostname] = data

                foo = 1
        time.sleep(10)


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--email", default=None)
@click.option("--cost", default=30)
@click.pass_obj
def show(env, email, cost=0):
    config.callback()
    top = expandpath(INVENTORY_ROOT) + '/'
    found = find_files(top, includes=['.*yaml'])
    lines = {k.split(top)[-1]: v for k, v in found.items()}

    banner("Inventory", lines=lines)
    foo = 1


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--email", default=None)
@click.option("--cost", default=30)
@click.pass_obj
def query(env, email, cost=0):
    raise NotImplementedError("not yet!")
