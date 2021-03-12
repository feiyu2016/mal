#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import IntEnum 
import os
import sys

'''
vhd: virtual hard disk formats supported by Microsoft

Functions:
1. Inspect vhd
2. Write asm.bin to vhd boot sector

Todo:
1. write asm.bin to vhd boot sector
2. print vhd file info (-v, -vv)
3. argparse
4. write vhd confirm, force with -f
5. is valid vhd
'''

BIG_ORDER = 'big'

class VirtualHardDiskImage:
    CopyOfHardiskFooter = 512
    DynamicDikHeader = 1024

    def __init__(self, handle):
        self.hdf = None
        self.ddh = None
        self.bat = None

        try:
            self.hdf = HardiskFooter(handle)
            self.ddh = DynamicDiskHeader(handle)
            # n_entries = self.ddh.max_table_entries()
            # self.bat = BAT(handle, n_entries)
        except Exception as inst:
            pass
    
    def is_fixed_vhd(self):
        if self.hdf and HardiskFooterHelper(self.hdf).is_fixed_vhd():
            return True
        return False

        
class HardiskFooter:
    CookieTag = b'conectix'

    # Hard disk footer fields Size(bytes) define
    Cookie = 8
    Features = 4
    FileFormatVersion = 4
    DataOffset = 8
    TimeStamp = 4
    CreatorApplication = 4
    CreatorVersion = 4
    CreatorHostOS = 4
    OriginalSize = 8
    CurrentSize = 8
    DiskGeometry = 4
    DiskType = 4
    Checksum = 4
    UniqueId = 16
    SavedState = 1
    Reserved = 427

    # Hard disk footer fields offset(bytes) define
    OffsetCookie = 0
    OffsetFeatures = 8
    OffsetFileFormatVersion = 12
    OffsetDataOffset = 16
    OffsetTimeStamp = 24
    OffsetCreatorApplication = 28
    OffsetCreatorVersion = 32
    OffsetHostOS = 36
    OffsetOriginalSize = 40
    OffsetCurrentSize = 48
    OffsetDiskGeometry = 56
    OffsetDiskType = 60
    OffsetChecksum = 64
    OffsetUniqueId = 68
    OffsetSavedState = 84
    OffsetReserved = 85

    def __init__(self, handle):
        HardiskFooter.verify_cookie(handle)
        handle.seek(-512, os.SEEK_END)
        self.raw = handle.read() 

    class DiskTypeEnum(IntEnum):
        NoneValue = 0
        Reserved0 = 1
        FixedHardDisk = 2
        DynamicHardDisk = 3
        DifferencingHardDisk = 4
        Reserved1 = 5
        Reserved2 = 6

    def verify_cookie(handle):
        handle.seek(-512, os.SEEK_END)
        cookie = handle.read(HardiskFooter.Cookie) 
        if cookie != HardiskFooter.CookieTag:
            raise Exception("Invalid Hard disk footer")

    def data_offset(self):
        I = HardiskFooter
        p1 = I.OffsetDataOffset
        p2 = p1 + I.DataOffset
        return self.raw[p1:p2]
    
    def disk_type(self):
        I = HardiskFooter
        p1 = I.OffsetDiskType
        p2 = p1 + I.DiskType
        return parse_int(self.raw, p1, p2)

