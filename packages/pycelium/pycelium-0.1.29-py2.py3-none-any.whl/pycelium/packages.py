import sys
import os
import re
import hashlib
import random
import inspect
import shutil

sys.path.append(os.path.abspath('.'))

from .definitions import (
    DEB,
    DEB_FACTS,
    REAL,
    TARGET,
    PIP_FACTS,
    SERVICE_FACTS,
    setdefault,
)

from .shell import (
    assign,
    bspec,
    tspec,
    update,
    walk,
    glom,
    T,
    Finder,
)

from .action import Action


class PkgInstall(Action):
    HANDLES = tuple()

    def __init__(self, install=True, upgrade=False, *args, **kw):
        super().__init__(*args, **kw)
        self.install = install
        self.upgrade = upgrade


class DebPkgInstall(PkgInstall):
    """
    Install .deb packages using apt
    """

    HANDLES = DEB

    def __init__(self, timeout=60, *args, **kw):
        super().__init__(*args, **kw)
        self.timeout = timeout
        # self.cmdline = "env DEBIAN_FRONTEND=noninteractive;  {{ 'sudo ' if sudo else '' }} apt-get -y -o DPkg::Lock::Timeout={{ timeout}} {{ 'install' if install else 'remove' }} {{ name }}"
        self.cmdline = "{{ 'sudo ' if sudo else '' }} DEBIAN_FRONTEND=noninteractive apt-get -yq -o DPkg::Lock::Timeout={{ timeout}} {{ 'install' if install else 'remove' }} {{ name }}"

        # E: dpkg was interrupted, you must manually run 'sudo dpkg --configure -a' to correct the problem.
        self.add_interaction(
            '150_correct_error',
            r"E:\s+dpkg\s.*you\s+must\s+manually\s+run\s+'(?P<command>sudo.*?)'.*?correct\s+.*?problem\s*.*(\n|$)",
            'correct_error',
        )

        # shared with DebAptUpdate
        self.add_interaction(
            '200_get_repo_url',
            r'(?P<action>Hit|Get|Ign):(?P<seq>\d+)\s+(?P<url>[^\s]+).*?(\n|$)',
            #'set_object',
        )
        # (Reading database ... 35%
        # self.add_interaction(
        #'201_reading_db',
        # r'.*?Reading\s+database\.*?\d+\%(\n|$)',
        ##'set_object',
        # )
        self.add_interaction(
            '202_regular_activity',
            r'(?P<action>Reading|Preparing|Unpacking|Selecting|Setting|Processing).*(\n|$)',
            #'set_object',
        )
        self.add_interaction(
            '203_restarting_service',
            r'Restarting.*?(?P<service>\w+).*service.*?(?P<status>\w+)(\n|$)',
            #'set_object',
        )
        # 0 upgraded, 0 newly installed, 0 to remove and 323 not upgraded.
        self.add_interaction(
            '204_summary',
            r'(?P<upgraded>\d+)\s+upgraded.*?(?P<new>\d+).*?newly.*?(?P<removed>\d+).*?remove.*?(?P<not_upgraded>\d+).*',
            #'set_object',
        )

    async def _interact_correct_error(self, match, *args, **kw):
        # answer = self.default_executor.ctx.get('password')
        # if answer:
        # self.log.debug(f"provide sudo password: {'*' * len(answer)}")
        # self.answer(f'{answer}')
        # else:
        # self.log.error(
        # f"no sudo password is provided???, terminating action"
        # )
        # self.push(self.EV_KILL)

        fix_command = match.group(1)
        result = await self.execute(
            '{{sudo}}  {{ fix_command }}',
            #'{{sudo}} chown {{ owner }}:{{ group }} "{{ path }}"',
            sudo='sudo -S',
            **kw,
        )
        foo = 1


class PipPkgInstall(PkgInstall):
    """
    Install pip packages
    """

    HANDLES = tuple(['pip'])

    def __init__(self, upgrade=True, *args, **kw):
        super().__init__(*args, **kw)
        self.upgrade = update
        # uninstall using
        if self.install:
            self.cmdline = "{{ 'sudo' if sudo else '' }} pip3 {{ 'install' if install else 'uninstall' }} {{ '-U' if install and upgrade else '' }} {{ name }}"
        else:
            # sudo find  /usr/local/lib/ -type d -name 'pycelium*' -exec rm -rf {} \;
            self.cmdline = "sudo find  /usr/local/lib/ -type d -name '{{ name }}*' -exec rm -rf {} \;"

    def _populate_interactions(self):
        super()._populate_interactions()
        self.add_interaction(
            '300_already_satisfied',
            r'.*\s+already\s+satisfied:\s+(?P<already>[^\s]+).*?(\n|$)',
            #'default_response',
            # answer='yes',
        )


class DebRepository(Action):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.cmdline = "{{ 'sudo' if sudo else '' }} pip3 {{ 'install' if install else 'uninstall' }} {{ '-U' if upgrade else '' }} {{ name }}"

    def _populate_interactions(self):
        super()._populate_interactions()
        self.add_interaction(
            '300_already_satisfied',
            r'.*\s+already\s+satisfied:\s+(?P<already>[^\s]+).*?(\n|$)',
            #'default_response',
            # answer='yes',
        )


def test_deb_packages():
    from asyncio import run, wait, create_task, sleep, FIRST_COMPLETED, Queue
    from .shell import Reactor, DefaultExecutor

    reactor = Reactor()

    conn = DefaultExecutor()
    reactor.attach(conn)

    # stm = CoockieCutter()
    packages = 'python3-selenium yorick-svipc python3-okasha raysession python3-ulmo'
    for name in packages.split():
        stm = DebPkgInstall(name=name)
        reactor.attach(stm)

    run(reactor.main())
    foo = 1
    reactor = Reactor()

    conn = DefaultExecutor()
    reactor.attach(conn)
    for name in packages.split():
        stm = DebPkgInstall(name=name, install=False)
        reactor.attach(stm)

    run(reactor.main())
    foo = 1


def test_pip_packages():
    from asyncio import run, wait, create_task, sleep, FIRST_COMPLETED, Queue
    from .shell import Reactor, DefaultExecutor

    reactor = Reactor()

    conn = DefaultExecutor()
    reactor.attach(conn)

    # stm = CoockieCutter()
    packages = 'ppci voronoiville python-calamine'
    # packages = 'python-calamine'
    for name in packages.split():
        stm = PipPkgInstall(name=name)
        reactor.attach(stm)

    run(reactor.main())
    foo = 1
    reactor = Reactor()

    conn = DefaultExecutor()
    reactor.attach(conn)
    for name in packages.split():
        stm = PipPkgInstall(name=name, install=False)
        reactor.attach(stm)

    run(reactor.main())
    foo = 1
