import os
import ctypes as ct
from ctypes import wintypes
from enum import IntFlag

class FSFlags(IntFlag):
    FILE_CASE_SENSITIVE_SEARCH        = 0x00000001
    FILE_CASE_PRESERVED_NAMES         = 0x00000002
    FILE_UNICODE_ON_DISK              = 0x00000004
    FILE_PERSISTENT_ACLS              = 0x00000008
    FILE_FILE_COMPRESSION             = 0x00000010
    FILE_VOLUME_QUOTAS                = 0x00000020
    FILE_SUPPORTS_SPARSE_FILES        = 0x00000040
    FILE_SUPPORTS_REPARSE_POINTS      = 0x00000080
    FILE_VOLUME_IS_COMPRESSED         = 0x00008000
    FILE_SUPPORTS_OBJECT_IDS          = 0x00010000
    FILE_SUPPORTS_ENCRYPTION          = 0x00020000
    FILE_NAMED_STREAMS                = 0x00040000
    FILE_READ_ONLY_VOLUME             = 0x00080000
    FILE_SEQUENTIAL_WRITE_ONCE        = 0x00100000
    FILE_SUPPORTS_TRANSACTIONS        = 0x00200000
    FILE_SUPPORTS_HARD_LINKS          = 0x00400000
    FILE_SUPPORTS_EXTENDED_ATTRIBUTES = 0x00800000
    FILE_SUPPORTS_OPEN_BY_FILE_ID     = 0x01000000
    FILE_SUPPORTS_USN_JOURNAL         = 0x02000000
    FILE_SUPPORTS_BLOCK_REFCOUNTING   = 0x08000000
    FILE_DAX_VOLUME                   = 0x20000000

class VolumeInfo:
    """
    Get volume information for windows devices
    """
    mount_point = ''
    disk_label  = ''
    fs_type     = ''
    max_length  = 0
    flags       = []
    serial      = 0


    def __init__(self, drive_letter):
        w   = wintypes
        dll = ct.WinDLL('kernel32',use_last_error=True)

        dll.GetVolumeInformationW.argtypes = w.LPCWSTR,w.LPWSTR,w.DWORD,w.LPDWORD,w.LPDWORD,w.LPDWORD,w.LPWSTR,w.DWORD
        dll.GetVolumeInformationW.restype  = w.BOOL
        dll.GetVolumeInformationW.errcheck = self.validate

        volumeNameBuffer     = ct.create_unicode_buffer(w.MAX_PATH + 1)
        fileSystemNameBuffer = ct.create_unicode_buffer(w.MAX_PATH + 1)
        serial_number        = w.DWORD()
        max_component_length = w.DWORD()
        file_system_flags    = w.DWORD()

        dll.GetVolumeInformationW( drive_letter,
                                   volumeNameBuffer,
                                   ct.sizeof( volumeNameBuffer ),
                                   ct.byref( serial_number ),
                                   ct.byref( max_component_length ),
                                   ct.byref(file_system_flags),
                                   fileSystemNameBuffer,
                                   ct.sizeof( fileSystemNameBuffer ))

        self.mount_point = drive_letter[:-1]
        self.disk_label  = volumeNameBuffer.value
        self.fs_type     = fileSystemNameBuffer.value
        self.max_length  = max_component_length.value
        self.flags       = FSFlags( file_system_flags.value )
        self.serial      = serial_number.value

    @classmethod
    def validate(cls, result, func, args):
        if not result:
            raise ct.WinError(ct.get_last_error())
        return None

    @classmethod
    def getDrives(cls):
        drives = [ chr(x) + ':' for x in range(65,91) if os.path.exists( chr(x) + ':' )]
        return drives

if __name__ == "__main__":
    for drive in VolumeInfo.getDrives():
        vi = VolumeInfo( drive )
        print( '\n'.join([ '',
                           f"{vi.mount_point=}",
                           f"{vi.disk_label=}",
                           f"{vi.fs_type=}",
                           f"{vi.max_length=}",
                           f"{vi.flags=}",
                           f"{vi.serial=}" ]))
