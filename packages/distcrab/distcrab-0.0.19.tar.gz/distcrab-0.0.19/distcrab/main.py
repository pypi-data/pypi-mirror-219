#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdout
from io import StringIO, FileIO, BytesIO
from pathlib import PurePosixPath
from socket import socket
from urllib.request import urlopen
from tarfile import open
from paramiko import Transport, SSHException, SFTPClient
from git.cmd import Git
from logging import getLogger
from os.path import basename

from queue import Queue
from threading import Thread

logger = getLogger()

class Src():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        kwargs = self.kwargs
        if kwargs.get('firmware'):
            location = kwargs.get('firmware')
            io = BytesIO(urlopen(location).read())
        elif kwargs.get('version'):
            version = kwargs.get('version')
            location = f'''http://192.168.21.1:5080/APP/develop/develop/update/industry/crab/dists/crab-{version}.tar.xz'''
            io = BytesIO(urlopen(location).read())
        elif kwargs.get('branch'):
            version = BytesIO(urlopen(f'''http://192.168.21.1:5080/APP/develop/develop/update/industry/crab/heads/{kwargs.get('branch')}.txt''').read()).read().decode()
            location = f'''http://192.168.21.1:5080/APP/develop/develop/update/industry/crab/dists/crab-{version}.tar.xz'''
            io = BytesIO(urlopen(location).read())
        else:
            location = f'''var/crab-{Git().describe(tags=True, abbrev=True, always=True, long=True, dirty=True)}.tar.xz'''
            io = BytesIO(FileIO(location).read())
        self.location = location
        self.io = io

    def __iter__(self):
        yield (PurePosixPath('/tmp/firmware.bin'), self.io)

    def dump(self):
        stdout.buffer.write(self.io.read())

    def download(self):
        FileIO(basename(self.location), 'wb').write(self.io.read())
        logger.info(self.kwargs)
        logger.info(basename(self.location))

class Archive():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __iter__(self):
        kwargs = self.kwargs
        tar = open(mode='r:xz', fileobj=Src(**kwargs).io)
        for tarinfo in tar.getmembers():
            file = tar.extractfile(tarinfo)
            if file:
                yield (PurePosixPath(f'''/usr/local/crab/{tarinfo.name}'''), file)
        tar.close()

class Client():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        sock = socket()
        sock.connect((kwargs.get('ip', '192.168.1.200'), kwargs.get('port', 22)))
        transport = Transport(sock)
        transport.start_client()
        try:
            if not kwargs.get('password'):
                raise SSHException
            transport.auth_password(kwargs.get('username', 'root'), kwargs.get('password', 'elite2014'))
        except SSHException:
            transport.auth_none(kwargs.get('username', 'root'))
        self.transport = transport

    def putfo(self, files):
        client = SFTPClient.from_transport(self.transport)
        for (path, content) in files:
            try:
                client.chdir(str(path.parent))
            except IOError:
                client.mkdir(str(path.parent))
            queue = Queue(maxsize=1)
            JOB_DONE = object()
            def callback(transferred, total):
                queue.put('{0:.3f}\n'.format(transferred / total, 2).encode())
            def task():
                client.putfo(content, str(path), content.getbuffer().nbytes, callback)
                queue.put(JOB_DONE)
            thread = Thread(target=task)
            thread.start()
            while True:
                chunk = queue.get()
                if chunk is JOB_DONE:
                    break
                yield chunk
            thread.join()

    def exec_command(self, commands):
        for command in commands:
            try:
                yield command
                channel = self.transport.open_session()
                channel.set_combine_stderr(True)
                channel.exec_command(command.decode())
                line = b''
                while True:
                    self.transport.send_ignore()

                    if channel.recv_ready():
                        char = channel.recv(1)
                        line += char
                        if char == b'\n':
                            yield line
                            line = b''
                    if channel.exit_status_ready():
                        break
                channel.close()
            except EOFError:
                pass
        return self

def distcrab(download=False, dump=False, ip='192.168.1.200', port=22, username='root', password=None, firmware=None, version=None, branch=None):
    src = Src(firmware=firmware, version=version, branch=branch)
    if download:
        src.download()
    elif dump:
        src.dump()
    elif firmware:
        client = Client(ip=ip, port=port, username=username, password=password)
        yield from client.putfo(src)
        yield from client.exec_command([
            b'/bin/mount -o rw,remount / && /bin/sync && /rbctrl/prepare-update.sh /tmp && /etc/init.d/rbctrl.sh stop && PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin /var/volatile/update/chrt-sqfs.sh /update/updater /mnt/tmp/update-final.sh'
        ])
    else:
        client = Client(ip=ip, port=port, username=username, password=password)
        yield from client.exec_command([
            b'/usr/local/bin/elite_local_stop.sh',
        ])
        yield from client.putfo(src)
        yield from client.exec_command([
            b'/bin/rm -rf /usr/local/crab/ && /bin/mkdir -p /usr/local/crab/ && /bin/sync && /bin/tar -xvJf /tmp/firmware.bin -C /usr/local/crab/ && /bin/rm -rf /tmp/firmware.bin && /bin/sync && /usr/local/bin/elite_local_start.sh',
        ])
