mov ax,0xb800
mov ds,ax
mov word [0x00],'a'
mov byte [0x01],0x07 ; make char white color
mov word [0x02],'s'
mov byte [0x03],0x07
mov word [0x04],'m'
mov byte [0x05],0x07
jmp $