class DynamicDiskHeader:
    CookieTag = b'cxsparse'

    # Dynamic Disk Header fields Size(bytes) define
    Cookie = 8
    DataOffset = 8
    TableOffset = 8
    HeaderVersion = 4
    MaxTableEntries = 4
    BlockSize = 4
    CheckSum = 4
    ParentUniqueID = 16
    ParentTimeStamp = 4
    Reserved = 4
    ParentUnicodeName = 512
    ParentLocatorEntry1 = 24
    ParentLocatorEntry2 = 24
    ParentLocatorEntry3 = 24
    ParentLocatorEntry4 = 24
    ParentLocatorEntry5 = 24
    ParentLocatorEntry6 = 24
    ParentLocatorEntry7 = 24
    ParentLocatorEntry8 = 24
    Reserved = 256

    # Dynamic Disk Header fields offset(bytes) define
    OffsetCookie = 0
    OffsetDataOffset = 8
    OffsetTableOffset = 16
    OffsetHeaderVersion = 24
    OffsetMaxTableEntries = 28
    OffsetBlockSize = 32
    OffsetChecksum = 36
    OffsetParentUniqueID = 40
    OffsetParentTimeStamp = 56
    OffsetReserved = 60
    OffsetParentUnicodeName = 64
    OffsetParentLocatorEntry1 = 576
    OffsetParentLocatorEntry2 = 600
    OffsetParentLocatorEntry3 = 624
    OffsetParentLocatorEntry4 = 648
    OffsetParentLocatorEntry5 = 672
    OffsetParentLocatorEntry6 = 696
    OffsetParentLocatorEntry7 = 720
    OffsetParentLocatorEntry8 = 744
    OffsetReserved = 768

    def __init__(self, handle):
        DynamicDiskHeader.verify_cookie(handle)
        handle.seek(512)
        self.raw = handle.read(1024)
    
    def verify_cookie(handle):
        handle.seek(0)
        cookie = handle.read(HardiskFooter.Cookie)
        if cookie != HardiskFooter.CookieTag:
            raise Exception("Invalid Hard disk footer")
        else:
            handle.seek(512)
            cookie = handle.read(DynamicDiskHeader.Cookie)
            if cookie != DynamicDiskHeader.CookieTag:
                raise Exception("Invalid Dynamic disk header")

    # This field stores the absolute byte offset of the Block 
    # Allocation Table (BAT) in the file.
    def table_offset(self):
        I = DynamicDiskHeader
        p1 = I.OffsetTableOffset 
        p2 = p1 + I.TableOffset
        return parse_int(self.raw, p1, p2)
    
    # This field holds the maximum entries present in the BAT. 
    # This should be equal to the number of blocks in the disk (
    # that is, the disk size divided by the block size).
    def max_table_entries(self):
        I = DynamicDiskHeader
        p1 = I.OffsetMaxTableEntries
        p2 = p1 + I.MaxTableEntries
        return parse_int(self.raw, p1, p2)

class BAT:
    EntrySize = 4

    def __init__(self, handle, n_entries):
        # Copy of hard disk footer + Dynamic Disk Header
        handle.seek(512 + 1024)
        self.raw = handle.read(BAT.EntrySize * n_entries)


class HardiskFooterHelper:

    def __init__(self, hdf):
        self.hdf = hdf

    def is_fixed_vhd(self):
        FIXED_DISK_TAG = b'\xff\xff\xff\xff'
        tag = self.hdf.data_offset()
        dt = self.hdf.disk_type()
        # print("tag = {}, dt = {:X}".format(tag, dt))
        return tag[0:4] == FIXED_DISK_TAG and dt == HardiskFooter.DiskTypeEnum.FixedHardDisk

class BootSector:

    def burn(binfile, vhd):
        with open(binfile, 'rb') as bin_handle:
            # todo: check binfile size <= 510
            bin_buf = bin_handle.read()
            bin_len = len(bin_buf)
            if bin_len > 510:
                raise Exception("Bin file too large")
            
            # build boot sector data
            boot_sector = [0] * 512
            boot_sector[0:bin_len] = bin_buf[:]
            boot_sector[-2] = 0x55
            boot_sector[-1] = 0xaa

            vhd.seek(0)
            vhd.write(bytes(boot_sector))
            vhd.flush()
            

def parse_int(raw, p_begin, p_end):
    v = raw[p_begin:p_end]
    return int.from_bytes(v, byteorder = BIG_ORDER)

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    # todo: check os.path.exist
    with open(dst, 'rb+') as handle:
        vhd_img = VirtualHardDiskImage(handle)
        if vhd_img.is_fixed_vhd():
            BootSector.burn(src, handle)