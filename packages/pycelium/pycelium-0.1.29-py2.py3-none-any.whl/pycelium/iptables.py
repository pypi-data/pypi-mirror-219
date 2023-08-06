import time


import yaml
import semver
import re
from glom import glom, assign

from pycelium.tools.containers import (
    simplify,
    merge,
    option_match,
    gather_values,
)

from .definitions import (
    PIP_FACTS,
    MODEM_FACTS,
    MODEM_ID_FACTS,
    CONNECTION_STATUS,
    DEVICE_STATUS,
    REAL,
    TARGET,
    ETC,
)

from .shell import (
    bspec,
    Finder,
)

from .action import Action
from .agent import Agent
from .service import Service
from .gathering import GatherFact


class IpTablesAction(Action):
    def __init__(
        self,
        path='/etc/iptables/rules.v4',
        enable=True,
        sudo=True,
        *args,
        **kw,
    ):
        super().__init__(sudo=sudo, enable=True, *args, **kw)
        self.path = path
        self.enable = enable

    async def _seq_10_iptables_forward(self, *args, **kw):
        """
        sysctl -w net.ipv4.ip_forward=1
        """
        result = await self.execute(
            '{{sudo}} sysctl -w net.ipv4.ip_forward={{ 1 if enable else 0 }}',
            sudo='sudo -S',
        )
        return result

    async def _seq_20_iptables_enable(self, *args, **kw):
        """
        iptables-restore < {{ path }}
        """
        if self.enable:
            result = await self.execute("iptables-restore < {{ path }}")
        return True
