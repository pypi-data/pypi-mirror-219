#!/bin/bash

loc=$PREFIX/etc/OpenCL/vendors

while read line; do
    echo ${line//\/opt\/anaconda1anaconda2anaconda3/$PREFIX}
done < $loc/intel-cpu.icd > $loc/intel-cpu.icd_fixed

mv $loc/intel-cpu.icd_fixed $loc/intel-cpu.icd

while read line; do
    echo ${line//\/opt\/anaconda1anaconda2anaconda3/$PREFIX}
done < $loc/intel-fpga_emu.icd > $loc/intel-fpga_emu.icd_fixed

mv $loc/intel-fpga_emu.icd_fixed $loc/intel-fpga_emu.icd
