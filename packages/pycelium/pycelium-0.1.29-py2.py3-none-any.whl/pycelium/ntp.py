from .action import Action
from .agent import Agent
from .packages import DebPkgInstall
from .gathering import GatherFact, DebListFact


from .definitions import LOCALTIME


class TimeControlFact(GatherFact):
    """

                       Local time: Fri 2023-06-16 18:00:14 CEST
               Universal time: Fri 2023-06-16 16:00:14 UTC
                     RTC time: Fri 2023-06-16 16:00:14
                    Time zone: Europe/Madrid (CEST, +0200)
    System clock synchronized: yes
                  NTP service: active
              RTC in local TZ: no




    """

    def __init__(self, merge=True, prefix=LOCALTIME, *args, **kw):
        super().__init__(merge=merge, prefix=prefix, *args, **kw)
        self.cmdline = "timedatectl"

    def _populate_interactions(self):
        super()._populate_interactions()
        self.add_interaction(
            '200_get_file_name',
            r'(?imsx)File:\s+(?P<key>.*?)(\n|$)',
            'new_group',
        )
        self.add_interaction(
            '200_timedatectl-timezone',
            ## r'\s*(?P<key>[^:]+):\s+(?P<value>[^\n]*)(\n|$)?',
            r'(?imsx)(?P<key>Time\s+zone):\s+(?P<value>[^\s]+).*?(\n|$)',
            'set_attribute',
        )
        self.add_interaction(
            '201_timedatectl-synchronized',
            ## r'\s*(?P<key>[^:]+):\s+(?P<value>[^\n]*)(\n|$)?',
            r'(?imsx)(?P<key>system\s+clock\s+synchronized):\s+(?P<value>[^\s]+).*?(\n|$)',
            'set_attribute',
        )
        self.add_interaction(
            '202_timedatectl-ntpservice',
            ## r'\s*(?P<key>[^:]+):\s+(?P<value>[^\n]*)(\n|$)?',
            r'(?imsx)(?P<key>(NTP\s+service)):\s+(?P<value>[^\s]+).*?(\n|$)',
            'set_attribute',
        )

        self.add_interaction(
            '203_timedatectl-rtc',
            ## r'\s*(?P<key>[^:]+):\s+(?P<value>[^\n]*)(\n|$)?',
            r'(?imsx)(?P<key>RTC\s+in\s+local\s+TZ):\s+(?P<value>[^\s]+).*?(\n|$)',
            'set_attribute',
        )


class TimeZoneAction(Action):
    """
    TBD
    """

    def __init__(self, timezone='etc/utc', *args, **kw):
        self._stop_no_seq = False  # wait until fibers have done
        super().__init__(*args, **kw)
        self.timezone = timezone
        self.cmdline = "timedatectl set-timezone {{ timezone }}"
        foo = 1


class SetNTPAction(Action):
    """
    TBD
    """

    def __init__(self, timezone='etc/utc', *args, **kw):
        self._stop_no_seq = False  # wait until fibers have done
        super().__init__(*args, **kw)
        self.timezone = timezone
        self.cmdline = "timedatectl set-timezone {{ timezone }}"
        foo = 1
