import os
from enum import IntEnum 

'''
vhd: virtual hard disk formats supported by Microsoft

Functions:
1. Inspect vhd
2. Write asm.bin to vhd boot sector

Todo:
1. write asm.bin to vhd boot sector
2. print vhd file info (-vvv)
3. argparse
'''

BIG_ORDER = 'big'

class HardiskFooter:
    # Field length define (in bytes)
    COOKIE = 8
    FEATURES = 4
    FILE_FORMAT_VERSION = 4
    DATA_OFFSET = 8
    TIME_STAMP = 4
    CREATOR_APPLICATION = 4
    CREATOR_VERSION = 4
    CREATOR_HOST_OS = 4
    ORIGINAL_SIZE = 8
    CURRENT_SIZE = 8
    DISK_GEOMETRY = 4
    DISK_TYPE = 4
    CHECKSUM = 4
    UNIQUE_ID = 16
    SAVED_STATE = 1
    RESERVED = 427

    def __init__(self, handle):
        self.hardisk_footer = HardiskFooter.read_hardisk_footer(handle)

    class DiskType(IntEnum):
        NoneValue = 0
        Reserved0 = 1
        FixedHardDisk = 2
        DynamicHardDisk = 3
        DifferencingHardDisk = 4
        Reserved1 = 5
        Reserved2 = 6

    def read_hardisk_footer(handle):
        handle.seek(-512, os.SEEK_END)
        return handle.read()
    
    def data_offset(self):
        I = HardiskFooter
        p1 = I.COOKIE + I.FEATURES + I.FILE_FORMAT_VERSION
        p2 = p1 + I.DATA_OFFSET 
        return self.hardisk_footer[p1:p2]
    
    def disk_type(self):
        I = HardiskFooter
        p1 = I.COOKIE + I.FEATURES + I.FILE_FORMAT_VERSION + I.DATA_OFFSET + I.TIME_STAMP + I.CREATOR_APPLICATION + I.CREATOR_VERSION + I.CREATOR_HOST_OS + I.ORIGINAL_SIZE + I.CURRENT_SIZE + I.DISK_GEOMETRY
        p2 = p1 + I.DISK_TYPE 
        v = self.hardisk_footer[p1:p2]
        v = int.from_bytes(v, BIG_ORDER)
        return v

    
class HardiskFooterHelper:

    def __init__(self, hdf):
        self.hdf = hdf

    def is_fixed_hardisk_image(self):
        FIXED_DISK_TAG = b'\xff\xff\xff\xff'
        tag = self.hdf.data_offset()
        dt = self.hdf.disk_type()
        #print("tag = {}, dt = {}".format(tag, dt))
        return tag[0:4] == FIXED_DISK_TAG and dt == HardiskFooter.DiskType.FixedHardDisk


if __name__ == "__main__":
    handle = open("sample.vhd", "rb")
    hdf = HardiskFooter(handle)
    hdf_helper = HardiskFooterHelper(hdf)
    print(hdf_helper.is_fixed_hardisk_image())
    handle.close()