import asyncssh
import asyncio
from .tools import parse_uri, expandpath

from .shell import DefaultExecutor
from .action import Action


class CopyID(Action):
    """ """

    def __init__(self, *args, **kw):
        self._stop_no_seq = False  # wait until fibers have done
        super().__init__(*args, **kw)

    # --------------------------------------------------
    # Coded as sequence: # TODO: review
    # --------------------------------------------------
    async def _seq_10_copyid_local(self, *args, **kw):
        chcwd = expandpath('.')
        self.local = DefaultExecutor(host='localhost', chcwd=chcwd)
        self.reactor.attach(self.local)

        return True

    async def _seq_20_copyid_exec(self, *args, **kw):
        """
        ssh-copy-id agp@wsentinel
        /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
        /usr/bin/ssh-copy-id: INFO: 7 key(s) remain to be installed -- if you are prompted now it is to install the new keys
        agp@wsentinel's password:"""
        # get current executor
        executor = await self.is_connected()

        # prepare remote target
        kw.update(executor.connection.__dict__)
        user = kw.get('_user')
        password = kw.get('_password')
        host = kw.get('_host')
        if user:
            xhost = f"{user}@{host}"
        else:
            xhost = host
        cmdline = f"ssh-copy-id {xhost}"

        # we need to make interfactive some often
        conn = self.local.connection
        rootpass = '123456'

        async with conn.create_process(
            cmdline, stderr=asyncssh.STDOUT
        ) as process:
            print(f"{cmdline} sent, waiting response")
            response = ""
            recv = True
            while recv:
                recv = await process.stdout.read(1024)
                print(recv)
                if recv:
                    response += recv.casefold()
                    if "password:" in response:
                        break
                await asyncio.sleep(0.1)
            # while "password" not in await process.stdout.read(1024).casefold():
            #     await asyncio.sleep(1)
            print(f"{cmdline}: sending rootpass")
            process.stdin.write(rootpass + "\n")
            process.stdin.write_eof()
            print(f"{cmdline}: rootpass sent, waiting response")
            whoami = (await process.stdout.read()).strip()
            print(">>", whoami)
            return whoami == "root"

        process = await local.create_process(cmdline, stderr=STDOUT)

        result = await self.local.exec_many(cmdline, sudo=False)
        self.local._term()
        return result
