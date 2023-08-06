import re
import os
import yaml

import asyncio
from datetime import datetime
from glom import glom

import click

from pycelium.shell import Reactor, DefaultExecutor
from pycelium.pastor import Pastor

from pycelium.tools.cli.main import main, CONTEXT_SETTINGS
from pycelium.tools.cli.config import config, banner
from pycelium.tools.cli.run import run

from pycelium.tools.mixer import merge_yaml
from pycelium.tools.inventory import analyze_node
from pycelium.tools.persistence import find_files

from ..tools import extend_config, build_deltas, analyze_args


@run.command()
@click.option("--uri", default=None)
@click.option("--include", multiple=True)
@click.option("--tag", multiple=True)
@click.pass_obj
def pastor(env, uri, include, tag):
    config.callback()
    extend_config(env)

    analyze_args(env, uri, include, tag)

    ctx = dict(env.__dict__)

    if not tag:
        host = ctx['host']
        hostname, data, tags = analyze_node(ctx, host)

    includes = ctx.get('includes', [])
    tags.append('base')
    for t in tags:
        for t in re.findall(r'\w+', t):
            includes.append(f'(.*?\.)?{t}\.yaml')

    reactor = Reactor(env=ctx, max_runtime=-1)
    conn = DefaultExecutor(**ctx)
    reactor.attach(conn)

    stm = Pastor(daemon=False)
    reactor.attach(stm)

    # magic ...
    asyncio.run(reactor.main())
