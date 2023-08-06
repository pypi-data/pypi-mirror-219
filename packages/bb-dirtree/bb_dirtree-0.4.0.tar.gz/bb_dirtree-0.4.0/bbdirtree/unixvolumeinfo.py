import os, shlex
from subprocess import run

class VolumeInfo:
    """
    Get file system information on unix systems
    """
    disks      = {}
    partitions = {}

    def __init__(self):
        disks = {}
        x = run(['lsblk', '-P', '-o', 'TYPE,LABEL,FSTYPE,MODEL,FSSIZE,NAME,MOUNTPOINT,UUID,PATH'], capture_output = True )
        for out in x.stdout.decode().strip().split('\n'):
            data = dict([( i[0], i[1].replace('"', '') ) for i in [ d.split('=') for d in shlex.split(out) ]])
            if data['TYPE'] == 'disk':
                data.pop('TYPE')
                data.pop('LABEL')
                data.pop('FSTYPE')
                data.pop('FSSIZE')
                data.pop('MOUNTPOINT')
                data.pop('UUID')
                self.disks[ data['NAME'] ] = data
            elif data['TYPE'] == 'part':
                data.pop('TYPE')
                data.pop('MODEL')
                self.partitions[ data['NAME'] ] = data

        for k, v in self.partitions.items():
            name = v['NAME']
            if not name:
                continue
            for d in self.disks:
                if name.startswith(d):
                    self.partitions[k]['DISK'] = self.disks[d]

    def byMountPoint(self):
        R = {}
        for k, v in self.partitions.items():
            if v['MOUNTPOINT']:
                R[ v['MOUNTPOINT'] ] = v

        return R

    def byUuid(self):
        for k, v in self.partitions.items():
            if v['UUID']:
                R[ v['UUID'] ] = v

        return R

    def byName(self):
        return self.partitions

    def fromPath(self, path):
        try:
            path = os.path.abspath( path )
        except Exception as E:
            log.exception(E)
            raise E

        common = ( '', {} )
        for k, v in self.partitions.items():
            if not v['MOUNTPOINT'] or v['MOUNTPOINT'] == '[SWAP]':
                continue
            if path.startswith( v['MOUNTPOINT'] ):
                if len( v['MOUNTPOINT'] ) > len( common[0] ):
                    common = ( v['MOUNTPOINT'], self.partitions[k] )

        if not common[1]:
            log.error(f"Couldn't find partition for '{path}'")

        return common[1]
