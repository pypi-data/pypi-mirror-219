import getpass
import os
import random
import re

import yaml

import asyncio

from glom import glom


from pycelium.containers import gather_values, search, simplify
from pycelium.definitions import HOST_CONFIG_FILE
from pycelium.installer import Installer
from pycelium.scanner import HostInventory, RenameHost
from pycelium.shell import Reactor, DefaultExecutor, LoopContext
from pycelium.tools import parse_uri, soft
from pycelium.tools.cli.config import (
    config,
    banner,
    RED,
    RESET,
    BLUE,
    PINK,
    YELLOW,
    GREEN,
)
from pycelium.tools.sequencers import expand_network

from .mixer import save_yaml

INVENTORY_ROOT = 'inventory/'


def extend_config(env):
    """Extend the config environment with some default folders."""
    cfg = env.__dict__

    # folders for searching
    parent = os.path.join(*os.path.split(os.path.dirname(__file__))[:-1])

    for p in [os.path.abspath("."), parent]:
        env.folders[p] = None


def explore_host(ctx, **kw):
    """Explore a single host"""
    with LoopContext():
        reactor = Reactor(env=ctx)
        conn = DefaultExecutor(retry=-1, **ctx)
        reactor.attach(conn)

        stm = HostInventory(daemon=False)
        reactor.attach(stm)

        asyncio.run(reactor.main())
        return reactor.ctx


def explore_single_host(ctx, host, top=None, save=True):
    data = explore_host(ctx)

    mac = get_mac(data)
    if mac:
        if save:
            data, path = save_blueprint(data, default_host=host, **ctx)
            return data, path
        return data, None
    return {}, None


def save_blueprint(data, default_host='unknown', top='inventory', **ctx):
    # ABAILABLE = set('')
    mac = get_mac(data)
    if mac:
        mac = mac.replace(':', '')

        ctx['observed_hostname'] = observed_hostname = glom(
            data, 'real.etc.hostname', default=default_host
        )

        # data = data.get('real')
        tags = get_host_tags(data)
        tags.append(observed_hostname)
        # _tags = '/'.join(tags)
        # path = f"{top}/{_tags}/{observed_hostname}.{mac}.yaml"
        path = f"{top}/{observed_hostname}.{mac}.yaml"
        data['_context'] = ctx
        data['_tags'] = tags

        save_yaml(data, path)
        return data, path
    return {}, None


def rename_host(ctx, hostname, **kw):
    """Rename a single host"""
    with LoopContext():
        reactor = Reactor(env=ctx)

        conn = DefaultExecutor(**ctx)
        reactor.attach(conn)

        # stm = Settler(daemon=False)
        stm = RenameHost(hostname=hostname)
        reactor.attach(stm)

        asyncio.run(reactor.main())
        return reactor.ctx


#  ---------------------------------------------


# def get_or_create_eventloop():
# try:
# return asyncio.get_running_loop()
# except RuntimeError as ex:
# if "There is no current event loop in thread" in str(ex):
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# return asyncio.get_event_loop()


def get_mac(data):
    specs = {
        '.*enp.*mac.*': None,
        '.*enp.*type.*': 'ether',
        '.*wlo.*mac.*': None,
        '.*wlo.*type.*': 'ether',
        '.*ens.*mac.*': None,
        '.*ens.*type.*': 'ether',
    }
    blueprint = gather_values(data, **specs)

    # blueprint = deindent_by(blueprint, IP_INFO)
    if 'mac' in blueprint:
        if blueprint.get('type') in ('ether',):
            return blueprint.get('mac')

    keys = list(blueprint)
    keys.sort()
    for iface in keys:
        info = blueprint.get(iface)
        if info.get('type') in ('ether',):
            return info.get('mac')


HW_TAGGING_FILE = 'hardware.tagging.yaml'


def _get_host_tags(data):
    """Try to figure out which kind of node is"""
    blueprint = {
        r'processor.0.*address_sizes': '36\s+bits',
        r'processor.0.*model_name': '.*celeron.*',
        r'processor.0.*siblings': '4',
        r'processor.0.*stepping': '8',
        r'ip.enp1s0.*type': 'ether',
    }
    keys = ['address_sizes', 'model_name', 'siblings', 'stepping', 'type']

    tags = ['node', 'venoen', 'ntp']

    block = {
        'blueprint': blueprint,
        'keys': keys,
        'tags': tags,
    }

    info = {}
    info['venoen'] = block

    yaml.dump(
        info, stream=open('hardware.tagging.yaml', 'w'), Dumper=yaml.Dumper
    )

    info = gather_values(data, **blueprint)

    return


def get_host_tags(data):
    """Try to figure out which kind of node is 'data'

    Datase looks like:

    venoen:
        blueprint:
          ip.enp1s0.*type: ether
          processor.0.*address_sizes: 36\s+bits
          processor.0.*model_name: .*celeron.*
          processor.0.*siblings: '4'
          processor.0.*stepping: '8'
        keys:
        - address_sizes
        - model_name
        - siblings
        - stepping
        - type
        tags:
        - node
        - venoen



    """
    db = yaml.load(open(HW_TAGGING_FILE), Loader=yaml.Loader)
    tags = set()
    for name, info in db.items():
        blueprint = info['blueprint']
        values = gather_values(data, **blueprint)
        keys = set(info['keys'])
        if keys.issubset(values):
            tags.update(info['tags'])
            tags.add(name)
    tags = list(tags)
    tags.sort()
    return tags


