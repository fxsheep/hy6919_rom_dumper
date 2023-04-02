#!/usr/bin/env python3
import os

READROM_GADGET_OFFSET = 0x26D6

def movc_addr(addr):
    ft = open('hy6919_readrom_template.bin', 'rb')
    bin = bytearray(ft.read())
    bin[READROM_GADGET_OFFSET] = (addr >> 8) & 0xff;
    bin[READROM_GADGET_OFFSET + 1] = addr & 0xff;
    ft.close();
    ftmp = open('hy6919_readrom.bin', 'wb')
    ftmp.write(bin)
    ftmp.close()
    os.system('sudo sg_raw -s 10240 /dev/sda df 00 00 00 14 00 00 00 00 00 00 00 00 00 00 d7 < hy6919_readrom.bin')
    os.system('sudo sg_raw -r 512 /dev/sda df 00 08 00 00 00 00 00 00 00 00 00 00 00 00 d6 -o tmp.bin')
    os.system('rm hy6919_readrom.bin')
    fres = open('tmp.bin', 'rb')
    b = bytes(fres.read(1))
    fres.close()
    return b

f = open('hy6919_brom_dump.bin', 'wb')

for i in range(0, 0x9000):
    f.write(movc_addr(i))
os.system('rm tmp.bin')
