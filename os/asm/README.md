### Modern Assembly Language Tutorial

A store for process of learning assembly language.

I hope create a tutorial to help people learn assembly language easily. The tutorial should be modern, interesting, concise.

Why assembly language? Is it out-of-date?

No, assembly language is a key to Operating System, Compiler and Chip Manufacturing.

Ok, let's go.


### tool/vhd.py

A convenient tool to test asm program.

```shell

# create sample.vhd in VirtualBox;
# Note! The sample.vhd must be Fixed size VHD.

# compile asm source
nasm -f bin c4.asm -o c4.bin

# write c4.bin to sample.vhd boot sector 
python vhd.py c4.bin sample.vhd

```