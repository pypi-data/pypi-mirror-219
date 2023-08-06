import asyncio
import random
import re
import os
import time
import yaml
import click

from glom import glom

# from pycelium.action import Action
from pycelium.definitions import HOST_CONFIG_FILE

from pycelium.installer import Installer
from pycelium.shell import Reactor, DefaultExecutor, LoopContext


from pycelium.tools.inventory import (
    INVENTORY_ROOT,
    explore_single_host,
    get_mac,
    get_host_tags,
    install_node,
)


from pycelium.tools import soft, expandpath
from pycelium.tools.containers import search, simplify
from pycelium.tools.persistence import find_files
from pycelium.tools.cli.inventory import (
    inventory,
    credentials,
    INVENTORY_ROOT,
    explore_host,
    explore_single_host,
    get_mac,
    get_host_tags,
    save_yaml,
    save_blueprint,
)
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
from ..tools import extend_config, analyze_args


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--network", multiple=True)
@click.option("--user", multiple=True)
@click.option("--password", multiple=True)
@click.option("--shuffle", default=True, type=bool)
@click.option("--cycles", default=1, type=int)
@click.option("--inventory", default=INVENTORY_ROOT, type=str)
@click.pass_obj
def install(env, network, user, shuffle, password, cycles, inventory):
    """
    - [ ] Gather information similar as explore
    - [ ] Install single node


    Note: Does NOT change the node name by now, bettr use explore + fish
    """
    config.callback()
    extend_config(env)

    conquered = dict()
    cfg = dict(env.__dict__)

    while cycles != 0:
        print(f"{YELLOW} Remain cycles: {cycles}{RESET}")
        cycles -= 1

        if not user:
            user = cfg.get('user') or user

        if not password:
            password = cfg.get('password', password)

        print(f"network: {network}")
        print(f"user: {user}")

        for ctx in credentials(network, user, shuffle, password, cfg):
            soft(ctx, **cfg)
            print("{_progress:.2%} {_printable_uri:>40}".format_map(ctx))
            host = ctx['host']
            if host in conquered:
                print(f"{host} is alredy conquered! :), skiping")
                continue

            result = install_node(ctx, host)
            if result:
                hostname, data, status = result
                if status in ('ok',):
                    conquered[hostname] = data
                    data, path = save_blueprint(
                        data, default_host=hostname, top=inventory, **ctx
                    )

        time.sleep(2)

    foo = 1

    return True  # so obsolete inventory file can be deleted


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--target", default='./templates')
@click.option("--source", default='~')
@click.option(
    "--include", default='wireguard/.*?/(?P<name>(?P<host>venoen\d+).conf)'
)
@click.option(
    "--pattern", default='{target}/{host}/wireguard/wg-centesimal.conf'
)
@click.option("--overwrite", is_flag=True, default=False)
@click.pass_obj
def cpwireguard(env, target, source, include, pattern, overwrite):
    """Copy WG config files from other locations"""
    config.callback()
    folders = [source]
    includes = [include]

    found = find_files(
        folders=folders,
        includes=includes,
    )

    for i, path in enumerate(found):
        print(f"{PINK}---> {path}{RESET}")
        for reg in includes:
            m = re.search(reg, path)
            if m:
                d = m.groupdict()
                d['target'] = target
                dest = pattern.format_map(d)
                if os.path.exists(dest) and not overwrite:
                    print(f"Skipping: {dest}, already exists")
                    continue

                print(dest)
                text = open(path).read()
                # print(text)
                text = translate_wg_config(text)
                # print(text)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                open(dest, 'wt').write(text)

                foo = 1

    foo = 1


# -----------------------------------------------
# rename clean nodes based on somw HW values
# -----------------------------------------------


@inventory.command()
# @click.argument('filename', default='sample.gan')
@click.option("--network", multiple=True)
@click.option("--user", multiple=True)
@click.option("--password", multiple=True)
@click.option("--include", multiple=True, default=['user.*.yaml'])
@click.option("--shuffle", default=True, type=bool)
@click.option("--cycles", default=1, type=int)
@click.pass_obj
def fish(env, network, user, shuffle, password, include, cycles):
    """
    - [ ] Gather information similar as explore
    - [ ] Install single node
    """
    config.callback()
    extend_config(env)

    conquered = dict()
    cfg = dict(env.__dict__)

    top = expandpath(INVENTORY_ROOT)
    while cycles != 0:
        print(f"{YELLOW} Remain cycles: {cycles}{RESET}")
        cycles -= 1

        found = find_files(folders=[top], includes=include)
        banner("Unassigned hosts", found)

        host_name_cfg = HOST_CONFIG_FILE
        host_names = yaml.load(
            open(host_name_cfg).read(), Loader=yaml.Loader
        )

        host_criteria = {}
        for host, criteria in host_names.items():
            blueprint = {}
            for k, v in criteria.items():
                if '*' not in k:
                    k = f'.*{k}'
                v = str(v)
                blueprint[k] = v
            host_criteria[host] = blueprint
        if shuffle:
            # process list in random order
            found = list(found)
            random.shuffle(found)

            host_criteria = list(host_criteria.items())
            random.shuffle(host_criteria)
            host_criteria = {k: v for k, v in host_criteria}
            foo = 1

        for path in found:
            data = yaml.load(open(path).read(), Loader=yaml.Loader)
            for host, blueprint in host_criteria.items():
                if host in (
                    #'venoen243',
                    #'venoen168',
                ):
                    continue
                result = search(data, blueprint)
                result = simplify(result)
                if result:
                    # hostname found!
                    # ctx = dict(env.__dict__)
                    ctx = data.get('env', {})
                    soft(ctx, **cfg)

                    print(f"{GREEN}renaming node to: {host}{RESET}")
                    rename_host(ctx, hostname=host)

                    print(f"{GREEN}reload node facts: {host}{RESET}")
                    data, new_path = explore_single_host(
                        ctx, host, save=True
                    )

                    print(f"{YELLOW}installing new node: {host}{RESET}")
                    tags = get_host_tags(data)
                    ok = install_single_node(tags, ctx)
                    if ok:
                        if path != new_path:
                            print(
                                f"{BLUE}deleting obsolete inventory file: {path}{RESET}"
                            )
                            os.unlink(path)
                        else:
                            print(
                                f"{GREEN}, preserving inventory file: {path}{RESET}"
                            )

                    # rename inventory name
                    foo = 1
            foo = 1

        time.sleep(15)

    return


def translate_wg_config(text):
    rules = {
        r'(Address\s+=\s+[\d\.]+)(/16)': r'\1/32',
        r'(AllowedIPs\s+=\s+10.220)(.2.33)/(16|32)': r'\1.0.0/16',
    }
    for pattern, repl in rules.items():
        text = re.sub(pattern, repl, text)

    return text