def gen_credentials(network, user, password=[], env={}, shuffle=False):
    used = set()
    for pattern in network:
        seq = expand_network(pattern)  # iterator for erally large ranges

        # print(f"Exploring: {pattern}  --> {total} items")
        for addr in seq:
            addr = '.'.join(addr)
            for i, cred in enumerate(user):
                # test initial uri
                uri = f'{cred}@{addr}'
                if False and uri not in used:  # TODO: remove False
                    yield uri
                    used.add(uri)

                # test without passwd and default password
                m = re.match(r'(?P<user>[^:]+)(?P<password>.*)?', cred)
                if m:
                    _user, _password = m.groups()
                    # test adding no passwd
                    uri = f'{_user}@{addr}'
                    if False and uri not in used:  # TODO: remove False
                        yield uri
                        used.add(uri)

                for _passwd in password:
                    #  test with default passwd
                    uri = f'{_user}:{_passwd}@{addr}'
                    if uri not in used:
                        yield uri
                        used.add(uri)

                _password = env.get('password')
                if _password:
                    #  test with default passwd
                    uri = f'{_user}:{_password}@{addr}'
                    if uri not in used:
                        yield uri
                        used.add(uri)


def credentials(network, user, shuffle=False, password=None, env={}, **kw):
    """
    password is the default password when is not provided
    """
    if isinstance(network, str):
        network = [network]

    if isinstance(user, str):
        user = [user]

    if not user:
        user = [getpass.getuser()]

    if isinstance(password, str):
        password = [password]

    total = 1
    if shuffle:
        universe = list(
            gen_credentials(network, user, password, env, shuffle)
        )
        random.shuffle(universe)
        total = len(universe)
    else:
        total = len(user)
        for pattern in network:
            seq = expand_network(pattern)
            total *= seq.total

        universe = gen_credentials(network, user, password, env, shuffle)

    for i, uri in enumerate(universe):
        ctx = parse_uri(uri)
        ctx['uri'] = uri
        ctx['_progress'] = i / total
        soft(ctx, user=getpass.getuser(), host='localhost')

        if ctx.get('password'):
            # ctx['shadow'] = ':' + '*' * len(ctx['password'])
            ctx['shadow'] = ':' + str(ctx.get('password'))

        else:
            ctx['shadow'] = ''

        ctx['_printable_uri'] = "{user}{shadow}@{host}".format_map(ctx)

        yield ctx


def get_hostname_from_blueprint(data):
    # 1. build host_criteria searh from `hostnames.yaml`
    host_name_cfg = HOST_CONFIG_FILE
    host_names = yaml.load(open(host_name_cfg).read(), Loader=yaml.Loader)

    host_criteria = {}
    for host, criteria in host_names.items():
        blueprint = {}
        for k, v in criteria.items():
            if '*' not in k:
                k = f'.*{k}'
            v = str(v)
            blueprint[k] = v
        host_criteria[host] = blueprint

    # 2. search the host that matches blueprint
    for host, blueprint in host_criteria.items():
        result = search(data, blueprint)
        result = simplify(result)
        if result:
            return host


def install_single_node(tags, ctx):
    with LoopContext():
        includes = ctx.get('includes', [])
        ctx.setdefault('max_runtime', 900)

        tags.append('base')
        for t in tags:
            for t in re.findall(r'\w+', t):
                includes.append(f'(.*?\.)?{t}\.yaml')

        reactor = Reactor(env=ctx)

        conn = DefaultExecutor(**ctx)
        reactor.attach(conn)

        stm = Installer(daemon=False)
        reactor.attach(stm)

        # magic ...
        asyncio.run(reactor.main())

    return reactor.status


def analyze_node(ctx, host):
    # 1. explore node and write its yaml

    data, path = explore_single_host(ctx, host)
    mac = get_mac(data)
    if not mac:
        # print(f"{RED}can't find mac address for node '{host}'{RESET}")
        return

    ctx['observed_hostname'] = observed_hostname = glom(
        data, 'real.etc.hostname', default=host
    )
    # 2. get realname from hostnames.yaml HW matching
    hostname = get_hostname_from_blueprint(data)
    if not hostname:
        print(f"{RED}can't find node '{host}' in hostname.yaml {RESET}")
        hostname = observed_hostname
        foo = 1

    # 3. rename node
    if hostname and observed_hostname != hostname:
        print(
            f"{YELLOW}renamin node '{host}': '{observed_hostname}' --> '{hostname}'{RESET}"
        )
        rename_host(ctx, hostname=hostname)

    # 4. install node
    tags = get_host_tags(data)
    # tags = data['_tag']
    tags.append(observed_hostname)
    return hostname, data, tags


def install_node(ctx, host):
    """
    1. explore node and write its yaml
    2. get realname from hostnames.yaml HW matching
    3. rename node
    4. install node
    """
    info = analyze_node(ctx, host)
    if info:
        hostname, data, tags = info
        ctx['real_hostname'] = hostname
        status = install_single_node(tags, ctx)
        return hostname, data, status
