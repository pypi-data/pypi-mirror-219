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


class NetPlanAction(Action):
    def __init__(
        self,
        path='/etc/netplan/00-installer-config.yaml',
        enable=True,
        sudo=True,
        *args,
        **kw,
    ):
        super().__init__(sudo=sudo, enable=True, *args, **kw)
        self.path = path
        self.enable = enable

    async def _seq_10_netplan_apply(self, *args, **kw):
        """
        sysctl -w net.ipv4.ip_forward=1
        """
        result = await self.execute(
            '{{ {{sudo}} netplan apply  if enable else echo "" }}',
            sudo='sudo -S',
        )
        return result
