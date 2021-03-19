#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
from libvhd import util
from libvhd import vhd

'''
vhd: virtual hard disk formats supported by Microsoft

Functions:
1. Inspect vhd
2. Write asm.bin to vhd boot sector

Todo:
* write asm.bin to vhd(dynamic) boot sector
* print vhd file info (-v, -vv)
'''

class BootSector:
    def do_burn(args, vhd_fh):
        bin_len = os.path.getsize(args.src)
        if bin_len > 512:
            print("Error: {} too large, it should <= 512".foramt(args.src))
            return
        
        do_it = args.force_write 
        if not do_it:
            do_it = util.yes_or_no("{} will be overwrite, are you sure? ".format(args.dst))

        if do_it:
            with open(args.src, 'rb') as bin_handle:
                bin_buf = bin_handle.read()

                if bin_len == 512:
                    if bin_buf[-2] != 0x55 or bin_buf[-1] != 0xaa:
                        print("Warn: {} lack of bootable tag".format(args.src))
            
                # build boot sector data
                boot_sector = [0] * 512
                boot_sector[0:bin_len] = bin_buf[:]
                boot_sector[-2] = 0x55
                boot_sector[-1] = 0xaa

                vhd_fh.write(bytes(boot_sector))
                vhd_fh.flush()
                print("Success: {} write to {} boot sector".format(args.src, args.dst))

    def burn(args, vhd_fh):
        vhd_fh.seek(0)
        BootSector.do_burn(args, vhd_fh)
            
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', dest='force_write', action='store_true', help='Without confirm, force write bin to dest vhd file')
    arg_parser.add_argument('src', help='source bin')
    arg_parser.add_argument('dst', help='destination vhd file')
    args = arg_parser.parse_args()

    # check file exists
    if os.path.exists(args.src) and os.path.exists(args.dst):
        with open(args.dst, 'rb+') as handle:
            vhd_img = vhd.VirtualHardDiskImage(handle)
            if vhd_img.is_fixed_vhd():
                BootSector.burn(args, handle)
            else:
                print("Error: {} is not Fixed hard disk image".format(args.dst))
    else:
        print("Error: {} or {} not exist".format(args.src, args.dst))
    